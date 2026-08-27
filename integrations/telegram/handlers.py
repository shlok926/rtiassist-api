import os
import io
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.database import SessionLocal
from models.schemas import CaseCreate, ActionConfirmation
from services import case_service, document_service, response_service
from .identity import get_or_create_telegram_user
from .formatters import format_case_summary, format_action_recommendation, format_response_analysis

def get_db_session():
    return SessionLocal()

async def get_user_from_update(update: Update):
    db = get_db_session()
    try:
        tg_user = update.effective_user
        user = get_or_create_telegram_user(db, str(tg_user.id), tg_user.first_name, tg_user.last_name)
        return user, db
    except Exception:
        db.close()
        raise

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, db = await get_user_from_update(update)
    db.close()
    
    msg = (
        "🏛 *Welcome to RTIAssist (Telegram Client)*\n\n"
        "I can help you manage your RTI cases using our backend services.\n\n"
        "Available commands:\n"
        "/newcase - Start a new RTI case\n"
        "/cases - View your active cases\n"
        "/help - Show instructions"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📖 *RTIAssist Help*\n\n"
        "/newcase - Start a new RTI case. Tell me your problem, and I'll recommend the next legal action.\n"
        "/cases - View your active cases, deadlines, and generated documents.\n"
        "\n*Note*: Complex operations like Appeal formatting and advanced uploads should be done on the web application."
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def cases_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, db = await get_user_from_update(update)
    try:
        case_list = case_service.get_cases(db, user.id, skip=0, limit=10)
        
        if not case_list.cases:
            await update.message.reply_text("📭 You don't have any cases yet. Use /newcase to start.")
            return
            
        for case in case_list.cases:
            keyboard = [[InlineKeyboardButton("View Details", callback_data=f"view_case_{case.id}")]]
            
            if case.status == "ACTION_RECOMMENDED":
                keyboard.append([InlineKeyboardButton("Confirm Action", callback_data=f"confirm_action_{case.id}")])
            elif case.status in ["READY_TO_FILE", "DRAFT_GENERATED", "AUTHORITY_RESOLVED"]:
                keyboard.append([InlineKeyboardButton("Generate / View Document", callback_data=f"doc_{case.id}")])
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                format_case_summary(case),
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    finally:
        db.close()

async def newcase_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Set conversation state
    context.user_data['state'] = 'WAITING_FOR_PROBLEM'
    await update.message.reply_text(
        "📝 *Start a New Case*\n\n"
        "What problem are you facing? Describe it in a few sentences.",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get('state')
    
    if state == 'WAITING_FOR_PROBLEM':
        user_text = update.message.text.strip()
        if len(user_text) < 15:
            await update.message.reply_text("Please provide a bit more detail (at least 15 characters).")
            return
            
        user, db = await get_user_from_update(update)
        try:
            processing_msg = await update.message.reply_text("⏳ Creating case and analyzing your problem via backend services...")
            
            # Create case using existing case_service
            case_data = CaseCreate(
                problem_description=user_text,
                title=f"Telegram Case - {user_text[:20]}..."
            )
            case = case_service.create_case(db, user.id, case_data)
            
            # Get action recommendation using existing service
            rec = case_service.get_action_recommendation(db, case.id, user.id)
            
            context.user_data['state'] = None
            
            await processing_msg.edit_text(
                format_action_recommendation(rec),
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Confirm Action", callback_data=f"confirm_action_{case.id}")]])
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        finally:
            db.close()
    
    # Check for document upload (Government Response)
    elif update.message.document:
        await handle_document(update, context)
        
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # We expect a PDF response upload
    doc = update.message.document
    if not doc.file_name.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please upload a PDF file.")
        return
        
    if doc.file_size > 10 * 1024 * 1024:
        await update.message.reply_text("❌ File is too large (max 10MB).")
        return
        
    case_id = context.user_data.get('waiting_for_response_case_id')
    if not case_id:
        await update.message.reply_text("Please select 'Upload Response' on a specific case first.")
        return
        
    user, db = await get_user_from_update(update)
    try:
        processing = await update.message.reply_text("⏳ Uploading and analyzing response...")
        
        file = await context.bot.get_file(doc.file_id)
        pdf_bytes = await file.download_as_bytearray()
        
        # We need to simulate UploadFile for the existing response_service
        from fastapi import UploadFile
        import tempfile
        
        # Create a temp file to pass to response_service
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
            
        with open(tmp_path, "rb") as f:
            upload_file = UploadFile(filename=doc.file_name, file=f)
            analysis = await response_service.upload_and_analyze_response(db, case_id, user.id, upload_file)
            
        os.unlink(tmp_path)
        context.user_data['waiting_for_response_case_id'] = None
        
        await processing.edit_text(
            format_response_analysis(analysis),
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error analyzing response: {str(e)}")
    finally:
        db.close()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user, db = await get_user_from_update(update)
    
    try:
        if data.startswith("confirm_action_"):
            case_id = data.replace("confirm_action_", "")
            try:
                confirmation = ActionConfirmation(confirmed=True)
                case_service.confirm_action(db, case_id, user.id, confirmation)
                
                # Automatically trigger authority resolution via service
                case_service.resolve_case_authority(db, case_id, user.id)
                
                keyboard = [[InlineKeyboardButton("Generate Document", callback_data=f"doc_{case_id}")]]
                await query.edit_message_text(
                    "✅ Action Confirmed & Authority Resolved via Service.\n\nReady to generate document.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                await query.edit_message_text(f"❌ Error: {str(e)}")
                
        elif data.startswith("doc_"):
            case_id = data.replace("doc_", "")
            try:
                from models.schemas import DocumentGenerateRequest
                req = DocumentGenerateRequest(language="english")
                doc = document_service.generate_case_document(db, case_id, user.id, req)
                
                keyboard = [[InlineKeyboardButton("Download PDF (Web)", url=f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/cases/{case_id}")]]
                await query.edit_message_text(
                    f"📄 *Document Generated (v{doc.version})*\n\n{doc.content[:500]}...\n\n_Please use the Web Application to download the full PDF and file it._",
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                await query.edit_message_text(f"❌ Error: {str(e)}")
                
        elif data.startswith("view_case_"):
            case_id = data.replace("view_case_", "")
            case = case_service.get_case(db, case_id, user.id)
            
            keyboard = []
            if case.status == "FILED" or case.status == "AWAITING_RESPONSE":
                keyboard.append([InlineKeyboardButton("Upload Government Response", callback_data=f"upload_resp_{case_id}")])
                
            keyboard.append([InlineKeyboardButton("View on Web", url=f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/cases/{case_id}")])
            
            await query.edit_message_text(
                format_case_summary(case),
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
        elif data.startswith("upload_resp_"):
            case_id = data.replace("upload_resp_", "")
            context.user_data['waiting_for_response_case_id'] = case_id
            await query.edit_message_text("📤 Please upload the PDF of the Government Response now.")
            
    finally:
        db.close()
