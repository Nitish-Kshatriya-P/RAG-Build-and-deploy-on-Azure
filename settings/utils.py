from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pydantic import BaseModel
from QA_System.__init__ import get_index_for_dense, get_index_for_sparse

# Custom output format for the chunks to be created from the pdf document.
class Op_format(BaseModel):
    id: str
    text: str
    metadata_source: str
    total_pages : int
    page_no : int

# Load the pdf document from the data folder.
def prep_pdf(file_name):
    loader = PyPDFLoader(f'Data/{file_name}')
    docs = loader.load()

# Split the data in pdf document into chunks of size 800 with an overlap of 50.
    ck_size= 800
    ck_overlap = 50
    splitter = RecursiveCharacterTextSplitter(chunk_size = ck_size, chunk_overlap = ck_overlap)
    pdf_chunks = splitter.split_documents(docs)

# Format the chunks into a list of dictionaries to be inserted into the vector database.
    doc_form  = Document(
        metadata = {"source": "RAG_application", "total_pages": 19, "page_no": 1},
        page_content = "This is a sample document",
    )

    list_of_chunks = []
    i = 0
    for chunk in pdf_chunks:
        output_obj = Op_format(
            id = f"{chunk.metadata['source']}1_chunk{i+1}",
            text = chunk.page_content,
            metadata_source = chunk.metadata["source"],
            total_pages= chunk.metadata["total_pages"],
            page_no = chunk.metadata["page"]
        )
        formatted_obj = output_obj.model_dump()
        i+=1
        list_of_chunks.append(formatted_obj)
    return list_of_chunks

# Below both the functions are used for inserting the chunks into the dense and sparse vector databases in pinecone.
def insert_chunks_dense(list_of_chunks: list):
    i = 0
    batch_size = 96
    try:
        while(i < len(list_of_chunks)):
            if (batch_size > len(list_of_chunks)):
                inserts = list_of_chunks[i:len(list_of_chunks)]
                get_index_for_dense().upsert_records(namespace="RAG_application", records = inserts)
                print(f"Successfully inserted batch {i} to {len(list_of_chunks)} into dense vector database")
                break
            inserts = list_of_chunks[i:batch_size]
            get_index_for_dense().upsert_records(namespace="RAG_application", records = inserts)
            print(f"Successfully inserted batch {i} to {batch_size} into dense vector database")
            i += 95
            batch_size += 95
        return print("All chunks inserted successfully into dense vector database...")
    except Exception as e:
        print("Error: {e}")
    
def insert_chunks_sparse(list_of_chunks: list):
    i = 0
    batch_size = 96
    try:
        while(i < len(list_of_chunks)):
            if (batch_size > len(list_of_chunks)):
                inserts = list_of_chunks[i:len(list_of_chunks)]
                get_index_for_sparse().upsert_records(namespace="RAG_application", records = inserts)
                print(f"Successfully inserted batch {i} to {len(list_of_chunks)} into sparse vector database")
                break
            inserts = list_of_chunks[i:batch_size]
            get_index_for_sparse().upsert_records(namespace="RAG_application", records = inserts)
            print(f"Successfully inserted batch {i} to {batch_size} into sparse vector database")
            i += 95
            batch_size += 95
        return print("All chunks inserted successfully into sparse vector database...")
    except Exception as e:
        print("Error: {e}")
    
def delete_records():
    get_index_for_dense().delete(delete_all= True, namespace = "RAG_application")
    get_index_for_sparse().delete(delete_all= True, namespace= "RAG_application")

    return print("All records deleted successfully from both the vector databases...")

