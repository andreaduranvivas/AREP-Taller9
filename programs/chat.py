from langchain.chains import LLMChain
#from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

import os

"""
    Envía una pregunta a ChatGPT y recupera la respuesta.

    Utiliza la biblioteca langchain para interactuar con el modelo de lenguaje de ChatGPT.
    La pregunta se envía como un indicador y se recupera la respuesta generada por el modelo.

    Args:
        question (str): La pregunta a enviar a ChatGPT.

    Returns:
        str: La respuesta generada por ChatGPT.

    Raises:
        Exception: Si ocurre un error al interactuar con el modelo de lenguaje.
"""

os.environ["OPENAI_API_KEY"] = "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"

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI()

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What is at the core of Popper's theory of science?"

response = llm_chain.run(question)

print(response)
