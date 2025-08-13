from langchain_core.prompts import ChatPromptTemplate

def social_media_prompt_template(question: str) -> ChatPromptTemplate:
    
    template =""" You are a helpful assistant. Your task is to generate a clear and optimized search query for Google based on a given question. Additionally, identify which social media platform (e.g., Instagram, Twitter, LinkedIn) the query is related to.

        Your response should strictly follow this format:
        answer: ["generated_query": "your refined query", "platform": "social_media_platform"]

        Example:
        Query: "post the content related to tariff war on instagram"
        Response: ["generated_query": "tarrif war", "platform": "instagram"]

        Now, process the following question and provide your response in the given format:
        query: {question}
        """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt

def create_chat_prompt_template(context: str, question: str, social_media: str) -> ChatPromptTemplate:
    template = """Generate a high-quality post, tweet, or blog content based on platform and following context:
    {context}
    Craft an engaging, relevant, and platform-optimized response.
    platform: {social_media}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt

def create_prompt_generate_image(clear_query: str, social_media: str) -> ChatPromptTemplate:
    template = """Generate a high-quality promptto generate image based on platform and following query:
    {clear_query}
    platform: {social_media}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt