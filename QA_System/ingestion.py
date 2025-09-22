from settings.utils import prep_pdf, insert_chunks_dense, insert_chunks_sparse

# Here we upsert the chunks into both dense and sparse vector databases in pinecone by first loading the pdf document, splitting it into chunks, formatting the chunks and then inserting them into both the vector databases.
def upsert_chunks(pdf_path):
    list_of_chunks = prep_pdf(file_name= pdf_path)
    print("3")
    upsert_chunks_in_denseform = insert_chunks_dense(list_of_chunks)
    print("4")
    upsert_chunks_in_sparseform = insert_chunks_sparse(list_of_chunks)
    print("5")
    return print("Upsertion Successful...")