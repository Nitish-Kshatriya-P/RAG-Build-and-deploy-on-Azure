import os
from openai import OpenAI
from dotenv import load_dotenv
from settings.constants import model_id
from main_funcs import hyd_search_pdf

load_dotenv()
HF_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
# question: str, rag_info
def call_llm(question: str, rag_info):
        prompt = f'''
        You are an assistant that answers questions by taking the context provided in rag_info and mostly take context from the given content:

        Here's a question: {question}

        Here's some context for the above question: {rag_info}

        Answer:
        '''

        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_TOKEN  # Ensure HF_TOKEN is defined in your environment or configuration
        )

        response = client.chat.completions.create(
            model=model_id,  # Ensure model_id is defined in your environment or configuration
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )
        return response

def get_response(user_que: str):
    rag_information = hyd_search_pdf(user_que)

    llm_response = call_llm(question = user_que, rag_info= rag_information)

    return llm_response

def stream_generator(stream):
    """
    This generator function takes an OpenAI stream and yields the text content.
    """
    for chunk in stream:
        # It ensures that 'choices' is not an empty list before proceeding.
        if chunk.choices:
            content = chunk.choices[0].delta.content
            # This second check ensures the content is not None
            if content:
                yield content

