from sqlalchemy.orm import Session
from models.orm.user import User

def get_or_create_dev_user(db: Session) -> User:
    """Mock authentication user for development."""
    dev_telegram_id = "DEV_USER_001"
    user = db.query(User).filter(User.telegram_id == dev_telegram_id).first()
    if not user:
        user = User(
            telegram_id=dev_telegram_id,
            first_name="Developer",
            last_name="Account",
            email="dev@example.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.email is None:
        user.email = "dev@example.com"
        db.commit()
    return user
