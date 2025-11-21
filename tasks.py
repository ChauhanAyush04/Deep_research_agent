from crewai import Task
from agents import topic_analyst, web_searcher, web_content_reader, paper_reader_agent, insight_agent, report_agent


analyze_topic_task = Task(
    description="""
            Analyze the user-provided topic: '{topic}'.

                Your responsibilities:
                1. Provide a clear explanation of the topic.
                2. Identify important subtopics and knowledge areas.
                3. List relevant keywords for search engines.
                4. Generate 5-10 research questions.
                5. Produce a structured research plan.

                Output MUST be valid JSON:
                {
                "topic_overview": "...",
                "subtopics": [...],
                "keywords": [...],
                "research_questions": [...],
                "research_plan": "..."
                }
                """,
    agent=topic_analyst,
    expected_output="JSON with topic breakdown, subtopics, questions, keywords, and research plan."
)


web_search_task = Task(
    name="Web Search Task",
    description="""
                Using subtopics, keywords, and research questions, perform comprehensive web searches.

                Steps:
                1. Generate multiple search queries.
                2. Use search tools to fetch results.
                3. Collect page titles, URLs, and snippets.
                4. Fetch a short content preview for each link.
                5. Return a list of structured sources.

                Output MUST be valid JSON:
                {
                "search_queries": [...],
                "sources": [
                    {
                        "title": "...",
                        "url": "...",
                        "snippet": "...",
                        "raw_content_preview": "..."
                    }
                ]
                }
                """,
    agent=web_searcher,
    expected_output="JSON containing search queries + structured list of sources.",
    context=[analyze_topic_task]

)


read_content_task = Task(
    name="Web Content Extraction Task",
    description="""
                Read and extract meaningful information from each URL.

                For every page:
                1. Fetch webpage content.
                2. Remove noise like ads, menus, headers.
                3. Extract important paragraphs, definitions, and explanations.
                4. Summarize the page.
                5. Provide bullet-point insights.

                Output MUST be valid JSON:
                {
                "url": "...",
                "title": "...",
                "summary": "...",
                "key_points": [...],
                "clean_text": "..."
                }
                """,
    agent=web_content_reader,
    expected_output="JSON containing cleaned text, key points, and summaries for each URL.",
    context=[web_search_task]
)


read_papers_task = Task(
    name="Research Paper Reading Task",
    description="""
                Search for and analyze academic research papers related to the topic.

                For each paper:
                1. Fetch metadata (title, authors, publication year).
                2. Read the abstract and introduction.
                3. Extract method, results, and conclusion.
                4. Identify key findings, limitations, and contributions.
                5. Generate a proper citation.

                Output MUST be valid JSON:
                {
                "title": "...",
                "authors": "...",
                "source": "...",
                "abstract_summary": "...",
                "method_summary": "...",
                "key_findings": [...],
                "limitations": "...",
                "citation": "..."
                }
                """,
    agent=paper_reader_agent,
    expected_output="JSON with summaries and extracted scientific insights.",
    context=[analyze_topic_task]
)


synthesize_task = Task(
    name="Insight Synthesis Task",
    description="""
                Using all previous outputs (topic analysis, web search results, webpage summaries, 
                and research paper summaries), synthesize deep insights.

                Steps:
                1. Combine all information.
                2. Identify patterns, themes, and key insights.
                3. Compare findings across different sources.
                4. Resolve contradictions.
                5. Answer the research questions.
                6. Generate final conclusions.

                Output MUST be valid JSON:
                {
                "key_insights": [...],
                "answers_to_research_questions": {...},
                "comparisons": [...],
                "trends": [...],
                "final_conclusions": "..."
                }
                """,
    agent=insight_agent,
    expected_output="JSON containing insights, comparisons, and conclusions.",
    context=[
    analyze_topic_task,
    web_search_task,
    read_content_task,
    read_papers_task
    ]
)



generate_report_task = Task(
    name="Report Generation Task",
    description="""
                Using all synthesized insights and findings, write a complete research report.

                Structure must be:
                # <Topic>
                ## Introduction
                ## Research Questions
                ## Findings
                ## Insights & Analysis
                ## Summary / Conclusion
                ## References

                Requirements:
                - Clear academic writing style.
                - Well-structured sections.
                - No hallucinations.
                - Based entirely on previous outputs.

                Output MUST be Markdown text.
                """,
    agent=report_agent,
    expected_output="A complete, clean, well-formatted Markdown research report.",
    context=[synthesize_task]
)