import os
from openai import OpenAI
from dotenv import load_dotenv
from settings.constants import model_id

load_dotenv()
HF_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

def call_llm(question: str, rag_info):
    prompt = f'''
    You are an assistant that answers questions exclusively about the context provided in rag_info and only take context from the given content:

    Here's a question: {question}

    Here's some context for the above question: {rag_info}

    Answer:
    '''

    client = OpenAI(
        base_url = "https://router.huggingface.co/v1",
        api_key = HF_TOKEN
    )

    response = client.chat.completions.create(
        model  = model_id,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response
