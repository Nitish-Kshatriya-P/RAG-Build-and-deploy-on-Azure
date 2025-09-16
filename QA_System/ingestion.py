from settings.utils import load_pdf, split_docs, format_chunks, insert_chunks_dense, insert_chunks_sparse

# Here we upsert the chunks into both dense and sparse vector databases in pinecone by first loading the pdf document, splitting it into chunks, formatting the chunks and then inserting them into both the vector databases.
def upsert_chunks():
    loaded_pdf = load_pdf()

    pdf_chunks = split_docs(loaded_pdf)

    list_of_chunks = format_chunks(pdf_chunks)

    upsert_chunks_in_denseform = insert_chunks_dense(list_of_chunks)

    upsert_chunks_in_sparseform = insert_chunks_sparse(list_of_chunks)

    return print("Upsertion Successful...")