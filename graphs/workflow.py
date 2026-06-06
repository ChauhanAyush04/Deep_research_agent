from langgraph.graph import StateGraph, END
from state.agent_state import AgentState
from nodes.topic_analyzer import analyze_topic
from nodes.web_search_agent import perform_web_search
from nodes.paper_reader_agent import analyze_papers
from nodes.writer_agent import synthesize_report

def build_graph():
    """
    Builds the parallel research workflow graph:
    
    topic_analyzer
    ├─→ web_search_agent ──┐
    │                       ├→ writer_agent → END
    └─→ paper_reader_agent ┘
    
    Web Search and Paper Reader agents execute in parallel,
    improving efficiency and reducing response time.
    """
    
    graph_builder = StateGraph(AgentState)
    
    # Add nodes
    graph_builder.add_node("topic_analyzer", analyze_topic("chat_model"))
    graph_builder.add_node("web_search_agent", perform_web_search("chat_model"))
    graph_builder.add_node("paper_reader_agent", analyze_papers("chat_model"))
    graph_builder.add_node("writer_agent", synthesize_report("chat_model"))
    
    # Set entry point
    graph_builder.set_entry_point("topic_analyzer")
    
    # After topic analyzer, split into parallel execution
    graph_builder.add_edge("topic_analyzer", "web_search_agent")
    graph_builder.add_edge("topic_analyzer", "paper_reader_agent")
    
    # Both converge to writer agent
    graph_builder.add_edge("web_search_agent", "writer_agent")
    graph_builder.add_edge("paper_reader_agent", "writer_agent")
    
    # Writer to end
    graph_builder.add_edge("writer_agent", END)
    
    # Compile graph
    graph = graph_builder.compile()
    
    return graph