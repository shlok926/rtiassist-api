import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from integrations.telegram.identity import get_or_create_telegram_user
from models.database import SessionLocal
from models.orm.user import User

from models.database import engine, Base
from sqlalchemy.orm import sessionmaker

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    import models.orm
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@patch('integrations.telegram.handlers.get_db_session')
def test_telegram_identity_resolution(mock_get_db):
    db = TestSessionLocal()
    mock_get_db.return_value = db
    try:
        user = get_or_create_telegram_user(db, "123456789", "John", "Doe")
        assert user.telegram_id == "123456789"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        
        # Second time should fetch the same user
        user2 = get_or_create_telegram_user(db, "123456789", "John", "Doe")
        assert user.id == user2.id
    finally:
        db.close()

@pytest.mark.asyncio
@patch('integrations.telegram.handlers.get_db_session')
async def test_start_command(mock_get_db):
    db = TestSessionLocal()
    mock_get_db.return_value = db
    try:
        from integrations.telegram.handlers import start_cmd
        update = MagicMock()
        update.effective_user.id = 999999
        update.effective_user.first_name = "Alice"
        update.effective_user.last_name = "Smith"
        
        update.message = AsyncMock()
        
        context = MagicMock()
        
        await start_cmd(update, context)
        
        update.message.reply_text.assert_called_once()
        args, kwargs = update.message.reply_text.call_args
        assert "Welcome to RTIAssist" in args[0]
    finally:
        db.close()
