import requests
import os

def get_context(input, loader, k=5):
    return loader.docsearch.similarity_search(input, k=k)


def get_response(input, loader):
    context = get_context(input, loader)
    response = requests.get("http://localhost:5000/echo", params={"input": input, "context": context}).json()["response"]
    return response

def save_uploadedfile(uploadedfile, folder="api_files"):
    try:
        os.listdir(folder)
    except:
        os.mkdir(folder)
    with open(os.path.join(folder ,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())