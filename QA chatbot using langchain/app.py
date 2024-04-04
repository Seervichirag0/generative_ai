import streamlit as st
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

#Streamlit UI
st.set_page_config(page_title = "Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

from dotenv import load_dotenv
load_dotenv()
import os

chat = ChatOpenAI(temperature = 0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content = 'You are a Comedy AI assistant')
    ]

#Function to load OpenAI model and get responses

def get_chatmodel_response(question):
    
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

input = st.text_input("Input:",key='input')
response = get_chatmodel_response(input)

submit = st.button("Ask the question")

#if the button is clicked

if submit:
    st.subheader("The response is")
    st.write(response)
