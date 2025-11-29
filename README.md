# 🔍 Deep Research Agent

An automated **multi-agent research system** built using **CrewAI** and **OpenAI**, capable of performing deep topic analysis, structured web research, scientific paper extraction, content summarization, and generating a complete research report.

GitHub Repository: **https://github.com/ChauhanAyush04/Deep_research_agent.git**

---

## 🚀 Overview

**Deep Research Agent** is a fully automated multi-agent pipeline that performs comprehensive research on *any* topic.  
It uses multiple specialized AI agents to:

- Analyze the topic  
- Search the web  
- Scrape and summarize webpages  
- Fetch and analyze scientific papers (arXiv, PDFs)  
- Extract insights  
- Generate a structured research report  

Powered by:

- **CrewAI** for agent orchestration  
- **OpenAI GPT models** for reasoning and writing  
- **Serply Web Search Tool**  
- **JinaScrapeWebsiteTool**  
- **ArxivPaperTool**  

---

## ✨ Features

### 🧠 Multi-Agent Workflow

#### **1. Topic Analyst**
Breaks down the input topic, generates subtopics, and identifies research questions.

#### **2. Web Search Agent**
Uses Serply / Google-like tools to find high-quality URLs.

#### **3. Web Content Reader**
Scrapes websites, removes noise, and extracts structured summaries.

#### **4. Research Paper Reader**
Fetches and reads scientific papers from arXiv; extracts methodology, findings, and insights.

#### **5. Insight Synthesizer**
Combines all sources and builds deep insights.

#### **6. Research Report Writer**
Generates a complete research document with:
- Introduction
- Questions
- Findings
- Insights
- References

---

## 📁 Project Structure

```
Deep_research_agent/
│
├── agents.py          # All agent definitions
├── tasks.py           # All task definitions
├── crew.py            # Crew configuration and research pipeline
├── config.py          # Loads API keys from .env
├── test_research.py   # Simple test script
│
├── requirements.txt   # Dependencies
├── .env               # API keys (not committed)
│
└── README.md          # Project documentation
```



## 🔧 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ChauhanAyush04/Deep_research_agent.git
cd Deep_research_agent
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 🔐 Environment Variables
Create a `.env` file in your project directory and add your API keys:

```ini
OPENAI_API_KEY=your-openai-key
SERPLY_API_KEY=your-serply-key
```

