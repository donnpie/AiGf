# Usefull code to manage the pinecone db

import pinecone
from embedder import load_keys

if __name__ == '__main__':
    index_name = 'langchain-retrieval-augmentation' # Specify the index a name

    # Load environment variables
    keys = load_keys()

    # Initialise the pinecone client object
    pinecone.init(
        api_key=keys['PINECONE_API_KEY'],
        environment=keys['PINECONE_ENVIRONMENT']
    )

    # Retrieve the index
    index = pinecone.Index(index_name)
    
    # # Get a list of all IDs from the index - Doesn't work
    # all_ids = index.list_index()
    
    query_response = index.query(
        top_k=27,
        id='2d1ac156-6855-4d01-8786-336d6b2858aa'
    )
    
    # print(query_response)
    
    # build a list of id's to delete
    ids = list()
    
    for item in query_response['matches']:
        ids.append(item['id'])
        
    print(ids)
    
    
    # Sample code
    # query_response = index.query(
    #     namespace='example-namespace',
    #     top_k=10,
    #     include_values=True,
    #     include_metadata=True,
    #     vector=[0.1, 0.2, 0.3, 0.4],
    #     filter={
    #         'genre': {'$in': ['comedy', 'documentary', 'drama']}
    #     }
    # )

    # # DELETE EVERYTHING
    # index.delete(delete_all=True) # Doesn't work on free version
    # delete_response = index.delete(ids=ids)
    # print(delete_response)
    