# ThinkScribe - Startup Idea Validation Tool

A comprehensive AI-powered platform that validates startup ideas through Idea Understanding,  intelligent market analysis, competitor research, risk assessment, SWOT analysis and strategic advice. Built with FastAPI backend and React frontend, It uses LangGraph workflows and advanced language models to provide data-driven insights for entrepreneurs.

## Features

- **AI-Powered Market Analysis**: Deep market insights
- **Competitive Intelligence**: Automated competitor research and positioning analysis  
- **Risk Assessment**: Multi-dimensional risk evaluation across market, technical, operational, regulatory, and financial factors
- **SWOT Analysis**: Actionable SWOT( Strengths , weaknesses, opportunities, Threats) analysis that product teams and founders can act on.
- **Strategic Advisory**: Go/No-Go recommendations with actionable next steps
- **Web Search Integration**: Real-time market data via DuckDuckGo, invoked through a tool-enabled flow with robust fallbacks
- **Workflow Orchestration**: LangGraph-powered, tools-first agent coordination with automatic fallbacks
- **User-Friendly Interface**: Clean React web interface for easy interaction

##  Architecture

Follows a modular microservices architecture with clear separation of concerns:

```
├── main.py                     # FastAPI backend server
├── app.py                      # Streamlit frontend application
├── config.py                   # Configuration and model parameters
├── graphs/
│   └── workflow.py            # LangGraph workflow orchestration
├── nodes/                     # Analysis agents
│   ├── idea_understanding.py  # understanding the idea properly
│   ├── market_analyst.py      # Market analysis agent
│   ├── competitor_analysis.py # Competitor research agent
│   ├── risk_assessor.py       # Risk assessment agent
│   ├── swot_analysis.py       # SWOT Analysis
│   └── advisor.py             # Strategic advisor agent
├── state/
│   └── agent_state.py         # Shared state management
├── models/
│   └── chat_model.py          # Hugging Face model configuration
├── tools/
│   └── web_search_tool.py     # DuckDuckGo search integration
└── prompts/                   # Agent-specific prompts
    ├── idea_understanding.txt
    ├── market_analyst.txt
    ├── competitor_analyst_prompt.txt
    ├── risk_assessor.txt
    ├── swot_analysis.txt
    └── advisor.txt
```

## Prerequisites

- **Python 3.11+**
- **Google Gemini API Token** (for the configured Gemini model)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Devanshu1609/AI-Powered-Startup-Market-Research
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
GOOGLE_API_KEY=your_google_api_token_here
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

### 4. Validate Your Startup Idea
1. Open the interface in your browser
2. Enter your startup idea in the text area
3. Click "Validate" to initiate the analysis
4. Review the comprehensive validation report including:
   - Market analysis and opportunities
   - Competitive landscape assessment
   - Risk evaluation and mitigation strategies  
   - Strategic recommendations and next steps
   - SWOT Analysis

## How It Works

ThinkScribe employs a sophisticated multi-agent workflow:

1. **Input Processing**: User submits startup idea through Streamlit interface
2. **Tools‑First Analysis Nodes**: Each analysis node (market, competition, risk) runs in tools mode by default and may emit a tool call (DuckDuckGo) when needed
3. **Tool Execution and Routing**: Tool calls are routed through a central tools node; results are fed back into the calling node
4. **Automatic Fallbacks**: If a tool fails, the router diverts execution to a chat‑only fallback node to complete that step without tools
5. **Strategic Advisory**: Final advisor aggregates prior results and returns decision plus rationale
6. **Report Generation**: Consolidated validation report is returned to the frontend

Each agent leverages web search capabilities and specialized prompts to ensure thorough, data-driven analysis.

### New Flow Strategy (Tools‑First with Fallbacks)

- **Dynamic routing**: A custom router advances through `ANALYSIS_LIST` and determines the next node based on tool outcomes.
- **Tool node**: When a model response contains a tool call, execution is routed to a shared tools node and then resumed.
- **Fallback nodes**: On tool failure, execution skips to a chat‑only fallback for the current analysis step to ensure progress.

## Dependencies

### Core Framework
- **FastAPI**: High-performance API backend
- **React**: Interactive web frontend
- **LangGraph**: Workflow orchestration
- **LangChain Community**: Agent tools and integrations

### Search & Data
- **duckduckgo-search**: Web search functionality
- **Pydantic**: Data validation and parsing

## API Endpoints

### POST /validate
Validates a startup idea through comprehensive analysis.

**Request Body:**
```json
{
  "startup_idea": "Your startup idea description"
}
```

**Response:**
```json
{
  "startup_idea": "Original idea",
  "idea_analysis":"Explicitly Explaining the Idea",
  "market_analysis": "Market insights and opportunities",
  "competition_analysis": "Competitive landscape assessment", 
  "risk_assessment": "Risk factors and mitigation strategies",
  "SWOT Analysis": "SWOT(Strength, Weakness, Oppourtunities, Threats) Analysis",
  "advisor_recommendations": "Go/No-Go/Conditional Go",
  "advice": "Strategic recommendations and next steps"
}
```

## Limitations & Considerations

- **API Dependencies**: Relies on Google Gemini and DuckDuckGo services
- **Rate Limits**: Free tier API usage may have limitations
- **Search Quality**: Analysis quality depends on available web content
- **Response Time**: Initial model loading may cause delays
- **Data Privacy**: Ensure sensitive business ideas are handled appropriately
