from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from graphs.workflow import build_graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
graph = build_graph()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ResearchTopic(BaseModel):
    research_topic: Annotated[str, Field(...)]


@app.post("/validate")
async def validate_research_topic(idea: ResearchTopic):
    try:
        result = await graph.ainvoke(
    {
        "topic": idea.research_topic,
        "research_questions": None,
        "research_topics": None,
        "web_findings": None,
        "top_5_papers": None,
        "final_report": None,
        "messages": []
    },
    config={"recursion_limit": 100} 
)

        print("Research completed successfully for topic :- ", idea.research_topic)
        result.pop("messages", None)
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        print("Error :- ", e)
        raise HTTPException(status_code=400, detail=str(e))
