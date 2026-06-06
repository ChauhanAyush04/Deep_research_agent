from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Literal
from state.agent_state import AgentState
from models.chat_model import chat_model
from config import TOPIC_UNDERSTANDING_PROMPT_PATH
import json

class TopicAnalysis(BaseModel):
    """Structured output from Topic Analyzer"""
    research_questions: List[str] = Field(description="Questions for web search (5-7 questions)")
    research_topics: List[str] = Field(description="Topics for academic paper search (5-7 topics)")

parser = JsonOutputParser(pydantic_object=TopicAnalysis)

def analyze_topic(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    """
    Topic Analyzer Agent
    
    Purpose: Understand user's research request and convert it into:
    1. Research questions (for Web Search Agent)
    2. Research topics (for Paper Reader Agent)
    
    Input: User's research topic
    Output: research_questions and research_topics (as structured lists)
    """
    
    def topic_agent(state: AgentState) -> AgentState:
        try:
            with open(TOPIC_UNDERSTANDING_PROMPT_PATH, 'r') as f:
                template = f.read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file missing at {TOPIC_UNDERSTANDING_PROMPT_PATH}")

        prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=template,
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        chain = prompt_template | chat_model | parser

        try:
            response = chain.invoke({"topic": state["topic"]})
            
            return {
                "research_questions": response.get("research_questions", []),
                "research_topics": response.get("research_topics", [])
            # Remove: "messages": state.get("messages", [])
}
        except Exception as e:
            print(f"Error in Topic Analyzer: {e}")
            raise ValueError(f"Error analyzing topic: {e}")

    return topic_agent