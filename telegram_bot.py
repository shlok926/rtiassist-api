"""
RTIAssist — Telegram Bot v3
Features: Dual language system (UI + Draft), State auto-detect, Appeal generator, PDF Export
"""

import os
import asyncio
import requests
import io
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from bot_languages import get_message, get_language_keyboard, UI_LANGUAGES, DRAFT_LANGUAGES

# PDF Export support
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ reportlab not installed. PDF export will not be available.")

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

# ── STATE AUTO-DETECT ────────────────────────────
STATE_KEYWORDS = {
    "Maharashtra": ["maharashtra", "mumbai", "pune", "nagpur", "nashik"],
    "Delhi": ["delhi", "new delhi"],
    "Uttar Pradesh": ["uttar pradesh", "lucknow", "kanpur", "varanasi", "agra", " up "],
    "Gujarat": ["gujarat", "ahmedabad", "surat", "vadodara"],
    "Rajasthan": ["rajasthan", "jaipur", "jodhpur", "udaipur"],
    "Bihar": ["bihar", "patna", "gaya"],
    "West Bengal": ["west bengal", "kolkata", "bengal"],
    "Karnataka": ["karnataka", "bangalore", "bengaluru", "mysore"],
    "Tamil Nadu": ["tamil nadu", "chennai", "madurai", "tamilnadu"],
    "Kerala": ["kerala", "kochi", "thiruvananthapuram", "kozhikode"],
    "Madhya Pradesh": ["madhya pradesh", "bhopal", "indore", " mp "],
    "Punjab": ["punjab", "amritsar", "ludhiana"],
    "Haryana": ["haryana", "gurgaon", "gurugram", "faridabad"],
    "Andhra Pradesh": ["andhra pradesh", "visakhapatnam", "vijayawada"],
    "Telangana": ["telangana", "hyderabad"],
    "Odisha": ["odisha", "orissa", "bhubaneswar"],
    "Assam": ["assam", "guwahati"],
    "Jharkhand": ["jharkhand", "ranchi"],
    "Chhattisgarh": ["chhattisgarh", "raipur"],
    "Uttarakhand": ["uttarakhand", "dehradun"],
}

def auto_detect_state(text: str):
    t = text.lower()
    for state, keywords in STATE_KEYWORDS.items():
        for kw in keywords:
            if kw in t:
                return state
    return None

# ── CATEGORY AUTO-DETECT ─────────────────────────
CATEGORY_KEYWORDS = {
    "Food & Ration": ["ration", "food", "pds", "ration card", "grain", "wheat", "rice", "sugar"],
    "Land & Revenue": ["land", "mutation", "property", "revenue", "tehsil", "patwari", "jamabandi", "khasra"],
    "Passport & Visa": ["passport", "visa", "regional passport office", "rpo", "police verification"],
    "Pension & Social Security": ["pension", "old age", "widow", "disability pension", "social security"],
    "Education & Scholarship": ["scholarship", "school", "college", "education", "fee", "admission", "certificate"],
    "Health": ["hospital", "health", "medical", "medicine", "doctor", "treatment", "ambulance"],
    "Police & Law": ["police", "fir", "complaint", "investigation", "crime", "station"],
    "Municipal Services": ["water supply", "garbage", "sewage", "municipality", "corporation", "sanitation"],
    "Electricity & Water": ["electricity", "power", "bijli", "meter", "bill", "connection", "water supply"],
    "Roads & Infrastructure": ["road", "pmgsy", "construction", "bridge", "infrastructure", "highway"],
    "Employment": ["job", "employment", "nrega", "mgnrega", "labour", "worker", "salary"],
    "Banking & Finance": ["bank", "loan", "account", "mudra", "finance", "subsidy", "pmjdy"],
}

def auto_detect_category(text: str):
    t = text.lower()
    # Count matches for each category
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in t)
        if score > 0:
            category_scores[category] = score
    
    # Return category with highest score
    if category_scores:
        return max(category_scores, key=category_scores.get)
    return "Other"

# ── CATEGORY SELECTION KEYBOARD ──────────────────
def get_category_keyboard():
    categories = [
        "🔄 Auto-detect",
        "🍚 Food & Ration",
        "🌾 Land & Revenue", 
        "📘 Passport & Visa",
        "👴 Pension & Social Security",
        "🎓 Education & Scholarship",
        "🏥 Health",
        "🚔 Police & Law",
        "🏙️ Municipal Services",
        "⚡ Electricity & Water",
        "🛣️ Roads & Infrastructure",
        "💼 Employment",
        "🏦 Banking & Finance",
        "📋 Other",
    ]
    
    keyboard = []
    # 2 buttons per row
    for i in range(0, len(categories), 2):
        row = categories[i:i+2]
        keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}") for cat in row])
    
    return InlineKeyboardMarkup(keyboard)

