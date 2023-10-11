from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
# from playsound import playsound
import os

load_dotenv(find_dotenv())

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

    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4) # Only look at the last 4 messages

    llm = OpenAI

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )

    return llm_chain

chain = load_chain()

while True:
    human_input = input("your message here")
    ai = chain.predict(human_input=human_input)
    print(ai)
