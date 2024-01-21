import streamlit as st
import requests

st.title("Echo Bot")

# add a side bar with a file uploader only with pdf files and a submit button
st.sidebar.title("Upload a PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
submit_button = st.sidebar.button("Submit")

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

response = requests.get("http://localhost:5000/echo", params={"input": prompt}).json()["response"] if prompt else None

if response:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})