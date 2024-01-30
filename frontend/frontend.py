import streamlit as st
import requests

st.title("Teacher Bot")


st.sidebar.title("Set up")

# add a side bar with a file uploader only with pdf files and a submit button
uploaded_files = st.sidebar.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
submit_button = st.sidebar.button("Submit")
# when the submit button is clicked, loop through the uploaded files and response get the name of the file
if submit_button:
    pdf_db = "uploaded files:\n"
    for uploaded_file in uploaded_files:
        # request API to save the file
        file_bytes = uploaded_file.getvalue()
        #remove the extension from the file name and send it along with the file
        req = requests.post("http://localhost:5000/upload", files={"file": file_bytes}, data={"filename": uploaded_file.name.split(".")[0]})
        print(req, uploaded_file.name)
        if req.status_code == 200:
            # success message 
            st.sidebar.success(f"File {uploaded_file.name} uploaded successfully")
        elif req.status_code == 400:
            # error message
            st.sidebar.error(f"File {uploaded_file.name} already exists")


# add an input for the api ip address and port in the sidebar
api_ip = st.sidebar.text_input("API IP address", value="localhost")
# add a button to test the connection in the sidebar
test_connection = st.sidebar.button("Test connection")
if test_connection:
    try:
        # try to connect to the API
        req = requests.get(f"http://{api_ip}")
        # if the connection is successful, display a success message
        if req.status_code == 200:
            st.sidebar.success("Connection successful")
    except:
        # if the connection is not successful, display an error message
        st.sidebar.error("Connection failed")

        
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

response = requests.post("http://localhost:5000/ask", json={"question": prompt}).json()["response"] if prompt else None

if response:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})