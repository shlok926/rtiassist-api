import pytest
import socket
from bs4 import BeautifulSoup
from models.orm.authority import Authority, AuthorityVerificationHistory
from models.orm.source_registry import OfficialAuthoritySource
from services.source_intelligence import SourceIntelligence
from services.safe_fetcher import SafeFetcher
from datetime import datetime, timezone

from models.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_source_intel.db"
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

class DummyUser:
    email = "test@example.com"

@pytest.fixture
def test_user():
    return DummyUser()

@pytest.fixture
def mock_db_source(db_session, test_user):
    # Create Authority
    authority = Authority(
        department="Test Source Dept",
        government_level="CENTRAL",
        source_url="https://example.com/rti",
        source_type="OFFICIAL_WEBSITE",
        verification_status="VERIFIED",
        last_verified=datetime.now(timezone.utc),
        verified_by=test_user.email
    )
    db_session.add(authority)
    db_session.commit()
    db_session.refresh(authority)

    # Create Source
    source = OfficialAuthoritySource(
        authority_id=authority.id,
        source_url="https://example.com/rti",
        source_type="OFFICIAL_WEBSITE"
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)
    return authority, source

@pytest.mark.asyncio
async def test_irrelevant_source_content_change(db_session, mock_db_source, mocker):
    authority, source = mock_db_source
    
    # Mock a fetch that succeeds
    class MockResponse:
        status = "SUCCESS"
        content = "<html><body><h1>Official RTI Info</h1><p>Date: 2026-09-01</p></body></html>"
        error_message = None
        
    mocker.patch('services.safe_fetcher.SafeFetcher.fetch', return_value=MockResponse())
    
    # First check
    updated_source = await SourceIntelligence.check_source(db_session, source.id)
    assert updated_source.last_parse_status == "PARSED"
    assert updated_source.last_content_hash is not None
    assert updated_source.review_status == "UP_TO_DATE" # first time, no "change" detected
    
    first_hash = updated_source.last_content_hash
    
    # Mock an irrelevant change (script, meta, different layout but same visible text structure... wait, our normalize_and_hash strips meta/script. Let's add a meta tag change)
    MockResponse.content = "<html><head><meta name='csrf' content='new_token'></head><body><h1>Official RTI Info</h1><p>Date: 2026-09-01</p></body></html>"
    updated_source2 = await SourceIntelligence.check_source(db_session, source.id)
    
    assert updated_source2.last_content_hash == first_hash # Hash should match
    assert updated_source2.review_status == "UP_TO_DATE" # No change

@pytest.mark.asyncio
async def test_meaningful_source_content_change(db_session, mock_db_source, mocker):
    authority, source = mock_db_source
    
    class MockResponse:
        status = "SUCCESS"
        content = "<html><body><h1>Official RTI Info</h1></body></html>"
        error_message = None
        
    mocker.patch('services.safe_fetcher.SafeFetcher.fetch', return_value=MockResponse())
    await SourceIntelligence.check_source(db_session, source.id)
    
    # Meaningful change
    MockResponse.content = "<html><body><h1>Official RTI Info</h1><p>New PIO is John Doe</p></body></html>"
    updated_source = await SourceIntelligence.check_source(db_session, source.id)
    
    assert updated_source.review_status == "POTENTIAL_CHANGE_REQUIRES_REVIEW"
    
    # Authority should still be VERIFIED (Fail-closed is manual/semantic)
    db_session.refresh(authority)
    assert authority.verification_status == "VERIFIED"
    
    # Test idempotent changes
    updated_source_again = await SourceIntelligence.check_source(db_session, source.id)
    assert updated_source_again.review_status == "POTENTIAL_CHANGE_REQUIRES_REVIEW"

@pytest.mark.asyncio
async def test_admin_review_downgrade(db_session, mock_db_source):
    authority, source = mock_db_source
    source.review_status = "POTENTIAL_CHANGE_REQUIRES_REVIEW"
    db_session.commit()
    
    # Admin decides it affects authority
    SourceIntelligence.review_and_decide(db_session, source.id, "admin@test.com", "AUTHORITY_CHANGED", "PIO name changed")
    
    db_session.refresh(source)
    db_session.refresh(authority)
    
    assert source.review_status == "UP_TO_DATE"
    assert authority.verification_status == "NEEDS_REVIEW"
    
    # Verify history
    history = db_session.query(AuthorityVerificationHistory).filter(
        AuthorityVerificationHistory.authority_id == authority.id,
        AuthorityVerificationHistory.verification_status == "NEEDS_REVIEW"
    ).first()
    assert history is not None
    assert history.notes == "PIO name changed"