# ── STATE SELECTION KEYBOARD ─────────────────────
def get_state_keyboard():
    rows = [
        ["🏛 Central Govt", "Maharashtra", "Delhi"],
        ["Uttar Pradesh", "Gujarat", "Rajasthan"],
        ["Bihar", "West Bengal", "Karnataka"],
        ["Tamil Nadu", "Kerala", "Madhya Pradesh"],
        ["Punjab", "Haryana", "Andhra Pradesh"],
        ["Telangana", "Odisha", "Assam"],
        ["Jharkhand", "Chhattisgarh", "Uttarakhand"],
        ["❌ Cancel"],
    ]
    keyboard = []
    for row in rows:
        keyboard.append([InlineKeyboardButton(s, callback_data=f"state_{s}") for s in row])
    return InlineKeyboardMarkup(keyboard)


# ── LEGAL TOOLS KEYBOARD ─────────────────────────
def get_legal_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Second Appeal (CIC) — FREE", callback_data="legal_sa")],
        [InlineKeyboardButton("🛒 Consumer Complaint — FREE", callback_data="legal_cc")],
        [InlineKeyboardButton("📜 Legal Notice — FREE", callback_data="legal_ln")],
        [InlineKeyboardButton("💼 Labour Complaint — FREE", callback_data="legal_lc")],
        [InlineKeyboardButton("⬅️ Back to Tools", callback_data="show_tools")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_tool_keyboard(lang="english"):
    """Main tool selection keyboard shown after language selection"""
    if lang == "english":
        keyboard = [
            [InlineKeyboardButton("🏙️ Generate RTI Application", callback_data="tool_rti")],
            [InlineKeyboardButton("⚖️ Legal Tools (4 Free Tools)", callback_data="tool_legal")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🏙️ RTI Application Banayein", callback_data="tool_rti")],
            [InlineKeyboardButton("⚖️ Kanuni Tools (4 Muft Tools)", callback_data="tool_legal")],
        ]
    return InlineKeyboardMarkup(keyboard)


async def show_tool_menu(chat_or_msg, lang, edit=False):
    """Show the main tool selection menu"""
    if lang == "english":
        text = (
            "🏙️ *What would you like to do today?*\n\n"
            "📌 *RTI Generation* — File an RTI application\n"
            "⚖️ *Legal Tools* — Second Appeal, Consumer Complaint, Legal Notice, Labour Complaint"
        )
    else:
        text = (
            "🏙️ *Aaj aap kya karna chahte hain?*\n\n"
            "📌 *RTI Generation* — RTI application file karein\n"
            "⚖️ *Kanuni Tools* — Doosri Appeal, Consumer Complaint, Legal Notice, Labour Complaint"
        )
    keyboard = get_tool_keyboard(lang)
    if edit:
        await chat_or_msg.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
    else:
        await chat_or_msg.reply_text(text, parse_mode='Markdown', reply_markup=keyboard)


# ── /start ───────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'ui_language' not in context.user_data:
        # Step 1: Choose language
        await update.message.reply_text(
            get_message("english", "choose_language"),
            parse_mode='Markdown',
            reply_markup=get_language_keyboard("ui")
        )
    else:
        # Already set — show tool menu
        lang = context.user_data.get('ui_language', 'english')
        context.user_data.pop('pending_legal_tool', None)
        context.user_data.pop('pending_text', None)
        await show_tool_menu(update.message, lang)


# ── /state ───────────────────────────────────────
async def state_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 *Apna State select karo:*",
        parse_mode='Markdown',
        reply_markup=get_state_keyboard()
    )


# ── /help ────────────────────────────────────────
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('ui_language', 'english')
    await update.message.reply_text(
        get_message(lang, "help"),
        parse_mode='Markdown'
    )


# ── PDF EXPORT FUNCTION ──────────────────────────
def generate_pdf(draft_text, department, state, user_name):
    """Generate PDF from RTI draft"""
    if not PDF_AVAILABLE:
        return None
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#FF6B00',
        spaceAfter=20,
        alignment=1  # Center
    )
    
    # Normal style
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=16
    )
    
    # Add title
    story.append(Paragraph("RTI Application", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add metadata
    metadata = f"""
    <b>Generated by:</b> RTIAssist AI<br/>
    <b>Date:</b> {datetime.now().strftime('%d %B %Y')}<br/>
    <b>Department:</b> {department}<br/>
    <b>State:</b> {state}<br/>
    <b>Applicant:</b> {user_name}<br/>
    """
    story.append(Paragraph(metadata, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Add draft text (escape HTML special chars)
    draft_escaped = draft_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    draft_paragraphs = draft_escaped.split('\n')
    
    for para in draft_paragraphs:
        if para.strip():
            story.append(Paragraph(para, normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# ── /about ───────────────────────────────────────
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('ui_language', 'english')
    await update.message.reply_text(
        get_message(lang, "about"),
        parse_mode='Markdown'
    )


# ── /fee ─────────────────────────────────────────
async def fee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('ui_language', 'english')
    await update.message.reply_text(
        get_message(lang, "fee_details"),
        parse_mode='Markdown'
    )


# ── /legal ───────────────────────────────────────
async def legal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('ui_language', 'english')
    msg = (
        "⚖️ *RTIAssist Legal Tools*\n\n"
        "Free legal documents — no advocate fees!\n\n"
        "Choose a tool:"
    ) if lang == "english" else (
        "⚖️ *RTIAssist कानूनी टूल्स*\n\n"
        "मुफ्त कानूनी दस्तावेज़ — वकील की फीस नहीं!\n\n"
        "टूल चुनें:"
    )
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_legal_keyboard())


# ── LEGAL TOOLS — INPUT PARSER & GENERATOR ──────
def parse_legal_input(text):
    """Parse key: value lines from user message"""
    result = {}
    for line in text.strip().split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            result[key.strip().lower()] = val.strip()
    return result


async def handle_legal_input(msg_obj, context, user_text, user_name, tool):
    lang = context.user_data.get('ui_language', 'english')
    fields = parse_legal_input(user_text)

    payload = {'tool': tool}

    if tool == 'second_appeal':
        payload.update({
            'name': fields.get('name', user_name),
            'department': fields.get('department', ''),
            'rti_date': fields.get('rti date', fields.get('rti_date', '')),
            'appeal_date': fields.get('appeal date', fields.get('appeal_date', '')),
            'query': fields.get('query', ''),
            'reason': fields.get('reason', 'no_response'),
            'details': fields.get('details', ''),
        })
    elif tool == 'consumer_complaint':
        payload.update({
            'name': fields.get('name', user_name),
            'address': fields.get('address', ''),
            'company': fields.get('company', ''),
            'type': fields.get('type', 'service_deficiency'),
            'description': fields.get('description', ''),
            'amount': fields.get('amount', ''),
            'purchase_date': fields.get('date', ''),
            'relief': fields.get('relief', 'all'),
        })
    elif tool == 'legal_notice':
        payload.update({
            'sender': fields.get('from', user_name),
            'recipient': fields.get('to', ''),
            'type': fields.get('type', 'contract_breach'),
            'description': fields.get('description', ''),
            'amount': fields.get('amount', ''),
            'state': fields.get('state', ''),
        })
    elif tool == 'labour_complaint':
        payload.update({
            'name': fields.get('name', user_name),
            'employer': fields.get('employer', ''),
            'type': fields.get('type', 'salary_unpaid'),
            'description': fields.get('description', ''),
            'amount': fields.get('amount', ''),
            'state': fields.get('state', ''),
        })

    processing = await msg_obj.reply_text(
        "⚖️ Generating your document..." if lang == "english" else "⚖️ दस्तावेज़ बन रहा है...",
        parse_mode='Markdown'
    )

    try:
        response = requests.post(
            f"{API_BASE}/legal/generate",
            json=payload,
            timeout=30
        )
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}")

        data = response.json()
        draft = data.get('draft', '')

        await processing.edit_text(
            "✅ *Document Ready!*" if lang == "english" else "✅ *दस्तावेज़ तैयार है!*",
            parse_mode='Markdown'
        )

        chunks = [draft[i:i+3800] for i in range(0, len(draft), 3800)]
        for i, chunk in enumerate(chunks):
            part_label = f" — Part {i+1}/{len(chunks)}" if len(chunks) > 1 else ""
            await msg_obj.reply_text(
                f"📄 *Your Document{part_label}:*\n\n```\n{chunk}\n```",
                parse_mode='Markdown'
            )

        context.user_data['last_draft'] = draft
        context.user_data['last_dept'] = tool.replace('_', ' ').title()
        context.user_data['last_state'] = fields.get('state', 'India')
        context.user_data.pop('pending_legal_tool', None)

        keyboard = [
            [InlineKeyboardButton("📄 Download PDF", callback_data="export_pdf")],
            [InlineKeyboardButton("⚖️ More Legal Tools", callback_data="legal_menu")],
            [InlineKeyboardButton("📋 Generate RTI", callback_data="new_rti")],
        ]
        await msg_obj.reply_text(
            "What would you like to do next?" if lang == "english" else "आगे क्या करना है?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        context.user_data.pop('pending_legal_tool', None)
        await processing.edit_text(
            f"❌ Error: {str(e)[:200]}" if lang == "english" else f"❌ त्रुटि: {str(e)[:200]}"
        )


# ── CORE GENERATE FUNCTION ───────────────────────
async def generate_rti(msg_obj, context, user_text, state, user_name, draft_lang):
    """Generate RTI with specified draft language"""
    lang = context.user_data.get('ui_language', 'english')
    await msg_obj.chat.send_action('typing')

    state_display = state if state and state != "🏛 Central Govt" else "Central"

    processing_msg = await msg_obj.reply_text(
        get_message(lang, "processing", state_display),
        parse_mode='Markdown'
    )

    try:
        api_state = state if state and state != "🏛 Central Govt" else None

        response = requests.post(
            f"{API_BASE}/rti/generate",
            json={
                "description": user_text,
                "language": draft_lang,
                "state": api_state,
                "demo_mode": os.getenv("DEMO_MODE", "false").lower() == "true"
            },
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}")

        data = response.json()

        await processing_msg.edit_text(
            get_message(lang, "generating"),
            parse_mode='Markdown'
        )
        await asyncio.sleep(1)

        dept    = data.get('department', 'Unknown')
        ministry= data.get('ministry', 'Unknown')
        score   = data.get('quality_score', 0)
        urgency = (data.get('urgency', 'routine') or 'routine').upper()
        success = (data.get('estimated_success_probability', 'medium') or 'medium').upper()
        risk    = (data.get('exempt_risk', 'low') or 'low').upper()
        draft   = data.get('draft', '')
        filing  = data.get('filing_instructions', '')

        score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"

        await processing_msg.edit_text(
            get_message(lang, "rti_ready", user_name, dept, ministry, 
                       state_display, urgency, score_emoji, score, success, risk),
            parse_mode='Markdown'
        )

        # Send draft (split if too long)
        if draft:
            chunks = [draft[i:i+3800] for i in range(0, len(draft), 3800)]
            for i, chunk in enumerate(chunks):
                part_label = f" — Part {i+1}/{len(chunks)}" if len(chunks)>1 else ""
                label = get_message(lang, "draft_label", part_label)
                await msg_obj.reply_text(
                    f"{label}\n\n```\n{chunk}\n```",
                    parse_mode='Markdown'
                )

        # Filing instructions
        if filing:
            instructions_label = get_message(lang, "filing_instructions")
            await msg_obj.reply_text(
                f"{instructions_label}\n\n{filing[:800]}",
                parse_mode='Markdown'
            )

        # Save for appeal and PDF export
        context.user_data['last_rti'] = data
        context.user_data['last_desc'] = user_text
        context.user_data['last_draft'] = draft
        context.user_data['last_dept'] = dept
        context.user_data['last_state'] = state_display
        context.user_data['last_warnings'] = data.get('warnings', [])
        context.user_data['last_suggestions'] = data.get('suggestions', [])
        context.user_data['last_score'] = score
        context.user_data['last_success'] = success
        context.user_data['last_risk'] = risk

        # Action buttons
        keyboard = [
            [
                InlineKeyboardButton("📄 Download PDF", callback_data="export_pdf"),
                InlineKeyboardButton("💾 Save as Text", callback_data="save_txt"),
            ],
            [
                InlineKeyboardButton("💡 AI Suggestions", callback_data="ai_suggestions"),
                InlineKeyboardButton("🌐 How to File Online", callback_data="how_to_file"),
            ],
            [
                InlineKeyboardButton(get_message(lang, "generate_appeal"),
                                   callback_data="gen_appeal"),
                InlineKeyboardButton(get_message(lang, "fee_info"),
                                   callback_data="fee_info"),
            ],
            [
                InlineKeyboardButton("📋 File on RTIOnline.gov.in",
                                   url="https://rtionline.gov.in"),
            ],
            [
                InlineKeyboardButton(get_message(lang, "new_rti"),
                                   callback_data="new_rti"),
            ]
        ]
        await msg_obj.reply_text(
            get_message(lang, "action_message"),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except requests.exceptions.ConnectionError:
        await processing_msg.edit_text(
            get_message(lang, "server_error"),
            parse_mode='Markdown'
        )
    except Exception as e:
        await processing_msg.edit_text(
            get_message(lang, "error", str(e)[:200]),
            parse_mode='Markdown'
        )


# ── MESSAGE HANDLER ──────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if UI language is set
    if 'ui_language' not in context.user_data:
        await update.message.reply_text(
            get_message("english", "choose_language"),
            parse_mode='Markdown',
            reply_markup=get_language_keyboard("ui")
        )
        return
    
    lang = context.user_data['ui_language']
    user_text = update.message.text.strip()
    user_name = update.message.from_user.first_name or "Friend"

    # Check if user is filling a legal tool form
    pending_legal = context.user_data.get('pending_legal_tool')
    if pending_legal:
        await handle_legal_input(update.message, context, user_text, user_name, pending_legal)
        return

    # Check if user is in RTI mode (selected RTI from tool menu)
    # OR they just typed directly (backward compat)
    pending_tool = context.user_data.get('pending_tool')
    if pending_tool != 'rti' and pending_tool is not None:
        # Unknown state, reset to tool menu
        await show_tool_menu(update.message, lang)
        return

    if len(user_text) < 15:
        await update.message.reply_text(
            get_message(lang, "problem_too_short"),
            parse_mode='Markdown'
        )
        return

    # Try auto-detect state
    detected_state = auto_detect_state(user_text)
    
    # Try auto-detect category
    detected_category = auto_detect_category(user_text)

    # Store user data for later
    context.user_data['pending_text'] = user_text
    context.user_data['pending_state'] = detected_state
    context.user_data['pending_category'] = detected_category
    context.user_data['pending_name'] = user_name
    
    if detected_state:
        # State found — now show detected category and ask to confirm
        category_display = detected_category.replace("🍚 ", "").replace("🌾 ", "").replace("📘 ", "").replace("👴 ", "").replace("🎓 ", "").replace("🏥 ", "").replace("🚔 ", "").replace("🏙️ ", "").replace("⚡ ", "").replace("🛣️ ", "").replace("💼 ", "").replace("🏦 ", "").replace("📋 ", "")
        
        msg = f"✅ *State:* {detected_state}\n📂 *Category:* {detected_category}\n\n" + get_message(lang, "confirm_category")
        
        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data="confirm_category")],
            [InlineKeyboardButton("🔄 Change Category", callback_data="change_category")]
        ]
        
        await update.message.reply_text(
            msg,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # State not found — ask to select state first
        await update.message.reply_text(
            get_message(lang, "state_not_detected"),
            parse_mode='Markdown',
            reply_markup=get_state_keyboard()
        )


# ── BUTTON CALLBACKS ─────────────────────────────
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_name = query.from_user.first_name or "Friend"
    
    # ── UI Language Selection ──
    if query.data.startswith("uilang_"):
        selected_lang = query.data.replace("uilang_", "")
        context.user_data['ui_language'] = selected_lang
        lang_name = UI_LANGUAGES.get(selected_lang, "English")

        # Step 1 done — confirm language set
        await query.message.edit_text(
            get_message(selected_lang, "language_set", lang_name),
            parse_mode='Markdown'
        )

        # Step 2 — show tool selection menu
        await show_tool_menu(query.message, selected_lang)
        return
    
    # ── Draft Language Selection ──
    if query.data.startswith("draftlang_"):
        selected_lang = query.data.replace("draftlang_", "")
        
        pending_text = context.user_data.get('pending_text')
        pending_state = context.user_data.get('pending_state')
        pending_name = context.user_data.get('pending_name', user_name)
        
        if not pending_text:
            lang = context.user_data.get('ui_language', 'english')
            await query.message.edit_text(
                get_message(lang, "problem_too_short"),
                parse_mode='Markdown'
            )
            return
        
        # If state is not detected yet, ask for state selection
        if not pending_state:
            context.user_data['pending_draft_lang'] = selected_lang
            lang = context.user_data.get('ui_language', 'english')
            await query.message.edit_text(
                get_message(lang, "state_not_detected"),
                parse_mode='Markdown'
            )
            await query.message.reply_text(
                get_message(lang, "state_not_detected"),
                parse_mode='Markdown',
                reply_markup=get_state_keyboard()
            )
            return
        
        # State detected — generate RTI with selected draft language
        lang = context.user_data.get('ui_language', 'english')
        await query.message.edit_text(
            get_message(lang, "state_selected", pending_state),
            parse_mode='Markdown'
        )
        context.user_data.pop('pending_text', None)
        context.user_data.pop('pending_state', None)
        context.user_data.pop('pending_category', None)
        await generate_rti(query.message, context, pending_text, pending_state, 
                          pending_name, selected_lang)
        return

    # ── Category Confirmation ──
    if query.data == "confirm_category":
        lang = context.user_data.get('ui_language', 'english')
        pending_category = context.user_data.get('pending_category', 'Other')
        
        await query.message.edit_text(
            f"✅ *Category:* {pending_category}",
            parse_mode='Markdown'
        )
        
        # Now ask for draft language
        await query.message.reply_text(
            get_message(lang, "choose_draft_language"),
            parse_mode='Markdown',
            reply_markup=get_language_keyboard("draft")
        )
        return

    # ── Change Category ──
    if query.data == "change_category":
        lang = context.user_data.get('ui_language', 'english')
        
        await query.message.edit_text(
            "📂 *Select Category:*" if lang == "english" else "📂 *श्रेणी चुनें:*",
            parse_mode='Markdown',
            reply_markup=get_category_keyboard()
        )
        return

    # ── Category Selection ──
    if query.data.startswith("cat_"):
        selected_category = query.data.replace("cat_", "")
        lang = context.user_data.get('ui_language', 'english')
        
        # Handle auto-detect
        if "Auto-detect" in selected_category:
            pending_text = context.user_data.get('pending_text', '')
            selected_category = auto_detect_category(pending_text)
        
        # Update pending category
        context.user_data['pending_category'] = selected_category
        
        await query.message.edit_text(
            f"✅ *Category:* {selected_category}",
            parse_mode='Markdown'
        )
        
        # Now ask for draft language
        await query.message.reply_text(
            get_message(lang, "choose_draft_language"),
            parse_mode='Markdown',
            reply_markup=get_language_keyboard("draft")
        )
        return

    # ── State Selection ──
    if query.data.startswith("state_"):
        selected = query.data.replace("state_", "")

        if selected == "❌ Cancel":
            lang = context.user_data.get('ui_language', 'english')
            await query.message.edit_text(
                "❌ Cancelled" if lang == "english" else "❌ रद्द किया गया"
            )
            return

        pending_text = context.user_data.get('pending_text')
        pending_name = context.user_data.get('pending_name', user_name)
        pending_draft_lang = context.user_data.get('pending_draft_lang')
        lang = context.user_data.get('ui_language', 'english')

        if not pending_text:
            # State set for future use
            context.user_data['selected_state'] = selected
            await query.message.edit_text(
                f"✅ State set: *{selected}*\n\nNow type your problem!" if lang == "english"
                else f"✅ राज्य सेट: *{selected}*\n\nअब अपनी समस्या लिखें!",
                parse_mode='Markdown'
            )
            return

        # If draft language already selected, generate RTI
        if pending_draft_lang:
            await query.message.edit_text(
                get_message(lang, "state_selected", selected),
                parse_mode='Markdown'
            )
            context.user_data.pop('pending_text', None)
            context.user_data.pop('pending_draft_lang', None)
            await generate_rti(query.message, context, pending_text, selected, 
                              pending_name, pending_draft_lang)
        else:
            # Ask for draft language
            context.user_data['pending_state'] = selected
            await query.message.edit_text(
                f"✅ State: *{selected}*",
                parse_mode='Markdown'
            )
            await query.message.reply_text(
                get_message(lang, "choose_draft_language"),
                parse_mode='Markdown',
                reply_markup=get_language_keyboard("draft")
            )
        return

    # ── Tool Selection ──
    if query.data == "show_tools":
        lang = context.user_data.get('ui_language', 'english')
        context.user_data.pop('pending_legal_tool', None)
        context.user_data.pop('pending_text', None)
        await show_tool_menu(query.message, lang, edit=True)
        return

    if query.data == "tool_rti":
        lang = context.user_data.get('ui_language', 'english')
        context.user_data['pending_tool'] = 'rti'
        prompt = (
            "📝 *Describe your problem in any language*\n\n"
            "Write in detail: what happened, which department, how long pending.\n\n"
            "*Example:*\n"
            "_My ration card application was rejected 3 months ago in Maharashtra, no reason given_"
        ) if lang == "english" else (
            "📝 *Apni problem kisi bhi bhasha mein likhein*\n\n"
            "Detail mein likhein: kya hua, kaun sa department, kitne time se pending.\n\n"
            "*Udaharan:*\n"
            "_Mera ration card Maharashtra mein 3 mahine se reject hai, koi karan nahi bataya_"
        )
        await query.message.edit_text(prompt, parse_mode='Markdown')
        return

    if query.data == "tool_legal":
        lang = context.user_data.get('ui_language', 'english')
        msg = (
            "⚖️ *Legal Tools — Choose:*\n\n"
            "All tools are completely FREE"
        ) if lang == "english" else (
            "⚖️ *Kanuni Tools — Chunein:*\n\n"
            "Sab tools bilkul muft hain"
        )
        await query.message.edit_text(msg, parse_mode='Markdown', reply_markup=get_legal_keyboard())
        return

    # ── Legal Tool Callbacks ──
    if query.data == "legal_menu":
        lang = context.user_data.get('ui_language', 'english')
        msg = "⚖️ *Legal Tools — Choose:*" if lang == "english" else "⚖️ *Kanuni Tools — Chunein:*"
        await query.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_legal_keyboard())
        return

    if query.data == "legal_sa":
        context.user_data['pending_legal_tool'] = 'second_appeal'
        await query.message.reply_text(
            "📝 *Second Appeal (CIC)*\n\n"
            "Send your details in this format:\n\n"
            "```\n"
            "Name: Your Full Name\n"
            "Department: Ministry/Department Name\n"
            "RTI Date: DD/MM/YYYY\n"
            "Appeal Date: DD/MM/YYYY\n"
            "Query: What you asked in RTI\n"
            "Reason: no_response / incomplete / denied / delay\n"
            "Details: Any extra context (optional)\n"
            "```",
            parse_mode='Markdown'
        )
        return

    if query.data == "legal_cc":
        context.user_data['pending_legal_tool'] = 'consumer_complaint'
        await query.message.reply_text(
            "🛒 *Consumer Complaint*\n\n"
            "Send your details in this format:\n\n"
            "```\n"
            "Name: Your Full Name\n"
            "Address: Your Address\n"
            "Company: Company Name\n"
            "Type: defective_product / service_deficiency / refund_denied / overcharging / builder_delay / insurance_claim / bank_issue\n"
            "Description: What happened\n"
            "Amount: Amount in rupees\n"
            "Date: DD/MM/YYYY\n"
            "Relief: refund / replacement / compensation / all\n"
            "```",
            parse_mode='Markdown'
        )
        return

    if query.data == "legal_ln":
        context.user_data['pending_legal_tool'] = 'legal_notice'
        await query.message.reply_text(
            "📜 *Legal Notice*\n\n"
            "Send your details in this format:\n\n"
            "```\n"
            "From: Your Name\n"
            "To: Recipient Name\n"
            "Type: rent_deposit / property_dispute / money_recovery / cheque_bounce / contract_breach / employment / family_maintenance\n"
            "Description: Issue details\n"
            "Amount: Amount in rupees (if any)\n"
            "State: Your State\n"
            "```",
            parse_mode='Markdown'
        )
        return

    if query.data == "legal_lc":
        context.user_data['pending_legal_tool'] = 'labour_complaint'
        await query.message.reply_text(
            "💼 *Labour Complaint*\n\n"
            "Send your details in this format:\n\n"
            "```\n"
            "Name: Your Full Name\n"
            "Employer: Company/Employer Name\n"
            "Type: salary_unpaid / wrongful_termination / pf_not_deposited / esi_not_provided / overtime_unpaid / gratuity_denied\n"
            "Description: What happened\n"
            "Amount: Amount in rupees (if any)\n"
            "State: Your State\n"
            "```",
            parse_mode='Markdown'
        )
        return

    # ── Other Button Actions ──
    lang = context.user_data.get('ui_language', 'english')
    
    if query.data == "fee_info":
        await query.message.reply_text(
            get_message(lang, "fee_details"),
            parse_mode='Markdown'
        )

    elif query.data == "save_txt":
        last_draft = context.user_data.get('last_draft')
        last_dept = context.user_data.get('last_dept', 'RTI')
        if not last_draft:
            await query.message.reply_text("⚠️ No draft to save. Please generate an RTI first.")
            return
        txt_bytes = last_draft.encode('utf-8')
        filename = f"RTI_{last_dept.replace(' ', '_')}.txt"
        await query.message.reply_document(
            document=io.BytesIO(txt_bytes),
            filename=filename,
            caption=(
                "✅ *RTI Draft saved as text file.*\nOpen it in any text editor or Notepad."
                if lang == "english" else
                "✅ *RTI Draft text file saved.*\nKisi bhi text editor mein khol sakte hain."
            ),
            parse_mode='Markdown'
        )

    elif query.data == "ai_suggestions":
        last_draft = context.user_data.get('last_draft', '')
        warnings   = context.user_data.get('last_warnings', [])
        suggestions= context.user_data.get('last_suggestions', [])
        score      = context.user_data.get('last_score', 0)
        success    = context.user_data.get('last_success', 'MEDIUM')
        risk       = context.user_data.get('last_risk', 'LOW')
        dept       = context.user_data.get('last_dept', 'Department')
        if not last_draft:
            await query.message.reply_text("⚠️ Generate an RTI first.")
            return
        score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        warn_text = "\n".join([f"  ⚠️ {w}" for w in warnings]) if warnings else "  ✅ No issues found"
        sugg_text = "\n".join([f"  • {s}" for s in suggestions]) if suggestions else "  ✅ Draft looks complete"
        tips = (
            f"💡 *AI Analysis of Your RTI Draft*\n"
            f"{'='*32}\n"
            f"🎯 *Department:* {dept}\n"
            f"{score_emoji} *Quality Score:* {score}/100\n"
            f"📈 *Success Probability:* {success}\n"
            f"⚠️ *Exemption Risk:* {risk}\n\n"
            f"🔍 *Issues Detected:*\n{warn_text}\n\n"
            f"✨ *Improvement Tips:*\n{sugg_text}\n\n"
            f"📌 *General Best Practices:*\n"
            f"  • Mention specific dates, file numbers wherever possible\n"
            f"  • Ask for certified copies of documents\n"
            f"  • Keep queries specific — avoid vague questions\n"
            f"  • Attach proof of fee payment (IPO/DD/online receipt)\n"
            f"  • Send via Speed Post with tracking for proof of delivery\n"
            f"  • File before 5 PM on working days"
        )
        await query.message.reply_text(tips, parse_mode='Markdown')

    elif query.data == "how_to_file":
        dept  = context.user_data.get('last_dept', 'Central Ministry')
        state = context.user_data.get('last_state', 'Central')
        is_central = state.lower() in ('central', 'none', '', 'none')
        if lang == "english":
            guide = (
                f"🌐 *How to File Your RTI Application*\n"
                f"{'='*34}\n\n"
                f"🚀 *Option 1 — Online (Easiest & Free)*\n"
                f"🔗 [RTI Online Portal](https://rtionline.gov.in)\n\n"
                f"*Steps:*\n"
                f"1️⃣ Go to rtionline\.gov\.in\n"
                f"2️⃣ Click *\'Submit Request\'* → Register / Login\n"
                f"3️⃣ Select Ministry/Department: *{dept}*\n"
                f"4️⃣ Paste the draft from this chat\n"
                f"5️⃣ Pay ₹10 fee — Debit/Credit/Net Banking/UPI\n"
                f"6️⃣ Submit → Save the *Registration Number*\n"
                f"7️⃣ Check reply status at: *RTI Online → View Status*\n\n"
                f"📮 *Option 2 — By Post*\n"
                f"1️⃣ Print the draft → Download PDF from this chat\n"
                f"2️⃣ Attach ₹10 IPO (Indian Postal Order) or Court Fee Stamp\n"
                f"3️⃣ Attach a plain white paper with your address for reply\n"
                f"4️⃣ Send via *Speed Post* to the PIO of {dept}\n"
                f"5️⃣ Keep tracking number as proof\n"
                f"6️⃣ Reply must come within *30 days*\n\n"
                f"⏰ *Deadlines:*\n"
                f"  • PIO reply: 30 days\n"
                f"  • Life & liberty matters: 48 hours\n"
                f"  • First Appeal: 30 days after no reply\n"
                f"  • Second Appeal (CIC): 90 days after First Appeal\n\n"
                f"💰 *Fee:* ₹10 (BPL applicants: FREE)\n"
                f"❌ *No fee for state RTIs in some states*"
            )
        else:
            guide = (
                f"🌐 *RTI Application Kaise File Karen*\n"
                f"{'='*32}\n\n"
                f"🚀 *Option 1 — Online (Sabse Aasan)*\n"
                f"🔗 [RTI Online Portal](https://rtionline.gov.in)\n\n"
                f"*Steps:*\n"
                f"1️⃣ rtionline\.gov\.in kholen\n"
                f"2️⃣ *\'Submit Request\' par click karen* → Register/Login\n"
                f"3️⃣ Ministry/Department chunen: *{dept}*\n"
                f"4️⃣ Is chat se draft paste karen\n"
                f"5️⃣ ₹10 fee bharen — Debit/Credit/Net Banking/UPI\n"
                f"6️⃣ Submit karen → *Registration Number save karen*\n"
                f"7️⃣ Reply status: *RTI Online → View Status*\n\n"
                f"📮 *Option 2 — Post se*\n"
                f"1️⃣ Draft print karen → is chat se PDF download karen\n"
                f"2️⃣ ₹10 ka IPO (Indian Postal Order) lagaen\n"
                f"3️⃣ Apne address ka ek paper saath lagaen\n"
                f"4️⃣ *Speed Post* se {dept} ke PIO ko bhejen\n"
                f"5️⃣ Tracking number sambhal kar rakhen\n"
                f"6️⃣ Jawab *30 din* mein aana chahiye\n\n"
                f"⏰ *Deadlines:*\n"
                f"  • PIO reply: 30 din\n"
                f"  • Jeevan-swatantrata: 48 ghante\n"
                f"  • Pehli Appeal: jawab na aane par 30 din mein\n"
                f"  • Doosri Appeal (CIC): 90 din mein\n\n"
                f"💰 *Fee:* ₹10 (BPL: MUFT)\n"
                f"❌ *Kuch states mein state RTI free hoti hai*"
            )
        await query.message.reply_text(guide, parse_mode='Markdown', disable_web_page_preview=True)

    elif query.data == "new_rti":
        lang = context.user_data.get('ui_language', 'english')
        context.user_data.pop('pending_legal_tool', None)
        context.user_data.pop('pending_text', None)
        await show_tool_menu(query.message, lang)

    elif query.data == "gen_appeal":
        last_rti = context.user_data.get('last_rti')
        if not last_rti:
            warning = "⚠️ First generate an RTI." if lang == "english" else "⚠️ पहले एक RTI जनरेट करें।"
            await query.message.reply_text(warning)
            return

        dept    = last_rti.get('department', '[Department]')
        ministry= last_rti.get('ministry', '[Ministry]')
        info    = context.user_data.get('last_desc', '[Information requested]')

        appeal = (
            "[DATE]\n\nTo:\nThe First Appellate Authority,\n"
            f"{dept},\n{ministry}\n\n"
            "Subject: First Appeal under Section 19(1) of RTI Act, 2005\n\n"
            "Respected Sir/Madam,\n\n"
            "1. I had filed an RTI on [DATE_OF_ORIGINAL_RTI] seeking:\n"
            f"   \"{info[:250]}\"\n\n"
            "2. The PIO has not responded within 30 days as required\n"
            "   under Section 7(1) of the RTI Act 2005.\n\n"
            "3. I hereby appeal and request:\n"
            "   a) Complete information be provided immediately\n"
            "   b) Penalty under Section 20(1) on defaulting PIO\n"
            "   c) Compensation for delay under Section 19(8)(b)\n\n"
            "Yours faithfully,\n\n[Your Full Name]\n[Address]\n[Phone]\n[Email]"
        )
        label = "📝 *First Appeal Letter:*" if lang == "english" else "📝 *प्रथम अपील पत्र:*"
        await query.message.reply_text(
            f"{label}\n\n```\n{appeal[:3800]}\n```",
            parse_mode='Markdown'
        )

    elif query.data == "export_pdf":
        # PDF Export Handler
        if not PDF_AVAILABLE:
            error_msg = "❌ PDF export not available. Install reportlab: pip install reportlab" if lang == "english" else "❌ PDF एक्सपोर्ट उपलब्ध नहीं है।"
            await query.message.reply_text(error_msg)
            return
        
        last_draft = context.user_data.get('last_draft')
        last_dept = context.user_data.get('last_dept', 'Unknown Department')
        last_state = context.user_data.get('last_state', 'Unknown')
        
        if not last_draft:
            warning = "⚠️ First generate an RTI." if lang == "english" else "⚠️ पहले एक RTI जनरेट करें।"
            await query.message.reply_text(warning)
            return
        
        # Generate PDF
        try:
            await query.message.reply_text(
                "📄 Generating PDF..." if lang == "english" else "📄 PDF बन रहा है...",
                parse_mode='Markdown'
            )
            
            pdf_buffer = generate_pdf(
                last_draft, 
                last_dept, 
                last_state, 
                user_name
            )
            
            if pdf_buffer:
                filename = f"RTI_{last_dept.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                await query.message.reply_document(
                    document=pdf_buffer,
                    filename=filename,
                    caption="✅ RTI Application PDF" if lang == "english" else "✅ RTI आवेदन PDF"
                )
            else:
                await query.message.reply_text(
                    "❌ PDF generation failed" if lang == "english" else "❌ PDF बनाने में त्रुटि"
                )
        except Exception as e:
            await query.message.reply_text(
                f"❌ Error: {str(e)}" if lang == "english" else f"❌ त्रुटि: {str(e)}"
            )


# ── MAIN ─────────────────────────────────────────
def main():
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN .env mein nahi mila!")
        return

    print("🤖 RTIAssist Telegram Bot v2 starting...")
    print(f"🔗 API: {API_BASE}")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("fee", fee))
    app.add_handler(CommandHandler("state", state_cmd))
    app.add_handler(CommandHandler("legal", legal_cmd))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot LIVE! Ctrl+C to stop.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()