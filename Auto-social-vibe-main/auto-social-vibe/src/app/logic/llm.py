from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from openai import OpenAI

def create_llm(model_name: str = "gpt-4o") -> ChatOpenAI:

    model = ChatOpenAI(model=model_name)
    return model

def generate_image(prompt:str):

    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url