@pytest.mark.asyncio
async def test_admin_review_irrelevant(db_session, mock_db_source):
    authority, source = mock_db_source
    source.review_status = "POTENTIAL_CHANGE_REQUIRES_REVIEW"
    db_session.commit()
    
    # Admin decides it's irrelevant
    SourceIntelligence.review_and_decide(db_session, source.id, "admin@test.com", "IRRELEVANT_CHANGE", "")
    
    db_session.refresh(source)
    db_session.refresh(authority)
    
    assert source.review_status == "UP_TO_DATE"
    assert authority.verification_status == "VERIFIED" # Not downgraded

def test_ssrf_ip_checks():
    # IPv4 Private/Loopback
    assert SafeFetcher.is_ip_safe("127.0.0.1") == False
    assert SafeFetcher.is_ip_safe("10.0.0.1") == False
    assert SafeFetcher.is_ip_safe("192.168.1.1") == False
    assert SafeFetcher.is_ip_safe("169.254.169.254") == False
    
    # IPv6 Loopback/Private
    assert SafeFetcher.is_ip_safe("::1") == False
    assert SafeFetcher.is_ip_safe("fc00::1") == False
    assert SafeFetcher.is_ip_safe("fe80::1") == False
    
    # IPv4-mapped IPv6
    assert SafeFetcher.is_ip_safe("::ffff:127.0.0.1") == False
    assert SafeFetcher.is_ip_safe("::ffff:169.254.169.254") == False
    
    # Public IPs
    assert SafeFetcher.is_ip_safe("8.8.8.8") == True
    assert SafeFetcher.is_ip_safe("2001:4860:4860::8888") == True

def test_dns_resolution_multiple_ips():
    # Since we moved to SafeResolver, we can just test SafeResolver directly
    pass # we'll test it in test_dns_rebinding_protection instead

@pytest.mark.asyncio
async def test_successful_fetch_parser_failure(db_session, mock_db_source, mocker):
    authority, source = mock_db_source
    
    class MockResponse:
        status = "SUCCESS"
        content = "some binary or invalid content"
        error_message = None
        
    mocker.patch('services.safe_fetcher.SafeFetcher.fetch', return_value=MockResponse())
    mocker.patch('services.source_intelligence.SourceIntelligence.normalize_and_extract_text', side_effect=Exception("Parse error"))
    
    updated_source = await SourceIntelligence.check_source(db_session, source.id)
    
    assert updated_source.last_fetch_status == "SUCCESS"
    assert updated_source.last_parse_status == "UNPARSEABLE"
    
    # Authority untouched
    db_session.refresh(authority)
    assert authority.verification_status == "VERIFIED"

@pytest.mark.asyncio
async def test_fetch_failure(db_session, mock_db_source, mocker):
    authority, source = mock_db_source
    
    class MockResponse:
        status = "TIMEOUT"
        content = None
        error_message = "Connection timed out"
        
    mocker.patch('services.safe_fetcher.SafeFetcher.fetch', return_value=MockResponse())
    
    updated_source = await SourceIntelligence.check_source(db_session, source.id)
    
    assert updated_source.last_fetch_status == "TIMEOUT"
    
    # Authority untouched
    db_session.refresh(authority)
    assert authority.verification_status == "VERIFIED"

def test_diff_generation():
    old = "Hello\nWorld"
    new = "Hello\nBrave\nWorld"
    diff = SourceIntelligence.generate_diff(old, new)
    assert "+Brave" in diff
    assert "Hello" in diff

def test_text_extraction_bounds():
    huge_html = "<html><body>" + ("<p>Text</p>" * 20000) + "</body></html>"
    extracted = SourceIntelligence.normalize_and_extract_text(huge_html)
    assert len(extracted) <= 100020  # 100KB limit + truncate msg

@pytest.mark.asyncio
async def test_dns_rebinding_protection(mocker):
    from services.safe_fetcher import SafeResolver
    import socket
    
    # We test the logic of SafeResolver
    resolver = SafeResolver()
    
    # Mock the aiohttp's built-in async resolve to return one safe and one unsafe IP
    async def mock_super_resolve(*args, **kwargs):
        return [
            {'host': '8.8.8.8', 'family': socket.AF_INET},
            {'host': '127.0.0.1', 'family': socket.AF_INET}
        ]
        
    mocker.patch('aiohttp.resolver.ThreadedResolver.resolve', new=mock_super_resolve)
    
    # Should filter out 127.0.0.1
    hosts = await resolver.resolve("example.com")
    assert len(hosts) == 1
    assert hosts[0]['host'] == '8.8.8.8'

@pytest.mark.asyncio
async def test_dns_rebinding_protection_blocks_all(mocker):
    from services.safe_fetcher import SafeResolver
    import socket
    
    resolver = SafeResolver()
    
    async def mock_super_resolve(*args, **kwargs):
        return [
            {'host': '127.0.0.1', 'family': socket.AF_INET}
        ]
        
    mocker.patch('aiohttp.resolver.ThreadedResolver.resolve', new=mock_super_resolve)
    
    with pytest.raises(ValueError, match="SSRF protection blocked the request"):
        await resolver.resolve("example.com")

