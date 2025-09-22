from QA_System.ingestion import upsert_chunks
from QA_System.search import hybrid_search
import asyncio

def start_RAG_pipe(pdf):
    """
    Main funciton to upsert into the vector db(s).
    """
    return upsert_chunks(pdf_path = pdf)

def hyd_search_pdf(question):
    """
    Main funciton to search the vector databases.
    """
    return hybrid_search(query = question)

