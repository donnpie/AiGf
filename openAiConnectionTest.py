# Purpose: To make a basic call to OpenAi API to confirm that it is working

# To install LangChain: https://python.langchain.com/docs/get_started/installation
# Quick start: https://python.langchain.com/docs/get_started/quickstart

from dotenv import find_dotenv, load_dotenv

# You need a paid OpenAi subscription to generate a valid API key
load_dotenv(find_dotenv())

# Model parameters:
# For parameter details see https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAI.html

# For model index and pricing see https://openai.com/pricing
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

# Create LLM (returns a single completion)
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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
    # openai_api_key=openai_api_key,
    # batch_size=batch_size
)

# output = llm('What is an LLM?')
# print(output)

prompt_template_product = PromptTemplate(
    input_variables=['product'],
    template="What would be a good company name for a company that makes colorful {product}?"
)

# prompt_template_product.format(product="cars")

chain = LLMChain(llm=llm, prompt=prompt_template_product)
print(chain.run("cars"))
exit()

