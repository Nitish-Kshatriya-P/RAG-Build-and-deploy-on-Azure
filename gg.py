'''
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

client = InferenceClient(
    provider="nebius",
    api_key= HF_TOKEN,
)

result = client.feature_extraction(
    "Today is a sunny day and I will get some ice cream.",
    model="Qwen/Qwen3-Embedding-8B",
)

4096
'''
import langchain
import os
import pinecone
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from pydantic import BaseModel
from QA_System.__init__ import get_index_for_dense
from llm import call_llm
from QA_System.__init__ import get_index_for_sparse
from QA_System.search import hybrid_search
from settings.utils import delete_records
from QA_System.ingestion import upsert_chunks

load_dotenv()

upsert_chunks()

'''
class Output_format(BaseModel):
    id: str
    text: str
    metadata_source: str
    total_pages : int
    page_no : int


file_loader = PyPDFDirectoryLoader('Data/')
loaded_doc = file_loader.load()
print("File Loaded..")

ck_size = 800
ck_overlap = 50

docs_into_chunks = RecursiveCharacterTextSplitter(chunk_size = ck_size, chunk_overlap = ck_overlap)
split_pdf = docs_into_chunks.split_documents(loaded_doc)

print(split_pdf)

print("Done splitting the document into chunks...")


from langchain_core.documents import Document

doc = Document(
    metadata = {"source":"custom_id", "total_pages": 19,"page": 1 },
    page_content = "This is a sample document"
)

list_of_chunks = []
i = 0

for doc in split_pdf:
    output_obj = Output_format(
        id = f"{doc.metadata['source']}1_chunk{i+1}",
        text = doc.page_content,
        metadata_source = doc.metadata["source"],
        total_pages= doc.metadata["total_pages"],
        page_no= doc.metadata["page"]
        )
    #json_obj = output_obj.model_dump_json(indent = 3)
    json_obj_to_dict = output_obj.model_dump()
    i += 1 
    list_of_chunks.append(json_obj_to_dict)

#get_index_of_vectordb().upsert_records()

print(list_of_chunks[0])

batch_size = 96 
i=0

while(i<len(list_of_chunks)):
    try:
        if (batch_size > len(list_of_chunks)):
            insert_chunk = list_of_chunks[i: len(list_of_chunks) + 1]
            get_index_for_sparse().upsert_records(namespace= "RAG_application", records= insert_chunk)
            print(f"Successfully inserted chunks from {i+2} to {len(list_of_chunks)}")
            print("All chunks inserted successfully...")
            break
        insert_chunk = list_of_chunks[i:batch_size]
        get_index_for_sparse().upsert_records(namespace= "RAG_application", records= insert_chunk)
        print(f"Successgully inserted chunks from {i} to {batch_size}")
        i+=95
        batch_size += 95
    except Exception as e:
        print(f"Error: {e}")


input = input("Enter your question: ")

dict_input ={
    "text":input 
}

dense_res = get_index_for_dense().search(namespace = "RAG_application", 
                                   query = {
                                       "inputs": dict_input,
                                       "top_k": 5
                                   }, 
                                   fields= ["text","page_no"])

sparse_res = get_index_for_dense().search(namespace = "RAG_application", 
                                   query = {
                                       "inputs": dict_input,
                                       "top_k": 5
                                   }, 
                                   fields= ["text","page_no"])

print(dense_res)
print(sparse_res)

# def merge_res():

result = call_llm(question= input, rag_info= dense_res)

for word in result.choices[0].message.content:
    print(word, end="")
'''



















































# vecdb_index.upsert_records(namespace= "RAG_application", records= list_of_chunks)
'''
client = InferenceClient(
    provider = "nebius",
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    )

result = client.feature_extraction(
        split_pdf,
        model = embed_model_id,
    )

print(result)

print("Done generating the embeddings...")

class Output_format(BaseModel):
    id: str
    values: list 
    metadata: dict
    page_content: str

'''
