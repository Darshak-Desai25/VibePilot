from langgraph.graph import END, StateGraph

from src.app.nodes_and_edges.nodes.llm_node import llm_node,image_generation
from src.app.nodes_and_edges.nodes.prompt_node import prompt_node , first_prompt_node
from src.app.nodes_and_edges.nodes.retrieval_node import retrieve_node
from src.app.states.schemas import AgentState

from tavily import TavilyClient
import os, re
from dotenv import load_dotenv
load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_online(state: AgentState):  # Default search depth if not specified
    """this is search tool which take latest information from the internet."""
    # print("State in searchhh node:", state['question'])
    try:
        # Perform the search using Tavily API
        result = tavily_client.get_search_context(
            query=state['clear_query'],
            max_tokens=1000  # Adjust as needed
        )
        #print(result)
        
        cleaned_result = re.sub(r'[\\"]+', '', result)
        cleaned_result = cleaned_result.strip("'[]")
        state["context"]=cleaned_result
        return state#{"result": cleaned_result}
    except Exception as e:
        return {'error': 'Search failed', 'details': str(e)}


def create_rag_graph():
    workflow = StateGraph(AgentState)

    #workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("user_prompt",first_prompt_node)#prompt template for query and platform
    workflow.add_node("llm_node", llm_node)#Response: ["generated_query": "tarrif war", "platform": "instagram"]
    workflow.add_node("final_llm_node",llm_node)
    workflow.add_node("searching_online", search_online)
    workflow.add_node("generate_prompt", prompt_node)# prompt for generating caption
    workflow.add_node("generate_image_llm", image_generation)
    # workflow.add_node("post_instagram", post_instagram)


    workflow.add_edge("user_prompt", "llm_node")
    workflow.add_edge("llm_node","searching_online")
    workflow.add_edge("searching_online", "generate_prompt")
    workflow.add_edge("generate_prompt", "final_llm_node")
    workflow.add_edge("final_llm_node", 'generate_image_llm')
    workflow.add_edge("generate_image_llm", END)

    workflow.set_entry_point("user_prompt")
    app = workflow.compile()
    # try:
    #     display(Image(app.get_graph().draw_mermaid_png()))
    # except Exception:
    #     # This requires some extra dependencies and is optional
    #     pass
    return app
