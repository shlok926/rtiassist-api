import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.orm.source_registry import OfficialAuthoritySource
from services.source_intelligence import SourceIntelligence

logger = logging.getLogger(__name__)

class SourceMonitoringService:
    DEFAULT_INTERVAL_HOURS = 24
    MAX_CONSECUTIVE_FAILURES = 5

    @classmethod
    async def run_due_checks(
        cls, 
        db: Session, 
        limit: int = 10,
        interval_hours: Optional[int] = None,
        max_concurrency: int = 5
    ) -> dict:
        """
        Finds due sources, locks them, and processes them concurrently.
        """
        now = datetime.now(timezone.utc)
        base_interval = timedelta(hours=interval_hours or cls.DEFAULT_INTERVAL_HOURS)
        
        # 1. Find due active sources that are not locked
        # Or locked more than 1 hour ago (stale lock recovery)
        stale_lock_threshold = now - timedelta(hours=1)
        
        due_sources = db.query(OfficialAuthoritySource).filter(
            OfficialAuthoritySource.is_active == True,
            or_(
                OfficialAuthoritySource.is_locked == False,
                OfficialAuthoritySource.locked_at < stale_lock_threshold
            ),
            or_(
                OfficialAuthoritySource.next_check_at == None,
                OfficialAuthoritySource.next_check_at <= now
            )
        ).limit(limit).all()
        
        if not due_sources:
            return {"processed": 0, "success": 0, "failed": 0}
            
        # 2. Lock them immediately (Basic concurrency protection)
        source_ids = []
        for src in due_sources:
            src.is_locked = True
            src.locked_at = now
            source_ids.append(src.id)
        
        db.commit()
        
        logger.info(f"Locked {len(source_ids)} sources for monitoring.")
        
        # 3. Process concurrently with a semaphore
        semaphore = asyncio.Semaphore(max_concurrency)
        
        success_count = 0
        failed_count = 0
        
        async def process_source(source_id: str):
            nonlocal success_count, failed_count
            async with semaphore:
                # We need a fresh session context or careful management if using one session.
                # Since check_source handles its own commits on the session, we'll use the shared one 
                # but we must be aware of concurrent commits. 
                # In SQLAlchemy, concurrent async operations on the SAME session are dangerous.
                # To be absolutely safe for Alpha, we'll process them sequentially in this loop, 
                # or we require a session factory. 
                # Given FastAPI usually provides 1 session per request/task, sequential is safer for DB.
                pass
                
        # To avoid SQLite concurrency issues on the shared session, we'll process sequentially for now.
        # This guarantees atomicity per source without session tearing.
        for source_id in source_ids:
            try:
                # Fetch fresh from DB
                src = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
                if not src:
                    continue
                    
                updated_source = await SourceIntelligence.check_source(db, source_id)
                
                # Check if it was a fetch failure
                if updated_source.last_fetch_status in ["SUCCESS", "PARSED", "UNPARSEABLE"]:
                    # Includes parser failures, because the fetch succeeded.
                    src.consecutive_failures = 0
                    src.next_check_at = datetime.now(timezone.utc) + base_interval
                    success_count += 1
                else:
                    # Timeout, unavailable, etc.
                    src.consecutive_failures += 1
                    backoff_multiplier = min(2 ** (src.consecutive_failures - 1), 24) # max 24x backoff
                    backoff_time = base_interval * backoff_multiplier
                    src.next_check_at = datetime.now(timezone.utc) + backoff_time
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Error monitoring source {source_id}: {str(e)}")
                # Recover lock on exception
                src = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
                if src:
                    src.consecutive_failures += 1
                    backoff_time = base_interval * min(2 ** (src.consecutive_failures - 1), 24)
                    src.next_check_at = datetime.now(timezone.utc) + backoff_time
                    failed_count += 1
            finally:
                # Always unlock
                src = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
                if src:
                    src.is_locked = False
                    src.locked_at = None
                    db.commit()
                    
        return {
            "processed": len(source_ids),
            "success": success_count,
            "failed": failed_count
        }
