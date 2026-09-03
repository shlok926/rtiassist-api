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
        
        due_source_ids = db.query(OfficialAuthoritySource.id).filter(
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
        
        if not due_source_ids:
            return {"processed": 0, "success": 0, "failed": 0}
            
        # Extract scalar IDs
        source_ids = [row[0] for row in due_source_ids]
            
        # 2. Lock them atomically (Basic concurrency protection)
        updated_count = db.query(OfficialAuthoritySource).filter(
            OfficialAuthoritySource.id.in_(source_ids),
            or_(
                OfficialAuthoritySource.is_locked == False,
                OfficialAuthoritySource.locked_at < stale_lock_threshold
            )
        ).update({"is_locked": True, "locked_at": now}, synchronize_session='fetch')
        
        db.commit()
        
        # If another worker locked them first, updated_count might be less.
        # We only process the ones we successfully locked.
        # Actually, to be safe, we just process source_ids and check is_locked == True and locked_at == now.
        
        logger.info(f"Atomically locked {updated_count} sources for monitoring.")
        
        success_count = 0
        failed_count = 0
                
        # To avoid SQLite concurrency issues on the shared session, we'll process sequentially for now.
        # This guarantees atomicity per source without session tearing.
        for source_id in source_ids:
            try:
                # Fetch fresh from DB
                src = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
                if not src:
                    continue
                
                # Check if we actually acquired the lock
                if not src.is_locked:
                    continue
                    
                # Handle SQLite dropping tzinfo
                src_locked_at = src.locked_at.replace(tzinfo=timezone.utc) if src.locked_at and src.locked_at.tzinfo is None else src.locked_at
                
                # Check if the lock was acquired by us just now (within 5 seconds to account for precision loss)
                if not src_locked_at or abs((src_locked_at - now).total_seconds()) > 5:
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
