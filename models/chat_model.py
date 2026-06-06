import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from tools.web_search_tool import web_search
from config import TEMPERATURE, MAX_NEW_TOKENS

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Use Groq model
chat_model = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

tools_list = [web_search]

# Equivalent of bind_tools
llm_with_tools = chat_model.bind_tools(tools_list)
