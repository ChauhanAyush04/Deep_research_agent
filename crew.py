from crewai import Crew, Process
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # ⬅ add this

from config import OPENAI_API_KEY, SERPLY_API_KEY
import os

from agents import (
    topic_analyst, web_searcher, web_content_reader,
    paper_reader_agent, insight_agent, report_agent
)

from tasks import (
    analyze_topic_task, web_search_task, read_content_task,
    read_papers_task, synthesize_task, generate_report_task
)

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPLY_API_KEY"] = SERPLY_API_KEY

app = FastAPI(title="Research Agent API")

# 🟢 ADD CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or ["http://localhost:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],            # allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

research_crew = Crew(
    agents=[
        topic_analyst,
        web_searcher,
        web_content_reader,
        paper_reader_agent,
        insight_agent,
        report_agent
    ],
    tasks=[
        analyze_topic_task,
        web_search_task,
        read_content_task,
        read_papers_task,
        synthesize_task,
        generate_report_task
    ],
    verbose=True,
    process=Process.sequential,
    memory=False,
    cache=False,
    share_crew=True
)

@app.post("/research")
async def research_topic(request: ResearchRequest):
    try:
        result = research_crew.kickoff(inputs={"topic": request.topic})
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the Research Agent API. Use the /research endpoint to start a research task."}
