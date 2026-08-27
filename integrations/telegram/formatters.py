def format_case_summary(case):
    status_emoji = {
        "UNDERSTANDING": "🤔",
        "ACTION_RECOMMENDED": "💡",
        "ACTION_CONFIRMED": "✅",
        "AUTHORITY_RESOLVED": "🏛",
        "DRAFT_GENERATED": "📄",
        "READY_TO_FILE": "📤",
        "FILED": "📬",
        "RESPONSE_RECEIVED": "📥",
        "ANALYSIS_READY": "🔍",
        "FIRST_APPEAL": "📝",
        "CLOSED": "🔒"
    }
    emoji = status_emoji.get(case.status, "📋")
    
    return f"{emoji} *Case ID:* `{case.id[:8]}`\n*Title:* {case.title}\n*Status:* {case.status}\n*Problem:* {case.problem_description[:100]}..."

def format_action_recommendation(rec):
    msg = f"💡 *Action Recommended:* {rec.primary_action}\n\n*Reason:* {rec.reasoning}"
    if rec.clarification_needed:
        msg += f"\n\n❓ *Clarification Needed:* {rec.clarification_questions}"
    return msg

def format_response_analysis(analysis):
    msg = f"🔍 *Response Analysis*\n\n"
    msg += f"*Status:* {analysis.analysis_status}\n"
    msg += f"*Overall Assessment:* {analysis.overall_assessment}\n\n"
    
    msg += "*Answered:* \n"
    for a in analysis.answered_points:
        msg += f"✅ {a}\n"
        
    msg += "\n*Not Answered:* \n"
    for n in analysis.unanswered_points:
        msg += f"❌ {n}\n"
        
    if analysis.recommended_next_steps:
        msg += "\n*Recommended Next Steps:* \n"
        for r in analysis.recommended_next_steps:
            msg += f"👉 {r}\n"
            
    return msg
