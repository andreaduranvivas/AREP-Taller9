import bs4
from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os

os.environ["OPENAI_API_KEY"] = "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"

"""
    Carga documentos de un sitio web, los divide en fragmentos y los almacena en un vectorstore.
    Luego, utiliza un modelo de chat para responder preguntas basadas en el contexto recuperado.

    Raises:
        Exception: Si ocurre un error al cargar los documentos, al interactuar con el vectorstore,
                   o al realizar la búsqueda.
"""
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(splits[0])
print(splits[1])

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


def format_docs(docs):
    """
    Formatea los documentos recuperados de la base de datos vectorial.

    Esta función toma una lista de documentos y devuelve una cadena de texto que contiene el contenido de todos los documentos,
    separados por dos saltos de línea.

    Args:
        docs (list): Una lista de documentos recuperados de la base de datos vectorial.

    Returns:
        str: Una cadena de texto que contiene el contenido de todos los documentos, separados por dos saltos de línea.
    """
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("What is Task Decomposition?")

print(response)