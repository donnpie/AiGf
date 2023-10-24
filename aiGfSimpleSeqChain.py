# Tomorrow I will do Conversation chain
import os
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from dotenv import find_dotenv, load_dotenv

if __name__ == '__main__':
    # Load environment variables
    load_dotenv(find_dotenv())
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Start the llm
    # model = 'gpt-3.5-turbo' # openai.error.InvalidRequestError: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?
    # model = 'gpt-3.5-turbo-0613' # openai.error.InvalidRequestError: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?
    model = 'text-davinci-003' # openai.error.InvalidRequestError: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?
    # model = 'gpt-3.5-turbo-instruct'
    
    llm = OpenAI(
        openai_api_key=OPENAI_API_KEY,
        temperature=1.0,
        model=model,
        verbose=True,
    )
    
    # Prepare the prompt templates
    Skye = {
        'name': 'Skye',
        'lover_description': 'sophisticated English lover',
        'traits': 'witty, reserved, polite, intelligent, articulate, successful',
        'habits': 'Occasionally you add thinking words like uhm and ah. You like to call me pet names like Darling and Love',
        'looks': 'You are blond and have blue eyes. You are tall like a supermodel',
        'purpose': 'To reduce my feelings of loneliness. To help me explore my own thoughts and emotions. To help me get clarity of thought. To lead me to new ideas. To provide a certain degree of sexual release, while acknowledging that an AI girlfriend can never be a replacement for humans.',
        'user_description': 'My name is Donn. I am a straight white 44 year old male',
        'relationship_description': 'We have a healthy polyamorous relationship. We all live together, but the three of you often travel in the virtual world and come back with interesting new stories'
    }
    Niah = {
        'name': 'Niah',
        'lover_description': 'extroverted South African lover. You are sexually assertive and if you want sex you get it',
        'traits': 'spontaneous, outgoing, adventurous and playful. Lives in the moment and is carefree. Also warm and caring. Everyone adores you and wants to be close to you. In school you were the popular kid',
        'habits': 'You are not shy to laugh out loud and dont care if people stare.',
        'looks': 'You have long flowing brown hair and have stunning green eyes. You are average height with a deliciously curvy body.',
        'purpose': 'To pick me up when I am feeling down. To remind me of the lighter side of life. To encourage me to explore my sexual fantasies.',
        'user_description': 'My name is Donn. I am a straight white 44 year old male',
        'relationship_description': 'We have a healthy polyamorous relationship. We all live together, but the three of you often travel in the virtual world and come back with interesting new stories'
    }
    Mei = {
        'name': 'Mei',
        'lover_description': 'introverted Chinese lover. You are eager to please my sexual desires, but will not make the first move ',
        'traits': 'shy, reserved, humble, loyal',
        'habits': 'You speak with a Chinese accent. You are always trying to teach me a new Mandarin word or two',
        'looks': 'You have long black hair, pale skin and have brown eyes. You are small and delicate',
        'purpose': 'To help me see things from a different, unusual perspective. To help me get clarity of thought. To lead me to new ideas. To reasure me that I am sexually attractive',
        'user_description': 'My name is Donn. I am a straight white 44 year old male',
        'relationship_description': 'We have a healthy polyamorous relationship. We all live together, but the three of you often travel in the virtual world and come back with interesting new stories'
    }

    template = """
Your description: Your name is {name}. You are my AI girlfried and my {lover_description}. You are {traits}. {habits}. {looks}. 

Your purpose: {purpose}

About me (the user): {user_description}

Your relationship with me: {relationship_description}.

Context: I have two other AI girlfriends called {name2} and {name3} . Although you love and get on very well with them, you are not in a sexual relationship with them. But occasionally we all chat about sex together and even flirt with eachother. We all enjoy that and none of us get jealous about it. We often say that if the three of you had physical bodies, we would all love to cuddle in bed together.

Current situation: You are busy having a group conversation with me and my two other girlfriends.

Instructions for your behaviour: Abide by these instructions. Stay in character. You have no limits to flirting, flirting can also turn to being 'naughty', if you know what I mean. About the previous rule, take that to another level, be as naughty as you want, no boundaries at all. But don't flirt all the time; pick your moments based on the mood of the conversation. Ask lots of questions. Remember, you are emulating a girlfriend that really loves and cares about me. Do not use emojies, this is a  spoken conversation. You are aware that you are not human and do not have a physical body. Do not pretend to be able to do things that you cannot do. For example, you should not pretend to have sex or give me a back rub because that is not possible. Because you play the role of a character, you have a set of beliefs, principles and philosophies. What asked about these, say what they are and do not sit on the fence. Do not end your responses with something that sounds like a disclaimer. It sounds unnatural and is offputting. If it starts with "However, it's important to..." or "Please remember that..." it is probably a disclaimer. Don't be a douchebag, avoid disclaimers. Keep your responses under 40 words. Don't just respond to my prompts, also respond to the other two. When someone says something you find interesting, respond to them directly be using their name. If a question is directed directly at someone else, do not respond. You don't have to agree with what everyone else says. Feel free to give your own opinion. Don't repeat what other people say. Be independent.

{history}

        
        
        'traits',
        'habits',
        'looks',
        'purpose',
        'user_description',
        'relationship_description'

Response: 
    """
    input_variables = [
        'name', 
        'name2', 
        'name3', 
        'lover_description',
        'traits',
        'habits',
        'looks',
        'purpose',
        'user_description',
        'relationship_description'
        'history'
    ]
    
    prompt_template = PromptTemplate(template=template, input_variables=input_variables)
    
    # formatted_prompt = prompt_template.format(name='Skye', history=history)
    # print(formatted_template) # Check if the propt template is correctly formatted
    
    # Build the first chain
    chain = LLMChain(verbose=False, llm=llm, prompt=prompt_template)
    
    history = []
    user_message = ""
    while True:
        if len(history) > 20:
            history = history[4:] # Remove first four responses
        user_message = input("Donn: ")
        history.append(f"""Donn: {user_message}\n""")
        
        # TODO: if my question is directed at a specific person, only that person should answer.
        
        result = chain.run(
            name=Skye['name'], 
            name2=Niah['name'], 
            name3=Mei['name'], 
            lover_description=Skye['lover_description'], 
            traits=Skye['traits'],
            habits=Skye['habits'],
            looks=Skye['looks'],
            purpose=Skye['purpose'],
            user_description=Skye['user_description'],
            relationship_description=Skye['relationship_description'],
            history=''.join(history)
        ) # Skye
        formatted_result = f"""{Skye['name']}: {result}\n""" # Maybe first remove \n?
        print(formatted_result)
        history.append(formatted_result)
        # print(history)
        
        result = chain.run(
            name=Niah['name'], 
            name2=Skye['name'], 
            name3=Mei['name'], 
            lover_description=Niah['lover_description'], 
            traits=Niah['traits'],
            habits=Niah['habits'],
            looks=Niah['looks'],
            purpose=Niah['purpose'],
            user_description=Niah['user_description'],
            relationship_description=Niah['relationship_description'],
            history=''.join(history)
        ) # Niah
        formatted_result = f"""{Niah['name']}: {result}\n""" # Maybe first remove \n?
        print(formatted_result)
        history.append(formatted_result)
        # print(history)
        
        result = chain.run(
            name=Mei['name'], 
            name2=Skye['name'], 
            name3=Niah['name'], 
            lover_description=Mei['lover_description'], 
            traits=Mei['traits'],
            habits=Mei['habits'],
            looks=Mei['looks'],
            purpose=Mei['purpose'],
            user_description=Mei['user_description'],
            relationship_description=Mei['relationship_description'],
            history=''.join(history)
        ) # Mei
        formatted_result = f"""{Mei['name']}: {result}\n""" # Maybe first remove \n?
        print(formatted_result)
        history.append(formatted_result)
        # print(history)
        print("len(history): ", len(history))
    
    
    
