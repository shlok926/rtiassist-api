from sqlalchemy.orm import Session
from models.orm.user import User

def get_or_create_telegram_user(db: Session, telegram_id: str, first_name: str, last_name: str = None) -> User:
    """Resolve Telegram identity. If user doesn't exist, create one."""
    user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
    if not user:
        # Create a new user for Telegram
        user = User(
            telegram_id=str(telegram_id),
            first_name=first_name,
            last_name=last_name,
            # We don't set email/password for pure Telegram users unless they link accounts later
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
