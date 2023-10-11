from dotenv import find_dotenv, load_dotenv

# You need a paid OpenAi subscription to generate a valid API key
load_dotenv(find_dotenv())

model_name = "text-davinci-003",
temperature = 0.7,
max_tokens = 1000,
top_p = 1,
frequency_penalty = 0,
presence_penalty = 0,
n = 1,
best_of = 1,
model_kwargs = dict(), # Dict[str, Any]

batch_size = 20

# Create ChatMessage (takes in multiple messages, returns a single message)
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.chains import ConversationChain
# from langchain.schema import HumanMessage

model_name="gpt-3.5-turbo" #"gpt-3.5-turbo-instruct"

llm = OpenAI(
    # model_name=model_name,
    # temperature = temperature,
    # max_tokens=max_tokens,
    # top_p=top_p,
    # frequency_penalty=frequency_penalty,
    # presence_penalty=presence_penalty,
    # n=n,
    # best_of=best_of,
    # model_kwargs=model_kwargs, # Dict[str, Any]
    openai_api_key=openai_api_key,
    # batch_size=batch_size
)

memory = ConversationalBufferWindowMemory()

conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=memory
)

# print(conversation.prompt.template)










# messages = [HumanMessage(content=prompt_template_product)]

# output = llm.predict_messages(messages)
# print(output)
