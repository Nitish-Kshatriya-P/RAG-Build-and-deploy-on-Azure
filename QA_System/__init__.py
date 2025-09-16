import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINE_API = os.getenv("PINECONE_API_KEY")

def get_index_for_dense():
    pc = Pinecone(api_key=PINE_API)
    dense_index_name = "llmops"
    dense_index = pc.Index(name = dense_index_name)
    return dense_index

def get_index_for_sparse():
    pc = Pinecone(api_key=PINE_API)
    sparse_index_name = "sparse-vectors"
    sparse_index = pc.Index(name = sparse_index_name)
    #Vector_db = PineconeVectorStore(index = vecdb_index)
    return sparse_index


