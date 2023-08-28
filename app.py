import streamlit as st
import time
import requests
import json
import os
import asyncio
from PIL import Image
from judini.codegpt.agent import Agent
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="centered")  

col1, col2 = st.columns([2,3])

with col1:
    image = Image.open('danigpt.png')
    st.image(image, width=200)

with col2:
    st.title("DaniGPT 🤖")
st.write("Preguntame cualquier cosa sobre python, Judini o Langchain")
st.write("OJO 👀 No estoy conectado a internet, así que puedo alucinar 😵‍💫, es tu trabajo corroborar que la respuesta que te entregue sea correcta.")
st.markdown('---')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("En que te puedo ayudar?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        #Judini
        codegpt_api_key= st.secrets["CODEGPT_API_KEY"]
        codegpt_agent_id= st.secrets["CODEGPT_AGENT_ID"]

        agent_instance = Agent(api_key=codegpt_api_key, agent_id=codegpt_agent_id)

        full_response = asyncio.run(agent_instance.completion(prompt, stream=False))
        
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})