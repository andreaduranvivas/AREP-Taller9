from langchain_community.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "9f8cc1f5-ab1e-4abb-818c-d8faf41ad1eb"
os.environ["PINECONE_ENV"] = "gcp-starter"

def loadText():
    """
    Carga documentos de texto, los divide en fragmentos y los almacena en Pinecone.

    Este proceso incluye la carga de documentos desde un archivo, la división de los documentos en fragmentos
    utilizando un text splitter, y el almacenamiento de estos fragmentos en Pinecone para permitir búsquedas
    basadas en similitud de vectores de embeddings.

    Raises:
        Exception: Si ocurre un error al cargar los documentos, al interactuar con Pinecone,
                   o al crear el índice en Pinecone.
    """
    loader = TextLoader("../resources/Conocimiento.txt")
    documents = loader.load()
    #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
        is_separator_regex = False,
    )


    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    import pinecone


    index_name = "langchain-demo"
    pc = Pinecone(api_key='9f8cc1f5-ab1e-4abb-818c-d8faf41ad1eb')

    print(pc.list_indexes())

    # First, check if our index already exists. If it doesn't, we create it
    if len(pc.list_indexes())==0:
        # we create a new index
        #pc.create_index(name=index_name, metric="cosine", dimension=1536)
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=PodSpec(
                environment=os.getenv("PINECONE_ENV"),
                pod_type="p1.x1",
                pods=1
            )
        )

    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

def search():
    """
    Realiza una búsqueda de similitud en Pinecone para encontrar documentos relevantes a una consulta dada.

    Utiliza un índice existente en Pinecone para buscar documentos que sean similares a la consulta proporcionada.
    Imprime el contenido del primer documento encontrado que es más relevante.

    Args:
        query (str): La consulta para la búsqueda de similitud.

    Raises:
        Exception: Si ocurre un error al interactuar con Pinecone o al realizar la búsqueda.
    """
    embeddings = OpenAIEmbeddings()

    index_name = "langchain-demo"
    # if you already have an index, you can load it like this
    docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

    query = "Who is Sherlock Holmes?"
    docs = docsearch.similarity_search(query)

    print(docs[0].page_content)

loadText()
search()