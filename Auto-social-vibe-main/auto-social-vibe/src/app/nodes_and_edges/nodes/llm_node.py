from langchain_core.messages import AIMessage
from src.app.logic.llm import create_llm, generate_image
from src.app.states.schemas import AgentState
import json,re


async def llm_node(state: AgentState):
    llm = create_llm()

    if not state.get("messages"):
        state["messages"] = []
    llm = create_llm()

    state["messages"].append(state["prompt"])
    
    response = await llm.ainvoke(state["prompt"].messages)

    if "generated_query" in response.content:
        match = re.search(r'\[(.*?)\]', response.content)
        if match:
            state["messages"].append(AIMessage(content=response.content))
            content_list = match.group(1).split(",")
            state["clear_query"], state["social_media"] = content_list[:2]
    else:
        state["messages"].append(AIMessage(content=response.content))
        state["answer"] = response.content
       
    
    return state

def image_generation(state: AgentState):
    if not state.get("messages"):
        state["messages"] = []
    query = state["answer"]
    response = generate_image(query)
    state["messages"].append(AIMessage(content=response))
    state["image_link"] = response
    return state

