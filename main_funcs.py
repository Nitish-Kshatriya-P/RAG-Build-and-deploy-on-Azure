from QA_System.ingestion import upsert_chunks
from QA_System.search import hybrid_search
import asyncio

def start_RAG_pipe(pdf):
    return upsert_chunks(pdf_path = pdf)

def hyd_search_pdf(question):
    return hybrid_search(query = question)

