from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    State model for the multi-agent research system.
    
    Flow:
    topic → Topic Analyzer → research_questions + research_topics
         ↓
         ├→ Web Search Agent → web_findings
         ├→ Paper Reader Agent → top_5_papers
         ↓
         Writer Agent → final_report
    """
    # Input
    topic: str
    
    # Topic Analyzer outputs
    research_questions: Optional[List[str]]
    research_topics: Optional[List[str]]
    web_findings: Optional[List[dict]]
    top_5_papers: Optional[List[dict]]
    final_report: Optional[str]
    messages: List[BaseMessage]