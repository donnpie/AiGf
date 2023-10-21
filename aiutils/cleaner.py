# Various methods to clean textual data

import os
import fnmatch
from docx import Document # !pip install python-docx
import re
import chardet # !pip install chardet

### Working with MS Word docs
def find_docx_files(root_dir):
    """Find all the .docx files in a folder and its subfolders

    Args:
        root_dir (str): root folder location

    Returns:
        list[str]: list of absolute file path names
    """
    docx_files = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if fnmatch.fnmatch(file, "*.docx"):
                docx_files.append(os.path.join(root, file))

    return docx_files

def read_docx(file_path: str) -> None:
    """Read into memory a .docx file and prints contents to terminal

    Args:
        file_path (str): absolute file path and name
    """
    doc = Document()
    for paragraph in doc.paragraphs:
        print(paragraph.text)
        
def example_ms_doc_search():
    start_directory = r"C:\\Users\donnp\\OneDrive\\8. Poly"  # Replace with the path to the directory you want to search
    docx_files = find_docx_files(start_directory)

    if docx_files:
        print("Found .docx files:")
        for file in docx_files:
            print(file)
    else:
        print("No .docx files found in the specified directory and its subdirectories.")
        
def example_ms_doc_read():
    file_path = "your_document.docx"
    read_docx(file_path)
        
# A note on converting to json:
# When you convert text to JSON and then write it to a file using UTF-8 encoding, certain characters, especially special or non-ASCII characters, will be represented as Unicode escape sequences (e.g., "\u2014"). This is the standard way to encode such characters in JSON.
# For example, the character "—" (an em dash) is represented as "\u2014" in JSON because it's a Unicode character, and JSON uses this escape sequence format to represent characters that are not part of the basic ASCII character set.   
 
### Working with plain text docs    
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        confidence = result['confidence']

        return encoding, confidence

# Example usage
def example_detect_encoding():
    file_path = './aiutils/sample_text.txt'
    detected_encoding, confidence = detect_encoding(file_path)
    print(f"Detected encoding: {detected_encoding} with confidence: {confidence}")

def find_non_displayable_characters(file_path: str):
    """decode and reencode a file to check if there are any encoding issues

    Args:
        file_path (str): location of the file
    """
    with open(file_path, 'rb') as file:
        content = file.read()
        try:
            decoded_content = content.decode('utf-8')
            reencoded_content = decoded_content.encode('utf-8')
        except UnicodeDecodeError as e:
            # Handle the decoding error and print information about the problematic character
            print(f"UnicodeDecodeError: {e}")
            problem_character = content[e.start:e.end]
            print(f"Problematic character: {problem_character}")
            return

    print("NO non-displayable characters found.")
    
def example_find_non_displayable_characters():
    file_path = './aiutils/sample_text.txt'
    find_non_displayable_characters(file_path)

def remove_non_printable(text):
    # Define a regex pattern to match non-printable characters
    non_printable_pattern = re.compile(r'[^\x20-\x7E]+')

    # Use the pattern to replace non-printable characters with an empty string
    cleaned_text = non_printable_pattern.sub('', text)

    return cleaned_text

def example_remove_non_printable():
    text_with_non_printable = "This is a text\x07with non-printable\x1Bcharacters."
    cleaned_text = remove_non_printable(text_with_non_printable)
    print(cleaned_text)

def remove_non_ascii(text):
    # Use a list comprehension to filter out non-ASCII characters
    clean_text = ''.join(char for char in text if ord(char) < 128)
    return clean_text

def example_remove_non_ascii():
    text = "This is a text with non-ASCII characters: Café, rôle, façade."
    cleaned_text = remove_non_ascii(text)
    print(cleaned_text)
    
    # To convert to ascii json:
    # json_data = json.dumps({"text": cleaned_text}, ensure_ascii=False)
    # print(json_data)

# Usage example:
if __name__ == "__main__":
    
    # example_ms_doc_search()

    # example_detect_encoding()
    # example_find_non_displayable_characters()
    example_remove_non_ascii()