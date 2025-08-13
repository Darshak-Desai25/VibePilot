from src.app.logic.prompt import create_chat_prompt_template,social_media_prompt_template,create_prompt_generate_image

async def first_prompt_node(state):
    question = state["question"]
    prompt = social_media_prompt_template(question)

    state["prompt"] = await prompt.ainvoke(
        {"question": question}
    )
    return state

async def prompt_node(state):
    question = state["question"]
    social_media = state["social_media"]
    context = state["context"]
    #formatted_context = [doc.page_content for doc in context]

    prompt = create_chat_prompt_template( question,context, social_media)

    state["prompt"] = await prompt.ainvoke(
        {"question": question, "context": context, "social_media": social_media}
    )
    return state

