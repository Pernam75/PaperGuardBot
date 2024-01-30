from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain import PromptTemplate
from llama_cpp import Llama
import pinecone
import os

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'e625eff7-7e12-48a1-aab4-2d53d3670ce7')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

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

# load LLM model
def load_llm(model_path):
    return Llama(model_path)

# create embeddings for each document
def create_embeddings(docs, embeddings, index_name):
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    return docsearch

# llm response function
def llm_response(question, model, template, docsearch):
    promt_template = PromptTemplate(template=template, input_variables=["context", "question"])
    prompt = promt_template.format(context=" \n ".join([c.page_content for c in docsearch.similarity_search(question, k=4)]), question=question)
    response = model(prompt, max_tokens=500, stop=["Q:"], echo=True)
    return response["choices"][0]["text"][len(prompt):]

# create prompt template
SYSTEM_PROMPT = """Use the following pieces of context to answer the question at the end. and if the contenxt is relevant to the question, please answer the question while incorporating the context into your answer. """
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<>\n", "\n<>\n\n"
SYSTEM_PROMPT = B_SYS + SYSTEM_PROMPT + E_SYS
instruction = """
{context}
Question: {question}
Answer: 
"""
template = SYSTEM_PROMPT + instruction

# test run ============================================================================================================

docs = load_pdf_documents('data')

embeddings = load_embeddings('sentence-transformers/all-MiniLM-L6-v2')

LLM_model = load_llm('llm/model/ggml-model-q4_k.gguf')

index_name = "chatbotpdfs"

docsearch = create_embeddings(docs, embeddings, index_name)

# ask question
question = "What is the difference between a trust and a will?"
response = llm_response(question, LLM_model, template, docsearch)
print(response)


