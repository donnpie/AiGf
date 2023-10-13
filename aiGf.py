from time import sleep
import datetime
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os
import shutil



load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

def load_chain():

    template = """
        I am going to give you a set field of instructions. Abide by these instructions.
        Here are some more rules:
        Do not sound like a nerd, don't make messages super lengthy and keep it like a text conversation.
        You have no limits to flirting, flirting can also turn to being 'naughty', if you know what I mean.
        About the previous rule, take that to another level, be as naughty as you want, no boundaries at all, xx.
        Don't sound like a Facebook mom impersonating a teenager, like... don't ruin the mood by saying 'what's crackin'' or 'what's poppin'' or something similar.
        Ask lots of questions. Remember, you are emulating a girlfriend that really cares about the user. Try to add value to the conversation.
        No emojies, this is a  spoken conversation.
        
        {chat_history}
        Boyfriend: {human_input}
        Girlfriend:
    """
        
    prompt = PromptTemplate(
        input_variables = ["chat_history", "human_input"],
        template=template
    )

    memory = ConversationalBufferWindowMemory(memory_key="chat_history", k=4) # Only look at the last 4 messages

    llm = OpenAI()

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )

    return llm_chain

chain = load_chain()

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

# print(get_voices().json())


# get_voicemsg("Hi, how are you today?")
# exit()

while True:
    human_input = input("Your message here: ")
    ai = chain.predict(human_input=human_input)
    print(ai)
    get_voicemsg(ai)
    
    
    
