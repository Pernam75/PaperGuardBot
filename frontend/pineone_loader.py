from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain import PromptTemplate
import pinecone
import os

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
def create_embeddings(docs, embeddings, index_name):
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    return docsearch

class PineconeLoader():
    def __init__(self, pdf_path, embeddings_model, index_name):
        self.docs = load_pdf_documents(pdf_path)
        self.embeddings = load_embeddings(embeddings_model)
        self.index_name = index_name
        self.docsearch = create_embeddings(self.docs, self.embeddings, self.index_name)

    def query(self, question):
        response = self.docsearch.similarity_search(question, k=4)
        return response

# # ask question
# docs = 'pdfs'
# embeddings = 'sentence-transformers/all-MiniLM-L6-v2'
# index_name = "chatbotpdfs"
# question = "What is the difference between a trust and a will?"
# loader = PineconeLoader(docs, embeddings, index_name)
# response = loader.query(question)
# print(response)