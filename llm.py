import os
from openai import OpenAI
from dotenv import load_dotenv
from settings.constants import model_id
from main_funcs import hyd_search_pdf

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

def call_llm(question: str, rag_info: str, stream: bool = True):
    """
    Call HuggingFace LLM (OpenAI-compatible) with optional streaming.
    """
    prompt = f"""
    You are an assistant that answers questions by taking the context provided in rag_info and mostly from the given content:

    Question: {question}

    Context: {rag_info}

    Answer:
    """

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        stream=stream
    )
    return response

def get_response(user_que: str):
    """
    Wrapper to fetch RAG context and call LLM.
    """
    rag_information = hyd_search_pdf(user_que)
    return call_llm(user_que, rag_information, stream=True)

def stream_generator(stream):
    """
    Generator that yields content from a streaming response.
    """
    for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                yield content
