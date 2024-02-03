import streamlit as st
from openai import OpenAI

st.title("ChatGPT-like clone")

# set OpenAI key from streamlit service
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# accept user input
if prompt := st.chat_input("What is up?"):
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # display user message in chat messae container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
             messages = [
                 {"role": msg["role"], "content": msg["content"]}
                 for msg in st.session_state.messages
             ],
             stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})