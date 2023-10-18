import streamlit as st
from PIL import Image
from judini.codegpt.agent import Agent
import asyncio
import time

st.set_page_config(layout="centered")  

col1, col2 = st.columns([2,3])

with col1:
    image = Image.open('danigpt.png')
    st.image(image, width=200)

with col2:
    st.title("DaniGPT 🤖")


st.write("Pregúntame cualquier cosa sobre Python, Judini o Langchain")
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
if prompt := st.chat_input("En qué te puedo ayudar?"):
	# Add user message to chat history
	st.session_state.messages.append({"role": "user", "content": prompt})

	# Display user message in chat message container
	with st.chat_message("user"):
		st.markdown(prompt)

	# Display assistant response in chat message container
	with st.chat_message("assistant"):
		message_placeholder = st.empty()

		# Utilizar el módulo judini.codegpt.agent para obtener la respuesta
		async def get_assistant_response(prompt):
			CODEGPT_API_KEY = "XXXXX"
			CODEGPT_AGENT_ID = "XXXXX"

			agent_instance = Agent(api_key=CODEGPT_API_KEY, agent_id=CODEGPT_AGENT_ID)
			# Utilizar el método chat_completion del agente para obtener la respuesta
			response_text = ""
			
			print(st.session_state.messages)
			async for response_chunk in agent_instance.chat_completion(st.session_state.messages, stream=False):
				response_chunk_text = response_chunk.strip()  # Obtener el texto del fragmento

				for chunk in response_chunk_text.split():
					response_text += chunk
					message_placeholder.markdown(response_text)
					time.sleep(0.09)
				

				# response_text += response_chunk_text
				# message_placeholder.markdown(response_chunk_text)

			# Agregar el contenido al diccionario de mensajes
			
			st.session_state.messages.append({"role": "assistant", "content": response_text})

		asyncio.run(get_assistant_response(prompt))