@pytest.mark.asyncio
async def test_safe_fetcher_integration_blocks_unsafe_dns(mocker):
    # This tests the entire fetch/connector path
    # If the domain resolves to an unsafe IP, SafeFetcher.fetch should fail before connecting
    import socket
    
    # We mock the built-in threaded resolver to return an unsafe IP
    async def mock_threaded_resolve(*args, **kwargs):
        return [
            {'host': '127.0.0.1', 'family': socket.AF_INET}
        ]
        
    mocker.patch('aiohttp.resolver.ThreadedResolver.resolve', new=mock_threaded_resolve)
    
    from services.safe_fetcher import SafeFetcher
    result = await SafeFetcher.fetch("https://example.com/api")
    
    # It must fail because of the resolver's SSRF protection
    assert "SSRF protection blocked the request" in result.error_message

# ==========================================
# STEP 1B: STRUCTURED INTELLIGENCE TESTS
# ==========================================
from services.deterministic_extractor import DeterministicExtractor

def test_extractor_pio_name_table():
    html = """
    <html><body>
    <table>
        <tr><th>Public Information Officer</th><td>Shri Ramesh Kumar</td></tr>
    </table>
    </body></html>
    """
    fields = DeterministicExtractor.extract_from_html(html, "OFFICIAL_RTI_PAGE")
    assert "pio_name" in fields
    assert fields["pio_name"].value == "Shri Ramesh Kumar"
    assert fields["pio_name"].confidence == "HIGH"
    
def test_extractor_fee_label():
    html = """
    <html><body>
    <div><strong>RTI Fee:</strong> Rs 10/-</div>
    </body></html>
    """
    fields = DeterministicExtractor.extract_from_html(html, "OFFICIAL_RTI_PAGE")
    assert "filing_fee" in fields
    assert fields["filing_fee"].value == "Rs 10/-"
    assert fields["filing_fee"].confidence == "HIGH"

def test_extractor_ambiguous_pio():
    html = """
    <html><body>
    <table>
        <tr><th>PIO</th><td>Officer A</td></tr>
        <tr><th>PIO</th><td>Officer B</td></tr>
    </table>
    </body></html>
    """
    fields = DeterministicExtractor.extract_from_html(html, "OFFICIAL_RTI_PAGE")
    assert "pio_name" in fields
    assert fields["pio_name"].confidence == "AMBIGUOUS"
    assert fields["pio_name"].value == "MULTIPLE_CANDIDATES"

@pytest.mark.asyncio
async def test_structured_change_proposals(db_session, mock_db_source, mocker):
    authority, source = mock_db_source
    # Ensure initial values
    authority.pio_name = "Old Officer"
    authority.verification_status = "UNVERIFIED"
    db_session.commit()
    
    class MockResponse:
        status = "SUCCESS"
        content = "<html><body><table><tr><th>Public Information Officer</th><td>Old Officer</td></tr></table></body></html>"
        error_message = None
        
    mocker.patch('services.safe_fetcher.SafeFetcher.fetch', return_value=MockResponse())
    
    # Run intelligence once to set baseline
    await SourceIntelligence.check_source(db_session, source.id)
    
    # Change content
    MockResponse.content = "<html><body><table><tr><th>Public Information Officer</th><td>New Officer</td></tr></table></body></html>"
    
    # Run intelligence again to trigger change detection
    updated_source = await SourceIntelligence.check_source(db_session, source.id)
    
    # Verify proposal is created
    from models.orm.source_registry import ProposedAuthorityChange
    proposals = db_session.query(ProposedAuthorityChange).filter(ProposedAuthorityChange.source_id == source.id).all()
    
    assert len(proposals) == 1
    assert proposals[0].field_name == "pio_name"
    assert proposals[0].old_value == "Old Officer"
    assert proposals[0].proposed_value == "New Officer"
    assert proposals[0].change_type == "CHANGED"
    assert proposals[0].review_status == "PENDING_REVIEW"
    
    # Simulate Admin API Review (Accept)
    from routes.admin_authorities import review_proposed_change
    from models.schemas import ProposedAuthorityChangeReviewRequest
    from models.orm.user import User
    
    admin = User(email="admin@test.com", role="ADMIN")
    req = ProposedAuthorityChangeReviewRequest(decision="ACCEPT", notes="Looks good")
    
    review_proposed_change(proposals[0].id, req, db_session, admin)
    
    # Verify authority is updated atomically
    db_session.refresh(authority)
    assert authority.pio_name == "New Officer"
    assert authority.verification_status == "UNVERIFIED" # Kept as is
    
    # Verify audit history
    from models.orm.authority import AuthorityVerificationHistory
    history = db_session.query(AuthorityVerificationHistory).filter(
        AuthorityVerificationHistory.authority_id == authority.id,
        AuthorityVerificationHistory.notes.like("%Accepted extraction for pio_name: Old Officer -> New Officer%")
    ).first()
    assert history is not None


