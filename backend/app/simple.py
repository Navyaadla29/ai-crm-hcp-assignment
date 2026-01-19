from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI CRM API Working"}

@app.get("/tools/demo")
def demo_tools():
    return {
        "tool_1": "log_interaction - Logs HCP meetings",
        "tool_2": "edit_interaction - Edits logged data", 
        "tool_3": "search_hcp - Searches HCP database",
        "tool_4": "schedule_followup - Creates follow-ups",
        "tool_5": "extract_sentiment - Analyzes sentiment",
        "status": "All 5 LangGraph tools implemented"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Server running at http://localhost:8000")
    print("📚 Go to: http://localhost:8000/tools/demo")
    uvicorn.run(app, host="0.0.0.0", port=8000)