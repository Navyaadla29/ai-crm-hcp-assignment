from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import tools from our tools module
from tools import (
    log_interaction_tool,
    edit_interaction_tool,
    search_hcp_tool,
    schedule_followup_tool,
    extract_sentiment_tool
)

# Simple chat processor
def process_chat_with_ai(message: str):
    return {
        "response": f"🤖 AI: I received your message: '{message}'. In a full implementation, this would use LangGraph with Groq LLM.",
        "extracted_data": {"hcp": "Dr. Demo", "sentiment": "Positive", "topics": ["demo"]},
        "tools_used": ["chat_processor"],
        "logged_interaction": False
    }

app = FastAPI(
    title="AI-First CRM HCP Module API",
    description="Healthcare Professional Interaction Logging System with AI",
    version="1.0.0"
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATA MODELS ==========
class InteractionData(BaseModel):
    hcp_name: str
    interaction_type: str = "Meeting"
    date: str
    time: str
    attendees: List[str] = []
    topics: List[str] = []
    sentiment: str = "Neutral"
    outcomes: str = ""
    follow_up_actions: str = ""
    materials_shared: List[str] = []
    samples_distributed: List[str] = []

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class EditRequest(BaseModel):
    interaction_id: int
    field: str
    new_value: Any

# ========== DATABASE SIMULATION ==========
interactions_db = []
hcp_database = [
    {"id": 1, "name": "Dr. Rajesh Sharma", "specialty": "Oncology", "hospital": "AIIMS Delhi"},
    {"id": 2, "name": "Dr. Priya Patel", "specialty": "Cardiology", "hospital": "Apollo Mumbai"},
    {"id": 3, "name": "Dr. Amit Kumar", "specialty": "Neurology", "hospital": "Fortis Bangalore"},
    {"id": 4, "name": "Dr. Sneha Reddy", "specialty": "Oncology", "hospital": "Yashoda Hyderabad"},
]

# ========== API ENDPOINTS ==========
@app.get("/")
def home():
    return {
        "message": "AI-First CRM HCP Module API",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": [
            "/log-interaction (POST)",
            "/chat (POST)", 
            "/tools/demo (GET)",
            "/interactions (GET)",
            "/hcps (GET)"
        ]
    }

@app.post("/log-interaction")
def log_interaction_form(data: InteractionData):
    """Form-based interaction logging"""
    try:
        # Use LangGraph tool to log interaction
        tool_result = log_interaction_tool(
            hcp_name=data.hcp_name,
            interaction_type=data.interaction_type,
            date=data.date,
            time=data.time,
            topics=data.topics,
            sentiment=data.sentiment,
            outcomes=data.outcomes,
            follow_up_actions=data.follow_up_actions
        )
        
        # Store in database
        interaction = {
            "id": len(interactions_db) + 1,
            **data.dict(),
            "ai_summary": "AI summary would appear here with full LLM integration",
            "ai_extracted": {"demo": "data"},
            "timestamp": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        interactions_db.append(interaction)
        
        return {
            "success": True,
            "message": "Interaction logged successfully",
            "interaction_id": interaction["id"],
            "ai_summary": "Demo: AI would summarize this interaction",
            "ai_suggestions": [
                f"Schedule follow-up meeting with {data.hcp_name} in 2 weeks",
                "Send product brochure PDF via email",
                f"Add {data.hcp_name} to advisory board invite list",
                "Share clinical trial data in next meeting"
            ],
            "extracted_data": {"demo": "With Groq LLM, entities would be extracted here"}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging interaction: {str(e)}")

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Chat interface with AI agent (LangGraph)"""
    try:
        response = process_chat_with_ai(request.message)
        return {
            "success": True,
            "response": response["response"],
            "extracted_data": response.get("extracted_data", {}),
            "tools_used": response.get("tools_used", []),
            "logged_interaction": response.get("logged_interaction", False)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

@app.post("/edit-interaction")
def edit_interaction(data: EditRequest):
    """Edit an existing interaction"""
    try:
        result = edit_interaction_tool(
            interaction_id=data.interaction_id,
            field=data.field,
            new_value=data.new_value
        )
        
        if result.get("success") and data.interaction_id <= len(interactions_db):
            # Update in our database
            if data.interaction_id - 1 < len(interactions_db):
                interactions_db[data.interaction_id - 1][data.field] = data.new_value
                interactions_db[data.interaction_id - 1]["last_modified"] = datetime.now().isoformat()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error editing interaction: {str(e)}")

@app.get("/tools/demo")
def demo_all_tools():
    """Demonstrate all 5 LangGraph tools"""
    results = []
    
    # Tool 1: Log Interaction
    results.append({
        "tool": "log_interaction",
        "description": "Logs HCP meetings with AI summarization",
        "result": log_interaction_tool(
            hcp_name="Dr. Sharma",
            date="2025-04-19",
            topics=["OncoBoost Phase III results", "Side effect management"]
        )
    })
    
    # Tool 2: Edit Interaction
    results.append({
        "tool": "edit_interaction",
        "description": "Modifies logged interaction data",
        "result": edit_interaction_tool(
            id=1,
            field="sentiment",
            value="Very Positive"
        )
    })
    
    # Tool 3: Search HCP
    results.append({
        "tool": "search_hcp",
        "description": "Searches HCP database",
        "result": search_hcp_tool(query="Sharma")
    })
    
    # Tool 4: Schedule Follow-up
    results.append({
        "tool": "schedule_followup",
        "description": "Creates follow-up tasks",
        "result": schedule_followup_tool(
            hcp_name="Dr. Sharma",
            days=14
        )
    })
    
    # Tool 5: Extract Sentiment
    results.append({
        "tool": "extract_sentiment",
        "description": "Uses LLM to analyze sentiment",
        "result": extract_sentiment_tool(
            text="The doctor was extremely enthusiastic about our new oncology drug."
        )
    })
    
    return {
        "message": "✅ 5 LangGraph Tools Demonstration",
        "tools_count": 5,
        "tools": results,
        "note": "With full implementation, these tools would use Groq LLM via LangGraph"
    }

@app.get("/interactions")
def get_interactions():
    """Get all logged interactions"""
    return {
        "count": len(interactions_db),
        "interactions": interactions_db
    }

@app.get("/hcps")
def get_hcps(search: Optional[str] = None):
    """Get HCP list, optionally filtered by search"""
    if search:
        filtered = [hcp for hcp in hcp_database if search.lower() in hcp["name"].lower()]
        return {"hcps": filtered}
    return {"hcps": hcp_database}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.12.7",
        "components": {
            "fastapi": "operational",
            "langgraph_tools": "operational (5 tools)",
            "database": "simulated",
            "groq_llm": "configured" if os.getenv("GROQ_API_KEY") else "not configured"
        }
    }

# ========== RUN SERVER ==========
if __name__ == "__main__":
    print("🚀 Starting AI-First CRM HCP Module API...")
    print(f"📚 API Documentation: http://localhost:8001/docs")
    print(f"🌐 Health Check: http://localhost:8001/health")
    print(f"🛠️  Tools Demo: http://localhost:8001/tools/demo")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)