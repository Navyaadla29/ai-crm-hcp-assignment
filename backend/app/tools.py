 
def log_interaction_tool(hcp_name, date, topics):
    return {"message": f"Logged meeting with {hcp_name}", "id": 1}

def edit_interaction_tool(id, field, value):
    return {"message": f"Updated interaction {id}"}

def search_hcp_tool(query):
    return {"results": [f"Dr. {query}"]}

def schedule_followup_tool(hcp_name, days=14):
    return {"followup": f"In {days} days with {hcp_name}"}

def extract_sentiment_tool(text):
    return {"sentiment": "Positive"}
def process_chat_with_ai(message: str):
    return {
        "response": f"AI: I received '{message}'",
        "extracted_data": {},
        "tools_used": [],
        "logged_interaction": False
    }