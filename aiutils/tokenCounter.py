import tiktoken

# import like this:
# from aiutils import get_token_count

# create the length function
def get_token_count(text_to_encode: str, model_name: str):
    tokenizer_name = tiktoken.encoding_name_for_model(model_name) # Find the encoder for a given model
    tokenizer = tiktoken.get_encoding(tokenizer_name)
    tokens = tokenizer.encode(
        text_to_encode,
        disallowed_special=()
    )
    return len(tokens)

tokenizer_name = tiktoken.encoding_name_for_model('gpt-3.5-turbo') # Find the encoder for a given model
tokenizer = tiktoken.get_encoding(tokenizer_name)

def tiktoken_len(text_to_encode: str):
    """Get the number of tokens in a piece of text. Use this function as the arg for length_function param in RecursiveCharacterTextSplitter"""
    tokens = tokenizer.encode(
        text_to_encode,
        disallowed_special=()
    )
    return len(tokens)

if __name__ == "__main__":
    text = "Life is struggle"
    print(get_token_count(text, 'gpt-3.5-turbo'))  