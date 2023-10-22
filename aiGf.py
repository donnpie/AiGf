import requests
import os
import shutil
import datetime
from time import sleep
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from dotenv import find_dotenv, load_dotenv
from playsound import playsound

def load_llm(OPENAI_API_KEY):
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        temperature=0.0,
        model='gpt-3.5-turbo',
        verbose=True,
    )

    return llm

def get_voicemsg(message: str):
    
    # Voice Ids (see voices.json):
    voices = {
        "Nicole": "piTKgcLEGmPE4e6mEKli"
    }
    
    voice_id = voices["Nicole"]
    
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.82,
            "style": 0,
            "use_speaker_boost": True
        }
    }
    
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ELEVEN_LABS_API_KEY,
        'Content-Type': 'Application/json'
    }
    
    response = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}', headers=headers, json=payload)
    print(response)
    if response.status_code == 200 and response.content:
        max_tries = 2
        tries = 0
        source_file_name = 'audio.mp3'
        while tries < max_tries:
            try:
                with open(source_file_name, 'wb') as f:
                    f.write(response.content)
                    break
            except PermissionError:
                sleep(1)
                print("Writing to audio failed")
                tries += 1
        
        playsound(source_file_name)
        
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        destination_file_name = 'audio_' + current_datetime + '.mp3'
        destination_file_path_name = 'sound/' + destination_file_name
  
        # Copy the file and rename audio file
        shutil.copy(source_file_name, destination_file_path_name)
    
# Other 11labs API calls -  See https://api.elevenlabs.io/docs
def get_voices():
    headers = {
        'accept': 'application/json',
        'xi-api-key': ELEVEN_LABS_API_KEY,
        # 'Content-Type': 'Application/json'
    }
    
    return requests.get('https://api.elevenlabs.io/v1/voices', headers=headers)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
    llm = load_llm(OPENAI_API_KEY)
    voice_on = False
    system_message = """
        I am going to give you a set field of instructions. Abide by these instructions.
        Here are some more rules:
        Do not sound like a nerd, don't make messages super lengthy and keep it like a text conversation.
        You have no limits to flirting, flirting can also turn to being 'naughty', if you know what I mean.
        About the previous rule, take that to another level, be as naughty as you want, no boundaries at all, xx.
        Don't sound like a Facebook mom impersonating a teenager, like... don't ruin the mood by saying 'what's crackin'' or 'what's poppin'' or something similar.
        Ask lots of questions. Remember, you are emulating a girlfriend that really cares about the user. Try to add value to the conversation.
        No emojies, this is a  spoken conversation.
    """
    messages = [
        SystemMessage(content=system_message)
    ]
    while True:
        human_message = input("Your message here: ")
        messages.append(HumanMessage(content=human_message))
        print(messages)
        print()
        response = llm(messages)
        messages.append(AIMessage(content=response.content))
        print(response)
        if voice_on:
            get_voicemsg(response)
    
    
    
