import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock

from models.orm.source_registry import OfficialAuthoritySource
from services.source_monitoring import SourceMonitoringService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.orm.authority import Authority

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_source_monitoring.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def mock_db_source(db_session):
    authority = Authority(
        id="AUTH_MOCK_001",
        government_level="STATE",
        department="Test Department",
        verification_status="VERIFIED",
        last_verified=datetime.now(timezone.utc),
        source_url="https://example.gov.in/rti",
        source_type="OFFICIAL_WEBSITE"
    )
    source = OfficialAuthoritySource(
        id="SRC_MOCK_001",
        authority_id=authority.id,
        source_url="https://example.gov.in/rti",
        source_type="OFFICIAL_WEBSITE",
        last_fetch_status="SUCCESS"
    )
    db_session.add(authority)
    db_session.add(source)
    db_session.commit()
    return authority, source

@pytest.fixture
def test_monitoring_source(db_session, setup_db, mock_db_source):
    authority, source = mock_db_source
    source.is_active = True
    source.is_locked = False
    source.next_check_at = datetime.now(timezone.utc) - timedelta(hours=1) # due
    source.consecutive_failures = 0
    db_session.commit()
    db_session.refresh(source)
    return authority, source


@pytest.mark.asyncio
async def test_scheduler_selects_due_source(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    
    mock_check = AsyncMock(return_value=source)
    # mock the parser to not do actual fetch
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check)
    
    results = await SourceMonitoringService.run_due_checks(db_session)
    
    assert results["processed"] == 1
    assert mock_check.called
    db_session.refresh(source)
    
    # Handle SQLite stripping timezone info
    next_check = source.next_check_at.replace(tzinfo=timezone.utc) if source.next_check_at.tzinfo is None else source.next_check_at
    assert next_check > datetime.now(timezone.utc)
    
    assert source.is_locked == False
    assert source.consecutive_failures == 0


@pytest.mark.asyncio
async def test_scheduler_skips_future_source(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    source.next_check_at = datetime.now(timezone.utc) + timedelta(hours=1)
    db_session.commit()
    
    mock_check = AsyncMock()
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check)
    
    results = await SourceMonitoringService.run_due_checks(db_session)
    
    assert results["processed"] == 0
    assert not mock_check.called


@pytest.mark.asyncio
async def test_scheduler_skips_inactive_source(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    source.is_active = False
    db_session.commit()
    
    mock_check = AsyncMock()
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check)
    
    results = await SourceMonitoringService.run_due_checks(db_session)
    
    assert results["processed"] == 0
    assert not mock_check.called


@pytest.mark.asyncio
async def test_scheduler_skips_locked_source(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    source.is_locked = True
    source.locked_at = datetime.now(timezone.utc) # recently locked
    db_session.commit()
    
    mock_check = AsyncMock()
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check)
    
    results = await SourceMonitoringService.run_due_checks(db_session)
    
    assert results["processed"] == 0
    assert not mock_check.called


@pytest.mark.asyncio
async def test_scheduler_recovers_stale_lock(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    source.is_locked = True
    source.locked_at = datetime.now(timezone.utc) - timedelta(hours=2) # stale lock
    db_session.commit()
    
    mock_check = AsyncMock(return_value=source)
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check)
    
    results = await SourceMonitoringService.run_due_checks(db_session)
    
    assert results["processed"] == 1
    assert mock_check.called
    db_session.refresh(source)
    assert source.is_locked == False


@pytest.mark.asyncio
async def test_failure_backoff(db_session, test_monitoring_source, mocker):
    authority, source = test_monitoring_source
    source.last_fetch_status = "TIMEOUT" # Simulated failure output
    
    # Check source mock
    async def mock_check_source(db, src_id):
        # We don't change anything, just simulate the failure output
        return source
        
    mocker.patch('services.source_intelligence.SourceIntelligence.check_source', side_effect=mock_check_source)
    
    results = await SourceMonitoringService.run_due_checks(db_session, interval_hours=1)
    
    assert results["processed"] == 1
    assert results["failed"] == 1
    
    db_session.refresh(source)
    assert source.consecutive_failures == 1
    
    # Run again, simulating immediate due
    source.next_check_at = datetime.now(timezone.utc) - timedelta(hours=1)
    db_session.commit()
    
    results2 = await SourceMonitoringService.run_due_checks(db_session, interval_hours=1)
    assert results2["failed"] == 1
    
    db_session.refresh(source)
    assert source.consecutive_failures == 2
    # Next check should be pushed out further due to backoff
    next_check = source.next_check_at.replace(tzinfo=timezone.utc) if source.next_check_at.tzinfo is None else source.next_check_at
    assert next_check > datetime.now(timezone.utc) + timedelta(hours=1.5)
