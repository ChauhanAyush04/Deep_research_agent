from langchain_core.prompts import PromptTemplate
from typing import List, Literal, Optional, Dict
from state.agent_state import AgentState
from models.chat_model import chat_model
from config import READ_PAPER_PROMPT_PATH
import requests
import json
import time
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArXivConfig:
    """Configuration for ArXiv API interactions"""
    BASE_URL = "http://export.arxiv.org/api/query?"
    TIMEOUT = 10
    RATE_LIMIT_DELAY = 1  # seconds between requests
    MAX_RETRIES = 2


def get_session_with_retries():
    """Create a requests session with retry strategy for ArXiv"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=ArXivConfig.MAX_RETRIES,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def analyze_papers(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    """
    Paper Reader Agent
    
    Purpose: Find and analyze academic papers from ArXiv
    
    Steps:
    1. Search ArXiv for papers on each research topic
    2. Retrieve candidate papers (25+ per topic)
    3. Perform semantic similarity matching (TF-IDF + cosine similarity)
    4. Rank papers by relevance score
    5. Select top 5 papers overall
    6. Analyze each paper to extract key findings and limitations
    
    Input: research_topics from Topic Analyzer
    Output: top_5_papers (structured with key findings and limitations)
    """
    
    def paper_reader_agent(state: AgentState) -> AgentState:
        research_topics = state.get("research_topics", [])
        
        if not research_topics:
            logger.warning("No research topics provided")
            return {"top_5_papers": []}
        
        all_papers = []
        
        # Search ArXiv for papers across all research topics
        for topic_idx, topic in enumerate(research_topics, 1):
            try:
                logger.info(f"[{topic_idx}/{len(research_topics)}] Searching ArXiv for: {topic}")
                papers = search_arxiv(topic)
                all_papers.extend(papers)
                logger.info(f"  Found {len(papers)} papers")
            except Exception as e:
                logger.error(f"Error searching ArXiv for topic '{topic}': {str(e)}")
                continue
        
        if not all_papers:
            logger.warning("No papers found in ArXiv")
            return {"top_5_papers": []}
        
        logger.info(f"\n[SEARCH SUMMARY]")
        logger.info(f"  Total papers found: {len(all_papers)}")
        
        # Remove duplicates by title
        seen_titles = set()
        unique_papers = []
        for paper in all_papers:
            title = paper.get('title', '').lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(paper)
        
        logger.info(f"  Unique papers: {len(unique_papers)}")
        
        # Rank by semantic similarity
        try:
            ranked_papers = rank_papers_by_similarity(unique_papers, research_topics)
            logger.info(f"  Papers ranked by relevance")
        except Exception as e:
            logger.error(f"Error ranking papers: {str(e)}")
            # Fallback: sort by year
            ranked_papers = sorted(unique_papers, key=lambda x: x.get("year", 0), reverse=True)
        
        # Select top 5 papers
        top_5 = ranked_papers[:5]
        logger.info(f"  Selected top 5 papers")
        
        # Analyze each top paper with LLM
        analyzed_papers = []
        for i, paper in enumerate(top_5, 1):
            try:
                logger.info(f"\nAnalyzing paper {i}/5: {paper.get('title', 'Unknown')[:60]}...")
                analyzed_paper = analyze_single_paper(paper, chat_model)
                analyzed_papers.append(analyzed_paper)
                logger.info(f"  ✓ Analysis complete")
            except Exception as e:
                logger.error(f"Error analyzing paper {i}: {str(e)}")
                # Add paper with empty analysis instead of skipping
                analyzed_papers.append({
                    "title": paper.get("title", ""),
                    "authors": paper.get("authors", []),
                    "year": paper.get("year", 0),
                    "summary": paper.get("abstract", "")[:500],
                    "key_findings": [],
                    "limitations": [],
                    "url": paper.get("url", ""),
                    "relevance_score": paper.get("relevance_score", 0),
                    "citation_count": paper.get("citation_count", 0)
                })
        
        logger.info(f"\n[ANALYSIS SUMMARY]")
        logger.info(f"  Successfully analyzed: {len(analyzed_papers)}/5 papers")
        
        return {"top_5_papers": analyzed_papers}
    
    return paper_reader_agent


def search_arxiv(topic: str, limit: int = 25) -> List[dict]:
    """
    Search ArXiv for papers related to a topic
    
    Uses ArXiv API (http://export.arxiv.org/api/query)
    Returns structured paper metadata
    
    Handles:
    - Rate limiting (respectful delays)
    - API errors and timeouts
    - XML parsing errors
    """
    
    # Search query - search in title and abstract
    search_query = f"(ti:{topic} OR abs:{topic})"
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        # Be respectful to the API - rate limiting
        time.sleep(ArXivConfig.RATE_LIMIT_DELAY)
        
        session = get_session_with_retries()
        response = session.get(
            ArXivConfig.BASE_URL,
            params=params,
            timeout=ArXivConfig.TIMEOUT
        )
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        papers = []
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        for entry in root.findall('atom:entry', ns):
            try:
                # Extract title
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip() if title_elem is not None else "Unknown"
                
                # Extract abstract/summary
                summary_elem = entry.find('atom:summary', ns)
                abstract = summary_elem.text.strip() if summary_elem is not None else ""
                
                # Extract published date
                published_elem = entry.find('atom:published', ns)
                published_date = published_elem.text if published_elem is not None else ""
                year = int(published_date[:4]) if published_date else 0
                
                # Extract authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text.strip())
                
                # Extract paper ID and URL
                id_elem = entry.find('atom:id', ns)
                arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else ""
                arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
                
                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "abstract": abstract,
                    "url": arxiv_url,
                    "arxiv_id": arxiv_id,
                    "published_date": published_date,
                    "citation_count": 0  # ArXiv doesn't provide citation counts
                })
                
            except Exception as e:
                logger.warning(f"Error parsing individual paper entry: {str(e)}")
                continue
        
        return papers
        
    except requests.exceptions.Timeout:
        logger.error(f"ArXiv API timeout for topic: {topic}")
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error accessing ArXiv for topic: {topic}")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from ArXiv: {str(e)}")
        return []
    except ET.ParseError as e:
        logger.error(f"XML parse error from ArXiv response: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching ArXiv: {str(e)}")
        return []


def rank_papers_by_similarity(papers: List[dict], research_topics: List[str]) -> List[dict]:
    """
    Rank papers using semantic similarity (TF-IDF + cosine similarity)
    Papers with higher similarity to research topics are ranked first
    
    Falls back to chronological ordering if similarity calculation fails
    """
    
    if not papers:
        return papers
    
    if not research_topics:
        # Fallback: sort by year
        return sorted(papers, key=lambda x: x.get("year", 0), reverse=True)
    
    try:
        # Prepare texts for similarity calculation
        paper_texts = []
        for p in papers:
            # Combine title and abstract for better matching
            text = f"{p.get('title', '')} {p.get('abstract', '')}"
            paper_texts.append(text)
        
        # Combine all research topics
        combined_topics = " ".join(research_topics)
        
        # Calculate TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            min_df=1,
            max_df=0.95
        )
        all_texts = paper_texts + [combined_topics]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Get vectors for topics and papers
        topics_vector = tfidf_matrix[-1]
        paper_vectors = tfidf_matrix[:-1]
        
        # Calculate cosine similarity
        similarities = cosine_similarity(paper_vectors, topics_vector.reshape(1, -1)).flatten()
        
        # Add relevance scores to papers
        for i, paper in enumerate(papers):
            paper["relevance_score"] = float(similarities[i])
        
        # Sort by relevance score (descending)
        ranked_papers = sorted(papers, key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        logger.info(f"Papers ranked by semantic similarity (top score: {ranked_papers[0].get('relevance_score', 0):.3f})")
        
        return ranked_papers
        
    except Exception as e:
        logger.warning(f"Error calculating similarity: {str(e)}, falling back to chronological order")
        # Fallback: sort by year (most recent first)
        return sorted(papers, key=lambda x: x.get("year", 0), reverse=True)


def analyze_single_paper(paper: Dict, llm_model) -> dict:
    """
    Analyze a single paper using LLM to extract key findings and limitations
    
    Handles:
    - Missing prompt file (uses default template)
    - Invalid JSON responses (provides empty analysis)
    - LLM errors (returns paper with basic fields)
    """
    
    try:
        # Load prompt template
        try:
            with open(READ_PAPER_PROMPT_PATH, 'r') as f:
                template = f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt file not found: {READ_PAPER_PROMPT_PATH}")
            # Use default template
            template = """Analyze this academic paper and extract key findings and limitations.

Title: {title}

Abstract:
{abstract}

Provide the response as JSON with these fields:
{{
  "key_findings": ["finding1", "finding2", ...],
  "limitations": ["limitation1", "limitation2", ...]
}}"""
        
        prompt_template = PromptTemplate(
            input_variables=["title", "abstract"],
            template=template
        )
        
        # Create chain: prompt -> model
        chain = prompt_template | llm_model
        
        # Invoke with error handling
        response = chain.invoke({
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", "")
        })
        
        # Parse response
        analysis = {"key_findings": [], "limitations": []}
        
        try:
            content = response.content if hasattr(response, 'content') else str(response)
            
            if isinstance(content, str) and content.strip().startswith("{"):
                # Try to parse JSON
                parsed = json.loads(content)
                analysis = {
                    "key_findings": parsed.get("key_findings", []),
                    "limitations": parsed.get("limitations", [])
                }
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON response from LLM for paper: {paper.get('title', 'Unknown')[:50]}")
            analysis = {"key_findings": [], "limitations": []}
        except Exception as e:
            logger.warning(f"Error parsing LLM response: {str(e)}")
            analysis = {"key_findings": [], "limitations": []}
        
        return {
            "title": paper.get("title", ""),
            "authors": paper.get("authors", []),
            "year": paper.get("year", 0),
            "summary": paper.get("abstract", "")[:500],  # Limit to 500 chars
            "key_findings": analysis.get("key_findings", []),
            "limitations": analysis.get("limitations", []),
            "url": paper.get("url", ""),
            "arxiv_id": paper.get("arxiv_id", ""),
            "relevance_score": paper.get("relevance_score", 0),
            "citation_count": paper.get("citation_count", 0)
        }
        
    except Exception as e:
        logger.error(f"Unexpected error analyzing paper: {str(e)}")
        # Return paper with basic fields
        return {
            "title": paper.get("title", ""),
            "authors": paper.get("authors", []),
            "year": paper.get("year", 0),
            "summary": paper.get("abstract", "")[:500],
            "key_findings": [],
            "limitations": [],
            "url": paper.get("url", ""),
            "arxiv_id": paper.get("arxiv_id", ""),
            "relevance_score": paper.get("relevance_score", 0),
            "citation_count": paper.get("citation_count", 0)
        }
