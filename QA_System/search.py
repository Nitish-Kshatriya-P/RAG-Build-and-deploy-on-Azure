# Here is the implemetation of hybrid search for a RAG application using 2 vector database in pinecone.
from QA_System.__init__ import get_index_for_dense, get_index_for_sparse

# Function to perform hybrid search by fetching data from both dense and sparse vector databases in pinecone and combining the results.
def hybrid_search(query: str):
    """
    For the given query the both vector dbs are searched and the results are combined.
    """
    dense_results = get_index_for_dense().search(
        namespace="RAG_application",
        query = {
            "inputs": {
                "text": query
                },
            "top_k": 5
        },
        fields= ["text","page_no"]
    )

    sparse_results = get_index_for_sparse().search(
        namespace="RAG_application",
        query = {
            "inputs": {
                "text": query
                },
            "top_k": 5
        },
        fields= ["text","page_no"]
    )
    # Removing the dupliactes with same 'id'
    deduplicate = {hit['_id']: hit for hit in dense_results["result"]["hits"] + sparse_results["result"]["hits"]}.values()
    # Sorting them based on the score in descending order
    sorted_hits = sorted(deduplicate, key = lambda x: x["_score"], reverse = True)
    # Formatting the final results with only the required fields
    final_results = [{'_id':hit['_id'], 'text': hit['fields']['text'], 'page_no': hit['fields']['text']} for hit in sorted_hits]
    return final_results


