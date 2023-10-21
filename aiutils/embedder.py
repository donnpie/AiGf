# Helper functions for doing vector embeddings

from chunker import add_metadata, get_length_function, get_text_from_file, get_text_splitter, get_tokenizer_for_model, split_text
from cleaner import clean_the_text, extract_metadata_for_docx, find_docx_files, get_docs_and_clean, get_docx_text
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from uuid import uuid4
import os
import pinecone # !install pinecone-client





### Test code ###
if __name__ == '__main__':
    model_name = 'gpt-3.5-turbo'
    embedding_model_name = 'text-embedding-ada-002'
    # input_file_path = "./aiutils/sample_text.txt"
    docx_start_directory = r"C:\\Users\donnp\\OneDrive\\8. Poly"
    
    # Load environment variables
    load_dotenv(find_dotenv())
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
    
    # Create embedder object
    embedder = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=embedding_model_name
    )
    
    # Prepare the text splitter
    tokenizer = get_tokenizer_for_model(model_name)
    length_function = get_length_function(tokenizer)
    text_splitter = get_text_splitter(length_function)
    
    # Initialise the pinecone client object
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    
    # Give the index a name
    index_name = 'langchain-retrieval-augmentation'
    
    dimension = 1536 # 1536 dim of text-embedding-ada-002
    
    # Create the index if it does not exist
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            metric='cosine',
            dimension=len(dimension)
        )
        
    # Retrieve the index
    # index = pinecone.GRPCIndex(index_name)
    index = pinecone.Index(index_name)

    # Inspect the index
    # index.describe_index_stats()
    
    # Prepare the data and metadata
    documents = []
    metadata = []
    docx_files = find_docx_files(docx_start_directory)
    
    for file_path in docx_files:
        text = get_docx_text(file_path)
        cleaned_text = clean_the_text(text)
        documents.append(cleaned_text)
        metadata.append(extract_metadata_for_docx(file_path))
        
    # return documents
    
    # print(documents)
    # print(metadata)
    
    batch_limit = 100
    ids = []
    embeddings = []
    metadatas = []
    
    # main loop
    for i, document in enumerate(documents):
        
        # Set the metadata for the document. This will be common for all chunks belonging to this document
        document_metadata = metadata[i]
        
        # Chunk up the doc
        chunks = split_text(document, text_splitter)
        
        # Create id numbers for chunks
        chunk_ids = [str(uuid4()) for _ in range(len(chunks))]

        # Embed the chunks
        chunk_embeddings = embedder.embed_documents(chunks)
        
        # Prepare metadata for chunks
        chunk_metadatas = [{
            "chunk_num": j, 
            "text": chunk, 
            **document_metadata
        } for j, chunk in enumerate(chunks)]
        
        # append these to current batches
        # Why do we add chunks to metadata and texts?
        ids.extend(chunk_ids)
        embeddings.extend(chunk_embeddings)
        metadatas.extend(chunk_metadatas)
        
        # Inspect
        # print(len(ids))
        # print(len(embeddings))
        # print(len(metadatas))
        # print()
        
        # if we have reached the batch_limit we can add texts
        if len(ids) >= batch_limit:
            index.upsert(vectors=zip(ids, embeddings, metadatas))

        #     # Reset the lists
            ids = []
            embeddings = []
            metadatas = []
    
    # Catch the last few chunks
    index.upsert(vectors=zip(ids, embeddings, metadatas))
    
    
    # print(len(ids))
    # print(len(embeddings))
    # print(len(metadatas))
    
    # print(ids)
    # print()
    # print(embeddings)
    # print()
    # print(metadatas)
        
     
