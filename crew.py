from crewai import Crew,Process

from config import OPENAI_API_KEY, SERPLY_API_KEY
import os

from agents import (
    topic_analyst, web_searcher, web_content_reader, 
    paper_reader_agent, insight_agent, report_agent 
)

from tasks import (
    analyze_topic_task, web_search_task, read_content_task, 
    read_papers_task, synthesize_task, generate_report_task
)

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPLY_API_KEY"] = SERPLY_API_KEY

research_crew = Crew(
    agents=[
        topic_analyst,
        web_searcher,       
        web_content_reader,   
        paper_reader_agent,  
        insight_agent,           
        report_agent             
    ],

    tasks=[
        analyze_topic_task, 
        web_search_task,    
        read_content_task,    
        read_papers_task,      
        synthesize_task,       
        generate_report_task    
    ],
    verbose=True,
    process=Process.sequential,
    memory = False,
    cache = False,
    share_crew=True
)

if __name__ == "__main__":
    result = research_crew.kickoff(inputs={"topic": "Quantum computing applications"})
    print(result)