from src.app.database import db
from src.app.logic.retrieval import create_retriever


async def retrieve_node(state):
    print("State in retrieval node:", state)
    retriever = create_retriever(db, k=2)

    state["context"] = await retriever.ainvoke(state["question"])
    return state
