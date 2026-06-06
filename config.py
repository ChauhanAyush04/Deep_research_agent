import os
from dotenv import load_dotenv
# URL
BASE_URL = "http://localhost:8000"

# Chat model
REPO_ID = "openai/gpt-oss-120b"
TEMPERATURE = 0.7
MAX_NEW_TOKENS = 512

# Prompts paths
TOPIC_UNDERSTANDING_PROMPT_PATH = os.path.join("prompts", "topic_analyzer.txt")
WEB_SEARCH_PROMPT_PATH = os.path.join("prompts", "web_search.txt")
READ_PAPER_PROMPT_PATH = os.path.join("prompts", "read_paper.txt")
WRITER_PROMPT_PATH = os.path.join("prompts", "writer.txt")

# Graph and reports
REPORTS_PATH = "reports"
GRAPH_VISUALIZATION_PATH = os.path.join(REPORTS_PATH, "research_agent_graph.png")

# Research workflow fields
RESEARCH_FIELDS = ["topic_analysis", "web_search_results", "paper_analysis", "final_report"]
