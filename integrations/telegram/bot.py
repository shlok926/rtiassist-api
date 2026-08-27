import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .handlers import start_cmd, help_cmd, cases_cmd, newcase_cmd, handle_message, button_callback

def get_telegram_app():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        return None
        
    app = Application.builder().token(token).updater(None).build()
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("cases", cases_cmd))
    app.add_handler(CommandHandler("newcase", newcase_cmd))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_message))
    
    return app
