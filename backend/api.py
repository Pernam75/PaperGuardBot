import os
from flask import Flask, request, jsonify
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain import PromptTemplate
from llama_cpp import Llama
import pinecone

app = Flask(__name__)

# load documents
def load_pdf_documents(path):
    print(f'Loading documents from : {path} folder')
    loader = PyPDFDirectoryLoader(path)
    data = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=20)
    docs = splitter.split_documents(data)
    print(f'Loaded {len(docs)} paragraphs')
    return docs

# load embeddings
def load_embeddings(model_name):
    print('Loading embeddings model')
    return HuggingFaceEmbeddings(model_name=model_name)

# load LLM model
def load_llm(model_path):
    print('Loading LLM model')
    return Llama(model_path)

# create embeddings for each document
def create_embeddings(docs, embeddings, index_name):
    # clear pinecone index
    print('checking for existing index')
    if index_name in pinecone.list_indexes():
        print('Deleting existing index')
        pinecone.delete_index(index_name)
    # create new index
    print('Creating new index')
    pinecone.create_index(name=index_name, metric='cosine', shards=1, dimension=384)
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    print('Creating embeddings')
    return docsearch

# llm response function
def llm_response(question, model, template, docsearch):
    print('Generating response')
    print(question)
    promt_template = PromptTemplate(template=template, input_variables=["context", "question"])
    context = " \n ".join([c.page_content for c in docsearch.similarity_search(question, k=4)])
    print(context)
    prompt = promt_template.format(context=context, question=question)
    response = model(prompt, max_tokens=500, stop=["Q:"], echo=True)
    print(response)
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




PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'e625eff7-7e12-48a1-aab4-2d53d3670ce7')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)




# variable names 
LLM_model_name = 'llm/model/ggml-model-q4_k.gguf'
embeddings_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
index_name = "chatbotpdfs"
data_path = 'data'

# load LLM model, embeddings, and documents
LLM_model = load_llm(LLM_model_name)
embeddings = load_embeddings(embeddings_model_name)
docs = load_pdf_documents(data_path)

# create docsearch
docsearch = create_embeddings(docs, embeddings, index_name)























# create a simple test route on the default URL explaining each endpoint
@app.route("/", methods=["GET"])
def test():
    # return Hello World! to the caller
    return jsonify({
        'Greetings': 'Welcome to chatbot API',
        'Endpoints': {
            '/': 'This page',
            '/settings': 'Get and set user variables POST/GET',
            '/ask': 'Ask a question POST',
            '/upload': 'Upload a document POST',
            '/documents': 'Get uploaded documents GET'
        }
    }), 200

# create a route to get the uploaded documents in the data folder
@app.route("/documents", methods=["GET"])
def get_documents():
    files = os.listdir(data_path)
    return jsonify({'files': files})

# create a route to get user variables 
@app.route("/settings", methods=["GET"])
def get_settings():
    return jsonify({
        'PINECONE_API_KEY': PINECONE_API_KEY,
        'PINECONE_API_ENV': PINECONE_API_ENV,
        'LLM_MODEL': LLM_model_name,
        'EMBEDDINGS_MODEL': embeddings_model_name,
        'INDEX_NAME': index_name,
        'TEMPLATE': template
    })

# create a route to chane user variables
@app.route("/settings", methods=["POST"])
def set_settings():
    global PINECONE_API_KEY, PINECONE_API_ENV, LLM_model, embeddings, index_name, template, LLM_model_name, embeddings_model_name
    data = request.get_json()
    PINECONE_API_KEY = data['PINECONE_API_KEY']
    PINECONE_API_ENV = data['PINECONE_API_ENV']
    LLM_model_name = data['LLM_MODEL']
    embeddings_model_name = data['EMBEDDINGS_MODEL']
    LLM_model = load_llm(LLM_model_name)
    embeddings = load_embeddings(embeddings_model_name)
    index_name = data['INDEX_NAME']
    template = data['TEMPLATE']
    return jsonify({
        'PINECONE_API_KEY': PINECONE_API_KEY,
        'PINECONE_API_ENV': PINECONE_API_ENV,
        'LLM_MODEL': LLM_model,
        'EMBEDDINGS_MODEL': embeddings,
        'INDEX_NAME': index_name,
        'TEMPLATE': template
    })

# API endpoint
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    response = llm_response(question, LLM_model, template, docsearch)
    return jsonify({'response': response})

# upload document endpoint
@app.route('/upload', methods=['POST'])
def upload_document():
    global docsearch
    print('Uploading document')
    file = request.files['file']
    filename = request.form.get('filename')
    filepath = 'data/' + filename + '.pdf'
    if os.path.exists(filepath):
        print('File already exists')
        return jsonify({'message': 'File already exists'}, 400)
    else:
        print('Saving file')
        file.save(filepath)
        new_docs = load_pdf_documents('data')
        docsearch = create_embeddings(new_docs, embeddings, index_name)
        return jsonify({'message': 'Document uploaded successfully'})


if __name__ == '__main__':
    app.run()



