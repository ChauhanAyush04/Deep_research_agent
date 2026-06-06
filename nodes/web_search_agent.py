from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict
from state.agent_state import AgentState
from models.chat_model import chat_model
from config import WEB_SEARCH_PROMPT_PATH
from ddgs import DDGS
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import logging
from bs4 import BeautifulSoup
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebFinding(BaseModel):
    """Individual finding from web search"""
    question: str = Field(description="The research question this finding addresses")
    summary: str = Field(description="Concise summary of findings")
    sources: List[dict] = Field(description="List of sources with title, url, and type")


class ScraperConfig:
    """Configuration for safe web scraping"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Domains that should be skipped (403 Forbidden, paywalls, etc.)
    BLOCKED_DOMAINS = {
        'wikipedia.org': 'Blocks automated scraping',
        'sciencedirect.com': 'Requires authentication',
        'himss.org': 'Blocks automated access',
        'quora.com': 'Blocks bots',
        'weforum.org': 'Blocks automated access',
        'journals.sagepub.com': 'Requires authentication',
        'jstor.org': 'Requires subscription',
        'springer.com': 'Requires subscription',
        'nature.com': 'Requires subscription',
    }
    
    TIMEOUT = 10
    MAX_RETRIES = 2
    RETRY_DELAY = 1


def get_session_with_retries():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=ScraperConfig.MAX_RETRIES,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(ScraperConfig.HEADERS)
    
    return session


def is_blocked_domain(url: str) -> tuple[bool, str]:
    """Check if a domain is blocked or restricted"""
    url_lower = url.lower()
    for domain, reason in ScraperConfig.BLOCKED_DOMAINS.items():
        if domain in url_lower:
            return True, reason
    return False, ""


def safe_scrape_url(url: str) -> Optional[Dict]:
    """
    Safely scrape a URL with comprehensive error handling.
    Returns dict with 'content' and 'title' on success, None on failure.
    """
    
    # Check if domain is blocked
    is_blocked, reason = is_blocked_domain(url)
    if is_blocked:
        logger.warning(f"[BLOCKED] {url} - {reason}")
        return None
    
    try:
        session = get_session_with_retries()
        response = session.get(url, timeout=ScraperConfig.TIMEOUT, allow_redirects=True)
        response.raise_for_status()
        
        # Extract text using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Get title
        title = soup.find('title')
        page_title = title.string if title else "Untitled"
        
        # Limit content length
        content = content[:1500]
        
        logger.info(f"[SUCCESS] Scraped: {url}")
        return {
            "content": content,
            "title": page_title,
            "url": url
        }
        
    except requests.exceptions.Timeout:
        logger.warning(f"[TIMEOUT] {url}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"[CONNECTION ERROR] {url}")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logger.warning(f"[403 FORBIDDEN] {url}")
        elif e.response.status_code == 401:
            logger.warning(f"[401 UNAUTHORIZED] {url}")
        else:
            logger.warning(f"[HTTP {e.response.status_code}] {url}")
        return None
    except Exception as e:
        logger.warning(f"[ERROR] {url} - {str(e)}")
        return None


def extract_text_with_fallback(html: str) -> str:
    """Extract main text content from HTML with multiple fallback methods"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Try to find main content
        main = soup.find(['main', 'article', 'div#content', 'div.content'])
        if main:
            text = main.get_text()
        else:
            text = soup.get_text()
        
        # Clean up
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = ' '.join(chunk for chunk in chunks if chunk)
        
        return content[:1500]  # Limit to 1500 chars
        
    except Exception as e:
        logger.warning(f"Fallback extraction failed: {e}")
        return ""


def perform_web_search(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    """
    Web Search Agent
    
    Purpose: Search the web and scrape content for answers to research questions
    
    Steps:
    1. Search for each research question using DuckDuckGo
    2. Scrape relevant content from top URLs (with safe handling)
    3. Clean and extract main content
    4. Summarize findings per question using LLM
    
    Input: research_questions from Topic Analyzer
    Output: web_findings (structured findings with sources)
    """
    
    def web_search_agent(state: AgentState) -> AgentState:
        research_questions = state.get("research_questions", [])
        
        if not research_questions:
            logger.warning("No research questions provided")
            return {"web_findings": []}
        
        web_findings = []
        ddgs = DDGS()
        
        for question_idx, question in enumerate(research_questions, 1):
            try:
                logger.info(f"[{question_idx}/{len(research_questions)}] Searching: {question}")
                
                # Step 1: Search the web for this question
                search_results = ddgs.text(question, max_results=10)
                
                if not search_results:
                    logger.warning(f"No search results for: {question}")
                    continue
                
                # Step 2: Scrape and clean content from top URLs
                extracted_contents = []
                sources = []
                
                for result_idx, result in enumerate(search_results[:5], 1):
                    url = result.get("href")
                    title = result.get("title", "Untitled")
                    
                    if not url:
                        logger.warning(f"Skipping result with no URL")
                        continue
                    
                    logger.info(f"  [{result_idx}/5] Scraping: {url}")
                    
                    # Safely scrape URL
                    scraped = safe_scrape_url(url)
                    
                    if scraped:
                        extracted_contents.append({
                            "url": url,
                            "title": title,
                            "body": scraped["content"]
                        })
                        
                        sources.append({
                            "title": title,
                            "url": url,
                            "type": "web"
                        })
                    
                    # Rate limiting - be respectful
                    time.sleep(ScraperConfig.RETRY_DELAY)
                
                # Step 3: Summarize findings using LLM
                if extracted_contents:
                    try:
                        # Load prompt template
                        try:
                            with open(WEB_SEARCH_PROMPT_PATH, 'r') as f:
                                template = f.read()
                        except FileNotFoundError:
                            logger.error(f"Prompt file not found: {WEB_SEARCH_PROMPT_PATH}")
                            # Use default template
                            template = """Answer the following research question based on the provided web content.

Question: {question}

Web Content:
{contents}

Provide a concise summary of the key findings from these sources."""
                        
                        prompt_template = PromptTemplate(
                            input_variables=["question", "contents"],
                            template=template
                        )
                        
                        # Create chain properly
                        chain = prompt_template | chat_model
                        
                        # Invoke with proper error handling
                        summary_response = chain.invoke({
                            "question": question,
                            "contents": json.dumps(extracted_contents, indent=2)
                        })
                        
                        # Extract content from response
                        summary_text = summary_response.content if hasattr(summary_response, 'content') else str(summary_response)
                        
                        web_findings.append(WebFinding(
                            question=question,
                            summary=summary_text,
                            sources=sources
                        ).dict())
                        
                        logger.info(f"✓ Completed: {question}")
                        
                    except Exception as e:
                        logger.error(f"Error summarizing findings for '{question}': {str(e)}")
                        # Still add finding with raw sources
                        web_findings.append({
                            "question": question,
                            "summary": f"Web sources found but summary generation failed. Sources available: {len(sources)}",
                            "sources": sources
                        })
                else:
                    logger.warning(f"No content could be scraped for: {question}")
            
            except Exception as e:
                logger.error(f"Error processing question '{question}': {str(e)}")
                continue
        
        logger.info(f"\n[SUMMARY] Found {len(web_findings)} web findings from {len(research_questions)} questions")
        
        return {
            "web_findings": web_findings
        }
    
    return web_search_agent
