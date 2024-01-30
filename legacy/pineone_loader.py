from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os

EMBEDDINGS = 'sentence-transformers/all-MiniLM-L6-v2'
INDEX_NAME = "chatbotpdfs"

# initialize pinecone
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)

# load documents
def load_pdf_documents(path):
    loader = PyPDFDirectoryLoader(path)
    data = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=20)
    return splitter.split_documents(data)

# load embeddings
def load_embeddings(model_name):
    return HuggingFaceEmbeddings(model_name=model_name)

# create embeddings for each document
def create_embeddings_documents(docs, embeddings, index_name):
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    return docsearch

class PineconeLoader():
    def __init__(self, embeddings_model=EMBEDDINGS, index_name=INDEX_NAME, pdf_path=None):
        self.index_name = index_name
        self.embeddings = load_embeddings(embeddings_model)
        self.docs = load_pdf_documents(pdf_path)
        self.docsearch = create_embeddings_documents(self.docs, self.embeddings, self.index_name)

    def get_context(self, input, k=5):
        context = self.docsearch.similarity_search(input, k=k)
        return context

# ask question
path = "LLM/data"
question = "What is the difference between a trust and a will?"
loader = PineconeLoader(EMBEDDINGS, INDEX_NAME, pdf_path=path)
response = loader.get_context(question)
print(response)