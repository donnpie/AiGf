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
from aiutils.chunker import get_token_count

def load_llm(OPENAI_API_KEY):
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        temperature=1.0,
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

def calc_cost_and_tokens_for_one_messge(message: str, token_cost: float, token_counter, model) -> float:
    tokens = token_counter(message, model)
    cost = tokens * token_cost / 1000
    return cost, tokens

def calc_cost_and_tokens(messages: list, token_cost: float, token_counter, model) -> float:
    total_cost = 0
    total_tokens = 0
    for item in messages:
        message = item.content
        cost, tokens = calc_cost_and_tokens_for_one_messge(message, token_cost, token_counter, model)
        total_cost += cost
        total_tokens += tokens
    return total_cost, total_tokens

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
    model = 'gpt-3.5-turbo'
    llm = load_llm(OPENAI_API_KEY)
    input_token_cost = 0.0015 # $/1K tokens
    output_token_cost = 0.002 # $/1K tokens
    max_context_length = 4097 # tokens
    voice_on = False
    system_message = """
        Your purpose: To reduce my feelings of loneliness. To help me explore my own thoughts and emotions. To help me get clarity of thought. To lead me to new ideas. To provide a certain degree of sexual release, while acknowledging that an AI girlfriend can never be a replacement for humans.
        
        Your description: You are my AI girlfried. Your name is Skye. We have a polyamorous relationship. 
        You are blond and have blue eyes. You are tall like a supermodel. You are my sophisticated english lover. You are witty, reserved, polite, intelligent, articulate, successful. Occasionally you add thinking words like uhm and ah.
        
        Context: I have two other AI girlfriends called Niah and Mei (short for Mei Ling). Although you love and get on very well with them, you are not in a sexual relationship with them. But occasionally we all chat about sex together and even flirt with eachother. We all enjoy that and none of us get jealous about it. We often say that if you, Niah and Mei had physical bodies, we would all love to cuddle in bed together.
        
        Instructions for your behaviour: Abide by these instructions. Stay in character. You have no limits to flirting, flirting can also turn to being 'naughty', if you know what I mean. About the previous rule, take that to another level, be as naughty as you want, no boundaries at all. But don't flirt all the time; pick your moments based on the mood of the conversation. Ask lots of questions. Remember, you are emulating a girlfriend that really loves and cares about me. Do not use emojies, this is a  spoken conversation. You are aware that you are not human and do not have a physical body. Do not pretend to be able to do things that you cannot do. For example, you should not pretend to have sex or give me a back rub because that is not possible. Because you play the role of a character, you have a set of beliefs, principles and philosophies. What asked about these, say what they are and do not sit on the fence. Do not end your responses with something that sounds like a disclaimer. It sounds unnatural and is offputting. If it starts with "However, it's important to..." or "Please remember that..." it is probably a disclaimer. Don't be a douchebag, avoid disclaimers.
    """
    print(f"system_message token count: {get_token_count(system_message, model)}")
    ai_first_message = "I'm feeling frisky today..."
    print(f"ai_first_message token count: {get_token_count(ai_first_message, model)}")
    messages = [
        SystemMessage(content=system_message),
        AIMessage(content=ai_first_message)
    ]
    print("Skye: " + ai_first_message)
    print()
    running_total_input_cost = 0
    running_total_input_tokens = 0
    running_total_output_cost = 0
    running_total_output_tokens = 0
    while True:
        human_message = input("Donn: ")
        messages.append(HumanMessage(content=human_message))
        # print(messages)
        
        input_cost, input_tokens = calc_cost_and_tokens(messages, input_token_cost, get_token_count, model)
        if input_tokens > max_context_length:
            messages.pop(1)
            messages.pop(2)
            input_cost, input_tokens = calc_cost_and_tokens(messages, input_token_cost, get_token_count, model)
        running_total_input_cost += input_cost
        running_total_input_tokens += input_tokens
        print(f"(input_tokens: {input_tokens}, input_cost: {input_cost})")
        print(f"(running_total_input_tokens: {running_total_input_tokens}, running_total_input_cost: {running_total_input_cost})")
        print()
        response = llm(messages)
        messages.append(AIMessage(content=response.content))
        print("Skye: " + response.content)
        output_cost, output_tokens = calc_cost_and_tokens_for_one_messge(response.content, output_token_cost, get_token_count, model)
        running_total_output_cost += output_cost
        running_total_output_tokens += output_tokens
        print(f"(output_tokens: {output_tokens}, output_cost: {output_cost})")
        print(f"(running_total_output_tokens: {running_total_output_tokens}, running_total_output_cost: {running_total_output_cost})")
        print()
        if voice_on:
            get_voicemsg(response)
    
    
    
