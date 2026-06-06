# Deep Research Agent

Deep Research Agent is a multi-agent AI research system that autonomously conducts in-depth research on user-defined topics. It leverages LangGraph-based agent orchestration, web search capabilities, and large language models to gather information, analyze sources, synthesize findings, and generate comprehensive research reports.

## Features

- **Multi-Agent Architecture for specialized research tasks**
- **Automated Topic Analysis and Research Planning**
- **Web Search Integration for real-time information retrieval**
- **Research Question Generation**
- **Information Synthesis and Summarization**
- **Comprehensive Report Generation**
- **LangGraph Workflow Orchestration**
- **Groq-Powered LLM Integration**
- **Structured and Data-Driven Research Outputs**

  
## Architecture

```text
User Query
    │
    ▼
Topic Analyzer Agent
    │
    ├── Research Questions
    ├── Research Topics
    │
    ▼
Research Coordinator
    │
    ├──────────────┬
    ▼              ▼          
Web Search    Paper Reader
Agent         Agent
    │              │
    └──────┬───────┘
           ▼
    Research Synthesizer
           │
           ▼
      Report Writer
           │
           ▼
     Final Research Report
```

## Project Structure

```text
Deep_research_agent/
│
├── agents/
│   ├── topic_analyzer.py
│   ├── web_search_agent.py
│   ├── paper_reader_agent.py
│   ├── research_synthesizer.py
│   └── report_writer.py
│
├── graphs/
│   └── workflow.py
│
├── tools/
│   ├── web_search.py
│   └── utilities.py
│
├── state/
│   └── agent_state.py
│
├── prompts/
│   ├── topic_analyzer.txt
│   ├── web_search_agent.txt
│   ├── paper_reader_agent.txt
│   └── report_writer.txt
│
├── main.py
├── config.py
├── requirements.txt
├── .env
└── README.md
```

## Prerequisites

- **Python 3.11+**
- **Groq API Key**
- **Internet connection for web search tools**

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ChauhanAyush04/Deep_research_agent.git
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_token_here
```

## Usage

ThinkScribe requires running both the backend API and frontend interface:

### Method 1: Manual Startup (Recommended for Development)

**Terminal 1 - Start the FastAPI Backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start the React Frontend:**
```bash
cd frontend
npm run dev
```

### Method 2: Production Deployment
```bash
# Backend (production mode)
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (in separate terminal)
npm run dev
```

### 3. Access the Application
- **Frontend Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000

### 4. Conduct Deep Research

1. Open the interface in your browser
2. Enter a research topic, question, or area of interest
3. Click "Research" to initiate the workflow
4. Review the comprehensive research report including:
   - Topic analysis and breakdown
   - Research questions and key themes
   - Web search findings
   - Synthesized insights and conclusions
   - References and supporting sources

## How It Works

Deep Research Agent employs a sophisticated multi-agent workflow:

1. **Input Processing**: User submits a research topic or query through the interface
2. **Topic Analysis**: The Topic Analyzer Agent identifies key concepts, research objectives, and subtopics
3. **Research Planning**: Research questions and investigation areas are generated automatically
4. **Information Gathering**: The Web Search Agent retrieves relevant information from online sources
5. **Knowledge Extraction**: Research findings are processed and structured for analysis
6. **Research Synthesis**: Insights from multiple sources are combined into a unified understanding
7. **Report Generation**: A comprehensive research report is generated and returned to the user

Each agent leverages specialized prompts and web search capabilities to ensure thorough, data-driven research.

### Workflow Strategy

- **Dynamic Routing**: Research tasks are distributed across specialized agents based on the query
- **Information Gathering**: Agents collect and analyze information from multiple sources
- **Shared State Management**: Findings are stored and exchanged between agents
- **Research Synthesis**: Information is consolidated into a coherent research report
- **Fallback Mechanisms**: The workflow continues even when certain tools or sources are unavailable

## Dependencies

### Core Framework

- **FastAPI**: High-performance API backend
- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: Agent tools and integrations

### AI & Research

- **Groq API**: Large Language Model inference
- **duckduckgo-search**: Real-time web search functionality
- **Pydantic**: Data validation and parsing

## API Endpoints

### POST /research

Conducts deep research on a given topic.

**Request Body:**

```json
{
  "query": "Impact of Artificial Intelligence on Healthcare"
}
```

**Response:**

```json
{
  "query": "Impact of Artificial Intelligence on Healthcare",
  "topic_analysis": "Breakdown of the research topic",
  "research_questions": [
    "What are the major applications of AI in healthcare?",
    "What challenges are associated with AI adoption?"
  ],
  "web_findings": "Collected information from web sources",
  "research_summary": "Key insights and findings",
  "final_report": "Comprehensive research report"
}
```

## Limitations & Considerations

- **API Dependencies**: Relies on Groq API and web search services
- **Rate Limits**: API usage may be subject to provider limitations
- **Search Quality**: Research quality depends on available online information
- **Response Time**: Complex research topics may require additional processing time
- **Source Reliability**: Users should independently verify critical information from generated reports
