import os
from flask import Flask, request, jsonify # for creating the API
from langchain.document_loaders import PyPDFDirectoryLoader # for loading pdf documents
from langchain.text_splitter import RecursiveCharacterTextSplitter # for splitting documents
from langchain.embeddings import HuggingFaceEmbeddings # for creating embeddings
from langchain.vectorstores import Pinecone # for creating vector stores
from langchain import PromptTemplate # for creating prompt templates
from llama_cpp import Llama # for using LLM model
import pinecone


# ------------------------first part is the flask app ------------------------
app = Flask(__name__)

# load documents
def load_pdf_documents(path):
    """
    The function `load_pdf_documents` loads PDF documents from a specified folder, splits them into
    paragraphs, and returns the loaded paragraphs.
    
    :param path: The "path" parameter is the path to the folder where the PDF documents are located
    :return: a list of paragraphs.
    """
    print(f'Loading documents from : {path} folder')
    loader = PyPDFDirectoryLoader(path)
    data = loader.load()
    print('splitting documents')
    splitter = RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=20)
    docs = splitter.split_documents(data)
    print(f'Loaded {len(docs)} paragraphs')
    return docs

# load embeddings
def load_embeddings(model_name):
    """
    The function "load_embeddings" loads an embeddings model using the HuggingFaceEmbeddings class.
    
    :param model_name: The `model_name` parameter is the name or identifier of the pre-trained
    embeddings model that you want to load. It could be the name of a specific model architecture or a
    pre-trained model from a specific library or framework
    :return: an instance of the HuggingFaceEmbeddings class.
    """
    print('Loading embeddings model')
    return HuggingFaceEmbeddings(model_name=model_name)

# load LLM model
def load_llm(model_path):
    """
    The function "load_llm" loads an LLM model from a specified path.
    
    :param model_path: The model_path parameter is the path to the LLM model file that you want to load.
    It should be a string representing the file path
    """
    print('Loading LLM model')
    return Llama(model_path)

# create embeddings for each document
def create_embeddings(docs, embeddings, index_name):
    """
    The function `create_embeddings` creates embeddings for a list of documents and indexes them using
    Pinecone.
    
    :param docs: The `docs` parameter is a list of documents. Each document should have a `page_content`
    attribute, which contains the text content of the document
    :param embeddings: The "embeddings" parameter is a vector representation of the documents. It is a
    numerical representation of the documents that captures their semantic meaning. These embeddings are
    used to perform similarity searches and retrieve relevant documents
    :param index_name: The `index_name` parameter is a string that represents the name of the index you
    want to create or use. It is used to identify and reference the index when performing operations
    such as adding documents or searching for similar documents
    :return: the `docsearch` object, which is created using the `Pinecone.from_texts` method.
    """
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
    """
    The function `llm_response` generates a response to a given question using the LLM model and the
    provided context. It uses a prompt template to format the input for the model and generate the
    response.

    :param question: The `question` parameter is a string representing the question that you want to
    ask the model
    :param model: The `model` parameter is an instance of the LLM model that you want to use to
    generate the response
    :param template: The `template` parameter is a string representing the prompt template that you want
    to use to format the input for the model
    :param docsearch: The `docsearch` parameter is an instance of the Pinecone vector store that you
    want to use to retrieve relevant context for the question
    :return: a string representing the response generated by the model
    """

    print('Generating response')
    print(question)
    promt_template = PromptTemplate(template=template, input_variables=["context", "question"])
    context = " \n ".join([c.page_content for c in docsearch.similarity_search(question, k=4)])
    print(context)
    prompt = promt_template.format(context=context, question=question)
    response = model(prompt, max_tokens=2048, stop=["Q:"], echo=True)
    print(response)
    return response["choices"][0]["text"][len(prompt):]
















# ------------------------second part is the app setup ------------------------
# here the user can set the variables for the app

# create prompt template
SYSTEM_PROMPT = """Use the following pieces of context to answer the question at the end.
If there is no relevant information in the provided context, try to answer yourself.
limit the output size to less than 1024 tokens.
"""
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<>\n", "\n<>\n\n"
SYSTEM_PROMPT = B_SYS + SYSTEM_PROMPT + E_SYS
instruction = """
Give the answer to the user query:
{question}
Using the information given in the context
{context}
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
LLM_model_name = 'llm/model/llama-2-7b-chat.Q4_K_M.gguf'
embeddings_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
index_name = "chatbotpdfs"
data_path = 'data'

# load LLM model, embeddings, and documents
LLM_model = load_llm(LLM_model_name)
embeddings = load_embeddings(embeddings_model_name)
docs = load_pdf_documents(data_path)

# create docsearch
docsearch = create_embeddings(docs, embeddings, index_name)





















# ------------------------third part is the API endpoints ------------------------

# create a simple test route on the default URL explaining each endpoint
@app.route("/", methods=["GET"])
def test():
    """
    The function `test` is a simple test route that returns a welcome message and a list of available
    endpoints for the API.
    """
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
    """
    The function `get_documents` returns a list of the documents that have been uploaded to the data
    folder.
    """
    files = os.listdir(data_path)
    return jsonify({'files': files})

# create a route to get user variables 
@app.route("/settings", methods=["GET"])
def get_settings():
    """
    The function `get_settings` returns the current user variables that are being used by the API.
    """
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
    """
    The function `set_settings` sets the user variables that are used by the API. It receives a JSON
    object containing the new values for the user variables and updates the variables accordingly.
    """
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
    """
    The function `ask_question` receives a JSON object containing a question and returns a response
    generated by the LLM model.
    """
    data = request.get_json()
    question = data['question']
    response = llm_response(question, LLM_model, template, docsearch)
    return jsonify({'response': response})

# upload document endpoint
@app.route('/upload', methods=['POST'])
def upload_document():
    """
    The function `upload_document` receives a PDF file and saves it to the data folder. It then loads
    the new document, creates embeddings for it, and updates the docsearch object.
    """
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



