# Helper functions for doing vector embeddings

from chunker import get_length_function, get_text_splitter as get_splitter, get_tokenizer_for_model, split_text
from cleaner import clean_the_text, extract_metadata_for_docx, find_docx_files, get_docx_text
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from uuid import uuid4
import os
import pinecone # !install pinecone-client

# Load environment variables
def load_keys():
    """Load environment variables
    """
    keys = dict()
    load_dotenv(find_dotenv())
    keys['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    keys['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
    keys['PINECONE_ENVIRONMENT'] = os.getenv('PINECONE_ENVIRONMENT')
    
    return keys

# Prepare the text splitter
def get_text_splitter(model_name: str):
    """Prepare the text splitter

    Args:
        model_name (str): Model name using for chat eg 'gpt-3.5-turbo'

    Returns:
        text_splitter: A text splitter function
    """
    tokenizer = get_tokenizer_for_model(model_name)
    length_function = get_length_function(tokenizer)
    text_splitter = get_splitter(length_function)
    
    return text_splitter

# Create the index if it does not exist
def create_index_if_not_exist(index_name: str, dimension: int):
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            metric='cosine',
            dimension=len(dimension)
        )

# Get documents and metadata
def get_documents_and_metadata(docx_files: list[str]):
    """_summary_

    Args:
        docx_files (list[str]): List of absolute file paths and names

    Returns:
        _type_: List of document texts and list of metadata for each document
    """
    for file_path in docx_files:
        text = get_docx_text(file_path)
        cleaned_text = clean_the_text(text)
        documents.append(cleaned_text)
        metadata.append(extract_metadata_for_docx(file_path))
        
    return documents, metadata

def prepare_docs_and_upsert(documents: list[str], metadata: list, text_splitter, embedder, index):
    
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

            # Reset the lists
            ids = []
            embeddings = []
            metadatas = []
    
    # Catch the last few chunks
    index.upsert(vectors=zip(ids, embeddings, metadatas))

### Test code ###
if __name__ == '__main__':
    
    # Set the settings
    model_name = 'gpt-3.5-turbo'
    embedding_model_name = 'text-embedding-ada-002'
    docx_start_directory = r"C:\\Users\donnp\\OneDrive\\8. Poly"
    index_name = 'langchain-retrieval-augmentation' # Give the index a name
    dimension = 1536 # 1536 dim of text-embedding-ada-002
    batch_limit = 100 # Max number of chunks to upsert in one batch
    
    # Load environment variables
    keys = load_keys()
    
    # Create embedder object
    embedder = OpenAIEmbeddings(
        openai_api_key=keys['OPENAI_API_KEY'],
        model=embedding_model_name
    )
    
    # Prepare the text splitter
    text_splitter = get_text_splitter(model_name)
    
    # Initialise the pinecone client object
    pinecone.init(
        api_key=keys['PINECONE_API_KEY'],
        environment=keys['PINECONE_ENVIRONMENT']
    )
    
    # Create the index if it does not exist
    create_index_if_not_exist(index_name, dimension)
        
    # Retrieve the index
    index = pinecone.Index(index_name)

    # Inspect the index
    # index.describe_index_stats()
    
    # Prepare the data and metadata
    documents = []
    metadata = []
    docx_files = find_docx_files(docx_start_directory)
    
    # Get documents and metadata
    documents, metadata = get_documents_and_metadata(docx_files)

    # Inspect    
    # print(documents)
    # print(metadata)
    
    # Run the main loop
    prepare_docs_and_upsert(documents, metadata, text_splitter, embedder, index)
    