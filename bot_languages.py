"""
RTIAssist Telegram Bot — Multi-language Support
UI Language Translations for Bot Messages
"""

# Supported UI languages
UI_LANGUAGES = {
    "hindi": "हिन्दी",
    "english": "English",
    "marathi": "मराठी",
    "tamil": "தமிழ்",
    "gujarati": "ગુજરાતી",
    "bengali": "বাংলা",
    "telugu": "తెలుగు",
    "kannada": "ಕನ್ನಡ"
}

# Supported draft languages
DRAFT_LANGUAGES = {
    "hindi": "हिन्दी",
    "english": "English",
    "marathi": "मराठी",
    "tamil": "தமிழ்",
    "gujarati": "ગુજરાતી",
    "bengali": "বাংলা",
    "telugu": "తెలుగు",
    "kannada": "ಕನ್ನಡ",
    "punjabi": "ਪੰਜਾਬੀ",
    "malayalam": "മലയാളം"
}

# Bot message translations
MESSAGES = {
    "english": {
        "choose_language": "🌐 *Choose Your Language*\n\nSelect the language you want to use for bot messages:",
        "language_set": "✅ Language set to: *{}*\n\n📝 Now tell me your problem in your own words.",
        "welcome": """🏛 *RTIAssist Bot — India's AI RTI Generator*

Hello! I will help you create RTI applications.

📝 *How to use:*
Type your problem directly — in Hindi or English.

*Example:*
_My ration card application was rejected 3 months ago in Maharashtra, no reason given_

💡 Mention the state name — I'll auto-detect it!
Or use /state to manually select.

━━━━━━━━━━━━━━━━
/start — This message
/state — Select state
/fee   — Filing fee
/legal — ⚖️ Legal Tools (New!)
/help  — Help
/about — About RTIAssist""",
        "problem_too_short": "📝 Please write in more detail!\n\n*Example:*\n_My ration card in Maharashtra was rejected 3 months ago_",
        "state_not_detected": "📍 *State not detected.*\n\nNo state name found in your message.\nPlease select your state from below:",
        "state_selected": "✅ State: *{}*\n\nGenerating RTI...",
        "confirm_category": "Is this correct? Click ✅ Confirm or 🔄 Change Category",
        "choose_draft_language": "📄 *In which language do you want your RTI draft?*\n\nSelect the document language:",
        "processing": """🔄 *Analyzing...*

📍 State: *{}*

⚙️ Layer 1: Identifying department...""",
        "generating": """🔄 *Generating draft...*

✅ Layer 1: Department identified
✅ Layer 2: PIO details found
✅ Layer 3: Draft ready
⚙️ Layer 4: Quality check...""",
        "rti_ready": """✅ *RTI Application Ready, {}!*

🏢 *Department:* {}
🏛 *Ministry:* {}
📍 *State:* {}
⚡ *Urgency:* {}

{} *Quality Score:* {}/100
📈 *Success Chance:* {}
⚠️ *Exempt Risk:* {}

📄 Draft coming below...""",
        "draft_label": "📄 *RTI Draft{}:*",
        "filing_instructions": "📋 *Filing Instructions:*",
        "action_message": "⬆️ *Copy the draft and file it!*\n\n🆓 RTIAssist — Completely Free",
        "file_online": "🔗 File Online Now",
        "generate_appeal": "📝 Generate Appeal",
        "fee_info": "💰 Fee Info",
        "new_rti": "🔄 New RTI",
        "server_error": "❌ *Could not connect to server.*\n\nRTIAssist API server is currently down.\nPlease try again later or use the website.",
        "error": "❌ *Error:* `{}`\n\nPlease try again later.",
        "help": """📚 *RTIAssist — Help*

*Step 1:* Type your problem
*Step 2:* Mention state or use /state
*Step 3:* Get draft in 30 seconds
*Step 4:* Copy → file at rtionline.gov.in

━━━━━━━━━━━━━━━━
⚖️ *Legal Tools (/legal):*
📝 Second Appeal (CIC)
🛒 Consumer Complaint
📜 Legal Notice
💼 Labour Complaint

━━━━━━━━━━━━━━━━
*Tips:*
✅ Write problem in detail
✅ Mention how long it's pending
✅ Include state name

🆓 RTIAssist is completely free!""",
        "about": """🏛 *RTIAssist — India's Most Powerful Free RTI Tool*

⚡ 4-Layer ASI-1 AI Pipeline
🌐 11 Indian Languages
📍 28+ States + UTs
📊 Quality Score 0-100
⚠️ Section 8 Exemption Risk Check
📝 Appeal Letter Generator
🆓 100% Free Forever

━━━━━━━━━━━━━━━━
👨‍💻 GitHub: github.com/shlok926/RTIASSIST-API""",
        "fee_details": """💰 *RTI Filing Fee — State-wise*

🏛 Central Govt: *₹10*
🏙️ Most States: *₹10*
🔶 Gujarat: *₹20*

━━━━━━━━━━━━━━━━
📋 *Payment Methods:*
• Indian Postal Order (IPO)
• Court Fee Stamp
• Demand Draft (DD)
• Online (on state portals)

✅ *BPL applicants — ZERO fee*
_Attach BPL card copy_

🔗 File at: rtionline.gov.in"""
    },
    "hindi": {
        "choose_language": "🌐 *अपनी भाषा चुनें*\n\nबॉट के संदेशों के लिए भाषा चुनें:",
        "language_set": "✅ भाषा सेट: *{}*\n\n📝 अब अपनी समस्या अपने शब्दों में बताएं।",
        "welcome": """🏛 *RTIAssist Bot — भारत का AI RTI जनरेटर*

नमस्ते! मैं आपकी RTI आवेदन बनाने में मदद करूंगा।

📝 *कैसे उपयोग करें:*
अपनी समस्या सीधे लिखें — हिन्दी या अंग्रेजी में।

*उदाहरण:*
_मेरा राशन कार्ड महाराष्ट्र में 3 महीने से रिजेक्ट है, कोई कारण नहीं बताया_

💡 राज्य का नाम लिखें — मैं ऑटो-डिटेक्ट कर लूंगा!
या /state से मैन्युअल चुनें।

━━━━━━━━━━━━━━━━
/start — यह संदेश
/state — राज्य चुनें
/fee   — फाइलिंग फीस
/legal — ⚖️ कानूनी टूल्स (नया!)
/help  — मदद
/about — RTIAssist के बारे में""",
        "problem_too_short": "📝 थोड़ा और विस्तार से लिखें!\n\n*उदाहरण:*\n_मेरा राशन कार्ड महाराष्ट्र में 3 महीने से रिजेक्ट है_",
        "state_not_detected": "📍 *राज्य पता नहीं चल पाया।*\n\nआपके संदेश में राज्य का नाम नहीं था।\nनीचे से अपना राज्य चुनें:",
        "state_selected": "✅ राज्य: *{}*\n\nRTI जनरेट हो रही है...",
        "confirm_category": "📍 *पहचाना गया राज्य:* {}\n📂 *पहचानी गई श्रेणी:* {}\n\n✅ क्या यह सही है?",
        "choose_draft_language": "📄 *RTI ड्राफ्ट किस भाषा में चाहिए?*\n\nदस्तावेज़ की भाषा चुनें:",
        "processing": """🔄 *विश्लेषण हो रहा है...*

📍 राज्य: *{}*

⚙️ Layer 1: विभाग पहचान रहा हूं...""",
        "generating": """🔄 *ड्राफ्ट बन रहा है...*

✅ Layer 1: विभाग पहचाना गया
✅ Layer 2: PIO विवरण मिला
✅ Layer 3: ड्राफ्ट तैयार
⚙️ Layer 4: क्वालिटी चेक...""",
        "rti_ready": """✅ *RTI आवेदन तैयार, {}!*

🏢 *विभाग:* {}
🏛 *मंत्रालय:* {}
📍 *राज्य:* {}
⚡ *तात्कालिकता:* {}

{} *क्वालिटी स्कोर:* {}/100
📈 *सफलता की संभावना:* {}
⚠️ *छूट जोखिम:* {}

📄 ड्राफ्ट नीचे आ रहा है...""",
        "draft_label": "📄 *RTI ड्राफ्ट{}:*",
        "filing_instructions": "📋 *फाइलिंग निर्देश:*",
        "action_message": "⬆️ *ड्राफ्ट कॉपी करें और फाइल करें!*\n\n🆓 RTIAssist — बिल्कुल मुफ्त",
        "file_online": "🔗 अभी ऑनलाइन फाइल करें",
        "generate_appeal": "📝 अपील जनरेट करें",
        "fee_info": "💰 फीस जानकारी",
        "new_rti": "🔄 नया RTI",
        "server_error": "❌ *सर्वर से कनेक्ट नहीं हो पाया।*\n\nRTIAssist API सर्वर अभी बंद है।\nथोड़ी देर बाद कोशिश करें या वेबसाइट उपयोग करें।",
        "error": "❌ *त्रुटि:* `{}`\n\nथोड़ी देर बाद दोबारा कोशिश करें।",
        "help": """📚 *RTIAssist — मदद*

*स्टेप 1:* अपनी समस्या लिखें
*स्टेप 2:* राज्य का नाम लिखें या /state से चुनें
*स्टेप 3:* 30 सेकंड में ड्राफ्ट पाएं
*स्टेप 4:* कॉपी करें → rtionline.gov.in पर फाइल करें

━━━━━━━━━━━━━━━━
⚖️ *कानूनी टूल्स (/legal):*
📝 द्वितीय अपील (CIC)
🛒 उपभोक्ता शिकायत
📜 कानूनी नोटिस
💼 श्रम शिकायत

━━━━━━━━━━━━━━━━
*टिप्स:*
✅ समस्या विस्तार से लिखें
✅ कितने समय से पेंडिंग है बताएं
✅ राज्य का नाम ज़रूर हो

🆓 RTIAssist बिल्कुल मुफ्त है!""",
        "about": """🏛 *RTIAssist — भारत का सबसे शक्तिशाली मुफ्त RTI टूल*

⚡ 4-Layer ASI-1 AI Pipeline
🌐 11 भारतीय भाषाएं
📍 28+ राज्य + केंद्र शासित प्रदेश
📊 क्वालिटी स्कोर 0-100
⚠️ धारा 8 छूट जोखिम जांच
📝 अपील पत्र जनरेटर
🆓 100% हमेशा मुफ्त

━━━━━━━━━━━━━━━━
👨‍💻 GitHub: github.com/shlok926/RTIASSIST-API""",
        "fee_details": """💰 *RTI फाइलिंग फीस — राज्यवार*

🏛 केंद्र सरकार: *₹10*
🏙️ अधिकांश राज्य: *₹10*
🔶 गुजरात: *₹20*

━━━━━━━━━━━━━━━━
📋 *भुगतान के तरीके:*
• भारतीय डाक ऑर्डर (IPO)
• कोर्ट फीस स्टाम्प
• डिमांड ड्राफ्ट (DD)
• ऑनलाइन (राज्य पोर्टल पर)

✅ *BPL आवेदक — शून्य फीस*
_BPL कार्ड की कॉपी संलग्न करें_

🔗 फाइल करें: rtionline.gov.in"""
    },
    "marathi": {
        "choose_language": "🌐 *तुमची भाषा निवडा*\n\nबॉट संदेशांसाठी भाषा निवडा:",
        "language_set": "✅ भाषा सेट: *{}*\n\n📝 आता तुमची समस्या तुमच्या शब्दांत सांगा।",
        "welcome": """🏛 *RTIAssist Bot — भारताचा AI RTI जनरेटर*

नमस्कार! मी तुम्हाला RTI अर्ज तयार करण्यात मदत करेन।

📝 *कसे वापरायचे:*
तुमची समस्या थेट लिहा — मराठी किंवा इंग्रजीत।

*उदाहरण:*
_माझे रेशन कार्ड महाराष्ट्रात 3 महिन्यांपासून रिजेक्ट आहे, कारण सांगितले नाही_

💡 राज्याचे नाव लिहा — मी ऑटो-डिटेक्ट करेन!
किंवा /state वरून मॅन्युअल निवडा।

━━━━━━━━━━━━━━━━
/start — हा संदेश
/state — राज्य निवडा
/fee   — फाइलिंग फी
/legal — ⚖️ कायदेशीर साधने (नवीन!)
/help  — मदत
/about — RTIAssist बद्दल""",
        "problem_too_short": "📝 कृपया अधिक तपशीलात लिहा!\n\n*उदाहरण:*\n_माझे रेशन कार्ड महाराष्ट्रात 3 महिन्यांपासून रिजेक्ट आहे_",
        "state_not_detected": "📍 *राज्य शोधले जाऊ शकले नाही।*\n\nतुमच्या संदेशात राज्याचे नाव नव्हते।\nकृपया खालून तुमचे राज्य निवडा:",
        "state_selected": "✅ राज्य: *{}*\n\nRTI तयार होत आहे...",
        "confirm_category": "📍 *ओळखले गेलेले राज्य:* {}\n📂 *ओळखली गेलेली श्रेणी:* {}\n\n✅ हे बरोबर आहे का?",
        "choose_draft_language": "📄 *RTI ड्राफ्ट कोणत्या भाषेत हवा?*\n\nदस्तऐवजाची भाषा निवडा:",
        "processing": """🔄 *विश्लेषण होत आहे...*

📍 राज्य: *{}*

⚙️ Layer 1: विभाग ओळखत आहे...""",
        "generating": """🔄 *ड्राफ्ट तयार होत आहे...*

✅ Layer 1: विभाग ओळखला
✅ Layer 2: PIO तपशील मिळाले
✅ Layer 3: ड्राफ्ट तयार
⚙️ Layer 4: गुणवत्ता तपासणी...""",
        "rti_ready": """✅ *RTI अर्ज तयार, {}!*

🏢 *विभाग:* {}
🏛 *मंत्रालय:* {}
📍 *राज्य:* {}
⚡ *तातडीचे:* {}

{} *गुणवत्ता स्कोअर:* {}/100
📈 *यशाची शक्यता:* {}
⚠️ *सूट जोखीम:* {}

📄 ड्राफ्ट खाली येत आहे...""",
        "draft_label": "📄 *RTI ड्राफ्ट{}:*",
        "filing_instructions": "📋 *फाइलिंग सूचना:*",
        "action_message": "⬆️ *ड्राफ्ट कॉपी करा आणि फाइल करा!*\n\n🆓 RTIAssist — पूर्णपणे मोफत",
        "file_online": "🔗 आता ऑनलाइन फाइल करा",
        "generate_appeal": "📝 अपील तयार करा",
        "fee_info": "💰 फी माहिती",
        "new_rti": "🔄 नवीन RTI",
        "server_error": "❌ *सर्व्हरशी कनेक्ट होऊ शकले नाही।*\n\nRTIAssist API सर्व्हर सध्या बंद आहे।\nकृपया थोड्या वेळाने प्रयत्न करा किंवा वेबसाइट वापरा।",
        "error": "❌ *त्रुटी:* `{}`\n\nकृपया थोड्या वेळाने पुन्हा प्रयत्न करा।",
        "help": """📚 *RTIAssist — मदत*

*पायरी 1:* तुमची समस्या लिहा
*पायरी 2:* राज्याचे नाव लिहा किंवा /state वरून निवडा
*पायरी 3:* 30 सेकंदात ड्राफ्ट मिळवा
*पायरी 4:* कॉपी करा → rtionline.gov.in वर फाइल करा

━━━━━━━━━━━━━━━━
*टिपा:*
✅ समस्या तपशीलात लिहा
✅ किती काळापासून प्रलंबित आहे ते सांगा
✅ राज्याचे नाव नक्की असावे

🆓 RTIAssist पूर्णपणे मोफत आहे!""",
        "about": """🏛 *RTIAssist — भारतातील सर्वात शक्तिशाली मोफत RTI टूल*

⚡ 4-Layer ASI-1 AI Pipeline
🌐 11 भारतीय भाषा
📍 28+ राज्ये + केंद्रशासित प्रदेश
📊 गुणवत्ता स्कोअर 0-100
⚠️ कलम 8 सूट जोखीम तपासणी
📝 अपील पत्र जनरेटर
🆓 100% कायमचे मोफत

━━━━━━━━━━━━━━━━
👨‍💻 GitHub: github.com/shlok926/RTIASSIST-API""",
        "fee_details": """💰 *RTI फाइलिंग फी — राज्यनिहाय*

🏛 केंद्र सरकार: *₹10*
🏙️ बहुतेक राज्ये: *₹10*
🔶 गुजरात: *₹20*

━━━━━━━━━━━━━━━━
📋 *पेमेंट पद्धती:*
• भारतीय डाक ऑर्डर (IPO)
• कोर्ट फी स्टॅम्प
• डिमांड ड्राफ्ट (DD)
• ऑनलाइन (राज्य पोर्टलवर)

✅ *BPL अर्जदार — शून्य फी*
_BPL कार्ड प्रत जोडा_

🔗 फाइल करा: rtionline.gov.in"""
    },
    "tamil": {
        "choose_language": "🌐 *உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்*\n\nபாட் செய்திகளுக்கு மொழியைத் தேர்ந்தெடுக்கவும்:",
        "language_set": "✅ மொழி அமைக்கப்பட்டது: *{}*\n\n📝 இப்போது உங்கள் பிரச்சனையை உங்கள் சொந்த வார்த்தைகளில் சொல்லுங்கள்।",
        "welcome": """🏛 *RTIAssist Bot — இந்தியாவின் AI RTI ஜெனரேட்டர்*

வணக்கம்! RTI விண்ணப்பங்களை உருவாக்க நான் உங்களுக்கு உதவுவேன்.

📝 *எப்படி பயன்படுத்துவது:*
உங்கள் பிரச்சனையை நேரடியாக எழுதுங்கள் — தமிழ் அல்லது ஆங்கிலத்தில்.

*உதாரணம்:*
_என் ரேஷன் கார்டு விண்ணப்பம் தமிழகத்தில் 3 மாதங்களாக நிராகரிக்கப்பட்டுள்ளது, காரணம் சொல்லவில்லை_

💡 மாநில பெயரை குறிப்பிடுங்கள் — நான் தானாக கண்டுபிடிப்பேன்!
அல்லது /state மூலம் கைமுறையாக தேர்ந்தெடுக்கவும்.

━━━━━━━━━━━━━━━━
/start — இந்த செய்தி
/state — மாநிலம் தேர்ந்தெடு
/fee   — தாக்கல் கட்டணம்
/legal — ⚖️ சட்ட கருவிகள் (புதியது!)
/help  — உதவி
/about — RTIAssist பற்றி""",
        "problem_too_short": "📝 இன்னும் விரிவாக எழுதுங்கள்!\n\n*உதாரணம்:*\n_என் ரேஷன் கார்டு தமிழகத்தில் 3 மாதங்களாக நிராகரிக்கப்பட்டுள்ளது_",
        "state_not_detected": "📍 *மாநிலம் கண்டறியப்படவில்லை.*\n\nஉங்கள் செய்தியில் மாநில பெயர் இல்லை.\nகீழே இருந்து உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும்:",
        "state_selected": "✅ மாநிலம்: *{}*\n\nRTI உருவாக்கப்படுகிறது...",
        "confirm_category": "📍 *கண்டறியப்பட்ட மாநிலம்:* {}\n📂 *கண்டறியப்பட்ட வகை:* {}\n\n✅ இது சரியானதா?",
        "choose_draft_language": "📄 *RTI வரைவு எந்த மொழியில் வேண்டும்?*\n\nஆவண மொழியைத் தேர்ந்தெடுக்கவும்:",
        "processing": """🔄 *பகுப்பாய்வு செய்யப்படுகிறது...*

📍 மாநிலம்: *{}*

⚙️ Layer 1: துறையை அடையாளம் காண்கிறது...""",
        "generating": """🔄 *வரைவு உருவாக்கப்படுகிறது...*

✅ Layer 1: துறை அடையாளம் காணப்பட்டது
✅ Layer 2: PIO விவரங்கள் கிடைத்தன
✅ Layer 3: வரைவு தயார்
⚙️ Layer 4: தரச் சரிபார்ப்பு...""",
        "rti_ready": """✅ *RTI விண்ணப்பம் தயார், {}!*

🏢 *துறை:* {}
🏛 *அமைச்சகம்:* {}
📍 *மாநிலம்:* {}
⚡ *அவசரம்:* {}

{} *தர மதிப்பெண்:* {}/100
📈 *வெற்றி வாய்ப்பு:* {}
⚠️ *விலக்கு ஆபத்து:* {}

📄 வரைவு கீழே வருகிறது...""",
        "draft_label": "📄 *RTI வரைவு{}:*",
        "filing_instructions": "📋 *தாக்கல் வழிமுறைகள்:*",
        "action_message": "⬆️ *வரைவை நகலெடுத்து தாக்கல் செய்யுங்கள்!*\n\n🆓 RTIAssist — முற்றிலும் இலவசம்",
        "file_online": "🔗 இப்போது ஆன்லைனில் தாக்கல் செய்யுங்கள்",
        "generate_appeal": "📝 மேல்முறையீடு உருவாக்கு",
        "fee_info": "💰 கட்டண தகவல்",
        "new_rti": "🔄 புதிய RTI",
        "server_error": "❌ *சர்வருடன் இணைக்க முடியவில்லை.*\n\nRTIAssist API சேவையகம் தற்போது செயலிழந்துள்ளது.\nபிறகு முயற்சிக்கவும் அல்லது இணையதளத்தைப் பயன்படுத்தவும்.",
        "error": "❌ *பிழை:* `{}`\n\nபிறகு மீண்டும் முயற்சிக்கவும்.",
        "help": """📚 *RTIAssist — உதவி*

*படி 1:* உங்கள் பிரச்சனையை எழுதுங்கள்
*படி 2:* மாநில பெயரைக் குறிப்பிடுங்கள் அல்லது /state பயன்படுத்துங்கள்
*படி 3:* 30 விநாடிகளில் வரைவைப் பெறுங்கள்
*படி 4:* நகலெடுக்கவும் → rtionline.gov.in இல் தாக்கல் செய்யுங்கள்

━━━━━━━━━━━━━━━━
⚖️ *சட்ட கருவிகள் (/legal):*
📝 இரண்டாம் மேல்முறையீடு (CIC)
🛒 நுகர்வோர் புகார்
📜 சட்ட அறிவிப்பு
💼 தொழில் புகார்

━━━━━━━━━━━━━━━━
*குறிப்புகள்:*
✅ பிரச்சனையை விரிவாக எழுதுங்கள்
✅ எவ்வளவு காலமாக நிலுவையில் உள்ளது என்பதைக் குறிப்பிடுங்கள்
✅ மாநில பெயர் இருக்க வேண்டும்

🆓 RTIAssist முற்றிலும் இலவசமானது!""",
        "about": """🏛 *RTIAssist — இந்தியாவின் மிக சக்திவாய்ந்த இலவச RTI கருவி*

⚡ 4-Layer ASI-1 AI Pipeline
🌐 11 இந்திய மொழிகள்
📍 28+ மாநிலங்கள் + யூனியன் பிரதேசங்கள்
📊 தரம் மதிப்பெண் 0-100
⚠️ பிரிவு 8 விலக்கு ஆபத்து சரிபார்ப்பு
📝 மேல்முறையீடு கடிதம் உருவாக்கி
🆓 100% என்றும் இலவசம்

━━━━━━━━━━━━━━━━
👨‍💻 GitHub: github.com/shlok926/RTIASSIST-API""",
        "fee_details": """💰 *RTI தாக்கல் கட்டணம் — மாநிலவாரியாக*

🏛 மத்திய அரசு: *₹10*
🏙️ பெரும்பாலான மாநிலங்கள்: *₹10*
🔶 குஜராத்: *₹20*

━━━━━━━━━━━━━━━━
📋 *கட்டண முறைகள்:*
• இந்திய அஞ்சல் ஆணை (IPO)
• நீதிமன்ற கட்டண முத்திரை
• டிமாண்ட் டிராஃப்ட் (DD)
• ஆன்லைன் (மாநில போர்ட்டல்களில்)

✅ *BPL விண்ணப்பதாரர்கள் — சுழிய கட்டணம்*
_BPL அட்டை நகலை இணைக்கவும்_

🔗 தாக்கல் செய்யுங்கள்: rtionline.gov.in"""
    }
}

def get_message(lang_code: str, key: str, *args) -> str:
    """Get translated message for given language and key"""
    lang = MESSAGES.get(lang_code, MESSAGES["english"])
    message = lang.get(key, MESSAGES["english"][key])
    if args:
        return message.format(*args)
    return message

def get_language_keyboard(lang_type="ui"):
    """Generate language selection keyboard"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    languages = UI_LANGUAGES if lang_type == "ui" else DRAFT_LANGUAGES
    
    # Create rows of 2 languages each
    rows = []
    items = list(languages.items())
    for i in range(0, len(items), 2):
        row = []
        for code, name in items[i:i+2]:
            callback_data = f"{lang_type}lang_{code}"
            row.append(InlineKeyboardButton(name, callback_data=callback_data))
        rows.append(row)
    
    return InlineKeyboardMarkup(rows)
