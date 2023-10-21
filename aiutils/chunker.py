# Provides predefined functions for chunking of plain text (.txt) docs

# Process:
# 1. Define a tokenizer
# 2. Define a length function
# 3. Set up the text splitter
# 4. Split the text
# 5. Add metadata
# 6. Optional, save to file

import tiktoken # !from aiutils import get_token_count
from uuid import uuid4
from datetime import date
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create tokenizer
def get_tokenizer_for_model(model_name: str):
    tokenizer_name = tiktoken.encoding_name_for_model(model_name) # Find the encoder for a given model
    return tiktoken.get_encoding(tokenizer_name)

# Create the length function
def get_length_function(tokenizer):
    """Returns the length function to be used in the text_splitter
    """
    def tiktoken_len(text_to_encode: str):
        tokens = tokenizer.encode(
            text_to_encode,
            disallowed_special=()
        )
        return len(tokens)

    return tiktoken_len


def tiktoken_len(text_to_encode: str):
    """Get the number of tokens in a piece of text. Use this function as the arg for length_function param in RecursiveCharacterTextSplitter. Ensure that tokenizer is declared outside the scope of this function."""
    tokens = tokenizer.encode(
        text_to_encode,
        disallowed_special=()
    )
    return len(tokens)

def get_token_count(text_to_encode: str, model_name: str):
    """Just a helper function. Don't use for chunking."""
    tokenizer_name = tiktoken.encoding_name_for_model(model_name) # Find the encoder for a given model
    tokenizer = tiktoken.get_encoding(tokenizer_name)
    tokens = tokenizer.encode(
        text_to_encode,
        disallowed_special=()
    )
    return len(tokens)

# Setup the text splitter
def get_text_splitter(length_function, chunk_size=500, chunk_overlap=20, separators=['\n\n', '\n', ' ', '']):
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        separators=separators
    )

# Get text from a file
def get_text_from_file(file_path: str) -> str:
    """Load text from a text file"""
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content

# Split the text using the text_splitter
def split_text(text, text_splitter):
    return text_splitter.split_text(text)

# Add metadata to all the chunks
def add_metadata(chunks):
    today = date.today().strftime("%Y-%m-%d")
    doc_id = f'{str(uuid4())}'
    return [
        {
            'doc_id': doc_id,
            'chunk_id': i,
            'date': today,
            'text': chunk
        } for i, chunk in enumerate(chunks)
    ]

# Optional: Save to file. Note the format is json lines (jsonl)
def save_to_jsonl_file(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item))
      
# Optional Combine the lines again (sometime you need to combine lines from multiple files)
# TODO: There is a bug in here that is still not fixed: JSONDecodeError: Expecting property name enclosed in double quotes: line 2 column 1 (char 2) or aJSONDecodeError: Extra data: line 1 column 2494 (char 2493)
def read_jsonl(file_path):
    documents = []

    with open(file_path, 'r') as f:
        for line in f:
            documents.append(json.loads(line))
            
    return documents

# To do the whole thing in one line
def chunk_and_save(chunker_setup_obj):
    
    model_name = chunker_setup_obj['model_name']
    input_file_path = chunker_setup_obj['input_file_path']
    output_file_path = chunker_setup_obj['output_file_path']
    
    tokenizer = get_tokenizer_for_model(model_name) # This is used indirectly in text_splitter
    length_function = get_length_function(tokenizer)
    text_splitter = get_text_splitter(length_function)
    text = get_text_from_file(input_file_path)
    chunks = split_text(text, text_splitter)
    # print(f'len(chunks): {len(chunks)}')
    data = add_metadata(chunks)
    print(data)
    save_to_jsonl_file(data, output_file_path)
        
if __name__ == "__main__":
# Typical usage:

    # #Specify the model 
    # model_name = 'gpt-3.5-turbo'
    
    # # Define tokenizer
    # tokenizer = get_tokenizer_for_model(model_name)
    
    # # Define lenght function
    # length_function = tiktoken_len
    
    # # Set up the text splitter function
    # text_splitter = get_text_splitter(length_function)
    
    # # Get text to be chunked
    # input_file_path = "./aiutils/sample_text.txt"
    # text = get_text_from_file(input_file_path)
    
    # # Split the text
    # chunks = split_text(text, text_splitter)
    
    # # Inspect
    # len(chunks)
    
    # # Add metadata to chunks
    # data = add_metadata(chunks)
    # print(data)
    
    # # Optional: save to file
    # input_file_path = './aiutils/training_data.jsonl'
    # save_to_jsonl_file(data, input_file_path)
    
    # Optional read file into memory
    # documents = read_jsonl('training_data.jsonl')
    
    # Inspect
    # len(documents)
    
    # Test the get_token_count func
    # print(get_token_count(text, 'gpt-3.5-turbo'))  
    
    # To do the whole thing in two lines
    chunker_setup_obj = {
        'model_name': 'gpt-3.5-turbo',
        'input_file_path': "./aiutils/sample_text.txt",
        'output_file_path': './aiutils/training_data.jsonl'
    }
    
    chunk_and_save(chunker_setup_obj)