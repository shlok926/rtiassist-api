import hashlib
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.orm.source_registry import OfficialAuthoritySource, ProposedAuthorityChange
from models.orm.authority import Authority, AuthorityVerificationHistory
from services.safe_fetcher import SafeFetcher
from services.deterministic_extractor import DeterministicExtractor

class SourceIntelligence:
    
    @staticmethod
    def normalize_and_extract_text(html_content: str) -> str:
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove noisy elements
        for element in soup(["script", "style", "meta", "noscript", "header", "footer", "nav"]):
            element.decompose()
            
        # Get text and normalize whitespace
        text = soup.get_text(separator=" ")
        normalized_text = " ".join(text.split())
        
        # Bound the size to prevent DB bloat (store max 100KB of text per source)
        if len(normalized_text) > 100000:
            normalized_text = normalized_text[:100000] + "\n...[TRUNCATED]"
            
        return normalized_text

    @staticmethod
    def get_hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_diff(old_text: str, new_text: str) -> str:
        import difflib
        if not old_text:
            return "No previous content to compare."
            
        diff = difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile='previous',
            tofile='current',
            lineterm=''
        )
        return '\n'.join(diff)

    @staticmethod
    async def check_source(db: Session, source_id: str) -> OfficialAuthoritySource:
        source = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
        if not source or not source.is_active:
            return source
            
        fetch_result = await SafeFetcher.fetch(source.source_url)
        
        source.last_checked_at = datetime.now(timezone.utc)
        source.last_fetch_status = fetch_result.status
        source.last_fetch_error = fetch_result.error_message
        
        if fetch_result.status == "SUCCESS":
            source.last_successful_fetch_at = datetime.now(timezone.utc)
            
            try:
                extracted_text = SourceIntelligence.normalize_and_extract_text(fetch_result.content)
                new_hash = SourceIntelligence.get_hash(extracted_text)
                source.last_parse_status = "PARSED"
                
                if not source.last_content_hash:
                    # First time checking
                    source.last_content_hash = new_hash
                    source.last_extracted_text = extracted_text
                elif source.last_content_hash != new_hash:
                    # Content changed.
                    source.last_content_hash = new_hash
                    source.previous_extracted_text = source.last_extracted_text
                    source.last_extracted_text = extracted_text
                    source.review_status = "POTENTIAL_CHANGE_REQUIRES_REVIEW"
                    
                    # Step 1B: Structured Extraction
                    extracted_fields = DeterministicExtractor.extract_from_html(fetch_result.content, source.source_type)
                    authority = db.query(Authority).filter(Authority.id == source.authority_id).first()
                    
                    if authority:
                        for field_name, ext_field in extracted_fields.items():
                            old_val = getattr(authority, field_name, None)
                            
                            if ext_field.confidence == "AMBIGUOUS":
                                change_type = "AMBIGUOUS"
                            elif old_val is None and ext_field.value:
                                change_type = "ADDED"
                            elif str(old_val) != ext_field.value:
                                change_type = "CHANGED"
                            else:
                                continue # UNCHANGED
                                
                            # Check if proposal already exists and is pending
                            existing_proposal = db.query(ProposedAuthorityChange).filter(
                                ProposedAuthorityChange.source_id == source.id,
                                ProposedAuthorityChange.field_name == field_name,
                                ProposedAuthorityChange.review_status == "PENDING_REVIEW"
                            ).first()
                            
                            if existing_proposal:
                                existing_proposal.proposed_value = ext_field.value
                                existing_proposal.evidence_snippet = ext_field.evidence
                                existing_proposal.change_type = change_type
                                existing_proposal.confidence = ext_field.confidence
                                existing_proposal.old_value = str(old_val) if old_val is not None else None
                            else:
                                proposal = ProposedAuthorityChange(
                                    source_id=source.id,
                                    authority_id=authority.id,
                                    field_name=field_name,
                                    old_value=str(old_val) if old_val is not None else None,
                                    proposed_value=ext_field.value,
                                    evidence_snippet=ext_field.evidence,
                                    change_type=change_type,
                                    confidence=ext_field.confidence
                                )
                                db.add(proposal)
                    
            except Exception:
                source.last_parse_status = "UNPARSEABLE"
        
        db.commit()
        db.refresh(source)
        return source

    @staticmethod
    def review_and_decide(db: Session, source_id: str, admin_email: str, decision: str, notes: str) -> OfficialAuthoritySource:
        """
        Decision can be:
        - "IRRELEVANT_CHANGE": Admin confirms the change doesn't affect authority info.
        - "AUTHORITY_CHANGED": Admin confirms the change affects the authority.
        """
        source = db.query(OfficialAuthoritySource).filter(OfficialAuthoritySource.id == source_id).first()
        if not source:
            raise ValueError("Source not found")
            
        if decision == "IRRELEVANT_CHANGE":
            source.review_status = "UP_TO_DATE"
            db.commit()
            
        elif decision == "AUTHORITY_CHANGED":
            source.review_status = "UP_TO_DATE"
            
            # This is where the fail-closed kicks in, driven by admin decision or future semantic AI
            authority = db.query(Authority).filter(Authority.id == source.authority_id).first()
            if authority and authority.verification_status == "VERIFIED":
                authority.verification_status = "NEEDS_REVIEW"
                
                history = AuthorityVerificationHistory(
                    authority_id=authority.id,
                    source_url=source.source_url,
                    source_type=source.source_type,
                    verification_status="NEEDS_REVIEW",
                    verified_by=admin_email,
                    notes=notes or "Admin confirmed source changes affect authority data."
                )
                db.add(history)
            db.commit()
            
        return source
