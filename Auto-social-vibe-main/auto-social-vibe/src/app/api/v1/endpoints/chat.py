from fastapi import APIRouter, Depends, HTTPException
from src.app.models.chat_models import ChatRequest, ChatResponse, Answer
from src.app.workflows.rag_workflow import create_rag_graph

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, graph=Depends(create_rag_graph)):
    try:
        # Prepare the input state for the RAG workflow
        initial_state = {"question": request.question}
        
        # Call the async invoke function
        result_state = await graph.ainvoke(initial_state)

        # Ensure the result is a valid dictionary
        if not isinstance(result_state, dict):
            raise HTTPException(status_code=500, detail="Invalid response from RAG graph.")

        # Extract answer and image link from the result
        answer_caption = result_state.get("answer", "Sorry, I couldn't find an answer.")
        image_link = result_state.get("image_link", "")

        # Return the response in the correct format
        return ChatResponse(answer=Answer(image=image_link, caption=answer_caption))  # ✅ Correct format

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
