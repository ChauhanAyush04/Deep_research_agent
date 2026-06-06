from langchain_core.prompts import PromptTemplate
from typing import Literal, Dict, List, Set, Tuple
from state.agent_state import AgentState
from models.chat_model import chat_model
from config import WRITER_PROMPT_PATH
import json
import re
from collections import OrderedDict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def synthesize_report(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    """
    Writer Agent
    
    Synthesizes web findings and academic papers into a comprehensive narrative report
    following academic research report structure with 8,000-12,000 words.
    Ensures a SINGLE, deduplicated reference list at the end.
    """
    
    def writer_agent(state: AgentState) -> AgentState:
        try:
            web_findings = state.get("web_findings", [])
            top_5_papers = state.get("top_5_papers", [])
            topic = state.get("topic", "")
            
            if not topic:
                raise ValueError("Topic is required in state")
            
            logger.info(f"Generating report for: {topic}")
            
            # Format findings for prompt
            web_findings_text = format_web_findings(web_findings)
            papers_text = format_papers(top_5_papers)
            
            # Load prompt
            try:
                with open(WRITER_PROMPT_PATH, 'r') as f:
                    template = f.read()
            except FileNotFoundError:
                raise ValueError(f"Prompt file not found at {WRITER_PROMPT_PATH}")
            
            prompt_template = PromptTemplate(
                input_variables=["topic", "web_findings", "papers"],
                template=template
            )
            
            logger.info("Generating comprehensive report with LLM...")
            
            # Generate comprehensive report
            chain = prompt_template | chat_model
            
            response = chain.invoke({
                "topic": topic,
                "web_findings": web_findings_text,
                "papers": papers_text
            })
            
            # Generate SINGLE unified references (fully deduplicated)
            logger.info("Generating deduplicated reference list...")
            references = generate_single_unified_references(web_findings, top_5_papers)
            
            # Remove any existing reference sections from the response
            report_content = remove_existing_references(response.content)
            
            # Combine report with SINGLE references section
            final_report = f"{report_content}\n\n## References\n\n{references}"
            
            # Validate word count
            validation = validate_report_length(final_report)
            
            logger.info(f"Report generation complete!")
            logger.info(f"  Word count: {validation['word_count']} words")
            logger.info(f"  Status: {validation['status']}")
            logger.info(f"  References: {count_references(references)}")
            
            return {
                "final_report": final_report,
                "word_count": validation["word_count"],
                "validation_status": validation["status"],
                "reference_count": count_references(references)
            }
            
        except ValueError as e:
            logger.error(f"Validation error in writer agent: {e}")
            raise ValueError(f"Validation error in writer agent: {e}")
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Error generating report: {str(e)}")
    
    return writer_agent


def format_web_findings(web_findings: list) -> str:
    """Format web findings for the writer prompt"""
    if not web_findings:
        return "No web findings available."
    
    formatted = ""
    for i, finding in enumerate(web_findings, 1):
        formatted += f"### Finding {i}\n"
        formatted += f"**Question:** {finding.get('question', 'N/A')}\n\n"
        formatted += f"**Summary:** {finding.get('summary', 'N/A')}\n\n"
        
        sources = finding.get('sources', [])
        if sources:
            formatted += "**Sources:**\n"
            for source in sources[:5]:  # Limit to top 5 sources
                title = source.get('title', 'N/A')
                url = source.get('url', 'N/A')
                formatted += f"- [{title}]({url})\n"
        formatted += "\n---\n\n"
    
    return formatted


def format_papers(papers: list) -> str:
    """Format academic papers for the writer prompt"""
    if not papers:
        return "No academic papers found."
    
    formatted = ""
    for i, paper in enumerate(papers, 1):
        formatted += f"### Paper {i}\n"
        formatted += f"**Title:** {paper.get('title', 'Unknown')}\n\n"
        
        authors = paper.get('authors', [])
        if authors:
            formatted += f"**Authors:** {', '.join(authors)}\n\n"
        
        formatted += f"**Year:** {paper.get('year', 'N/A')}\n\n"
        formatted += f"**Summary:** {paper.get('summary', 'N/A')}\n\n"
        
        findings = paper.get('key_findings', [])
        if findings:
            formatted += "**Key Findings:**\n"
            for finding in findings:
                formatted += f"- {finding}\n"
            formatted += "\n"
        
        limitations = paper.get('limitations', [])
        if limitations:
            formatted += "**Limitations:**\n"
            for limitation in limitations:
                formatted += f"- {limitation}\n"
            formatted += "\n"
        
        url = paper.get('url', '')
        if url:
            formatted += f"**URL:** {url}\n\n"
        
        formatted += "---\n\n"
    
    return formatted


def extract_url_from_reference(ref_text: str) -> str:
    """Extract URL from a reference string"""
    match = re.search(r'https?://[^\s]+', ref_text)
    if match:
        url = match.group(0).rstrip('.,;)')
        return url
    return None


def extract_title_from_reference(ref_text: str) -> str:
    """Extract title from a reference string"""
    if "Retrieved from" in ref_text:
        title = ref_text.split("Retrieved from")[0].strip().strip('.')
        return title
    match = re.search(r'\(\d{4}\)\.\s*(.+?)(?:\.\s*Retrieved|\.$)', ref_text)
    if match:
        return match.group(1).strip()
    return None


def generate_single_unified_references(web_findings: list, papers: list) -> str:
    """
    Generate a SINGLE unified reference list with ZERO duplicates.
    - Eliminates ALL duplicates (by URL, title, or DOI)
    - Numbers sequentially (1, 2, 3, etc.)
    - ONE entry per reference
    - Process academic papers first (higher priority), then web sources
    """
    seen_urls: Set[str] = set()
    seen_titles: Set[str] = set()
    references_list: List[str] = []
    
    # ============= PRIORITY 1: Academic Papers =============
    if papers:
        for paper in papers:
            authors = paper.get('authors', [])
            title = paper.get('title', 'Unknown').strip()
            year = paper.get('year', 'N/A')
            url = paper.get('url', '').strip()
            
            # Skip duplicates by URL
            if url and url in seen_urls:
                logger.debug(f"[SKIP] Duplicate paper URL: {url}")
                continue
            
            # Skip duplicates by title
            if title in seen_titles:
                logger.debug(f"[SKIP] Duplicate paper title: {title}")
                continue
            
            # Format: Authors (Year). Title. Retrieved from URL
            author_str = ", ".join(authors) if authors else "Unknown"
            ref_text = f"{author_str} ({year}). {title}"
            
            if url:
                ref_text += f". Retrieved from {url}"
                seen_urls.add(url)
            
            seen_titles.add(title)
            references_list.append(ref_text)
            logger.debug(f"[ADD] Paper: {title[:50]}...")
    
    # ============= PRIORITY 2: Web Sources =============
    if web_findings:
        for finding in web_findings:
            sources = finding.get('sources', [])
            for source in sources:
                title = source.get('title', 'Unknown').strip()
                url = source.get('url', '').strip()
                
                # Skip if URL is missing or N/A
                if not url or url == 'N/A':
                    logger.debug(f"[SKIP] Missing URL for: {title[:50]}...")
                    continue
                
                # Skip if we've already seen this URL
                if url in seen_urls:
                    logger.debug(f"[SKIP] Duplicate web source URL: {url}")
                    continue
                
                # Skip if we've already seen this title
                if title in seen_titles:
                    logger.debug(f"[SKIP] Duplicate web source title: {title[:50]}...")
                    continue
                
                ref_text = f"{title}. Retrieved from {url}"
                
                seen_urls.add(url)
                seen_titles.add(title)
                references_list.append(ref_text)
                logger.debug(f"[ADD] Web source: {title[:50]}...")
    
    # ============= FINAL: Number and Format =============
    if not references_list:
        return "No references available."
    
    # Number the references
    numbered_references = "\n\n".join(
        f"{i}. {ref}" for i, ref in enumerate(references_list, 1)
    )
    
    logger.info(f"[SUMMARY] Total unique references: {len(references_list)}")
    return numbered_references


def remove_existing_references(report_content: str) -> str:
    """
    Remove any existing reference sections from the report.
    Handles both "## References" and numbered list formats.
    """
    # Remove "## References" section and everything after it
    report = re.split(r'##\s*References', report_content, flags=re.IGNORECASE)[0]
    
    # Remove any trailing "References" followed by numbered list
    report = re.sub(
        r'References\s*\n+(?:\d+\.|---)',
        '',
        report,
        flags=re.IGNORECASE
    )
    
    return report.rstrip()


def validate_report_length(report: str, min_words: int = 8000, max_words: int = 12000) -> dict:
    """
    Validate that the generated report meets word count requirements.
    """
    word_count = len(report.split())
    
    return {
        "word_count": word_count,
        "meets_minimum": word_count >= min_words,
        "meets_maximum": word_count <= max_words,
        "status": "valid" if min_words <= word_count <= max_words else "invalid"
    }


def count_references(references_text: str) -> int:
    """Count the number of references in the text"""
    return len(re.findall(r'^\d+\.', references_text, re.MULTILINE))


def deduplicate_existing_references(references_str: str) -> str:
    """
    Deduplicate an existing reference string (if you already have one).
    Removes exact duplicates and near-duplicates.
    """
    lines = references_str.split('\n\n')  # Split by double newline
    seen_urls: Set[str] = set()
    seen_titles: Set[str] = set()
    unique_lines = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # Extract URL
        url = extract_url_from_reference(line)
        if url:
            if url in seen_urls:
                logger.debug(f"[REMOVE] Duplicate URL: {url}")
                continue
            seen_urls.add(url)
        
        # Extract title
        title = extract_title_from_reference(line)
        if title:
            if title in seen_titles:
                logger.debug(f"[REMOVE] Duplicate title: {title[:50]}...")
                continue
            seen_titles.add(title)
        
        unique_lines.append(line)
    
    # Re-number the references
    renumbered = []
    for i, line in enumerate(unique_lines, 1):
        # Remove the old number
        line = re.sub(r'^\d+\.\s*', '', line)
        renumbered.append(f"{i}. {line}")
    
    return '\n\n'.join(renumbered)
