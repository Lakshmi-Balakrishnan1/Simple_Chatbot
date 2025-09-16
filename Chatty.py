import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
#streamlit page initialization
st.set_page_config(page_title="Simple Chatbot", layout="wide")
st.title("Chatty The Bot")
#LLM Setup
llm=ChatGroq(model="llama-3.1-8b-instant")
#Personas
helpful_system_prompt ="You are a helpful and polite assistant. Always give clear, respectful answers."
sarcastic_system_prompt ="You are a sarcastic assistant. Respond with witty, dry humor and heavy sarcasm, but still answer the question."
def get_chain(persona):
        if persona=='helpful':
                return helpful_system_prompt
        elif persona=='sarcastic':
                return sarcastic_system_prompt
        else:
                return'You are a general chatbot'
def prompt_template(system_message):
    return ChatPromptTemplate.from_messages([
        ("system",system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

#Chat history
if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

#Personas
persona = st.radio("Choose a bot persona:", ["Helpful", "Sarcastic"])
persona = persona.lower()
system_message = get_chain(persona)

#conversational chain with memory
if "conversation" not in st.session_state:
        st.session_state.conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory(return_messages=True),verbose=False,prompt=prompt_template(system_message))
        st.session_state.persona=persona
#past chat messages
for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
#User input
user_query = st.chat_input("Ask a question...") #Input
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))#add q to history
    with st.chat_message("user"):
        st.markdown(user_query)
    with st.spinner("Thinking..."):
        response = st.session_state.conversation.invoke({"input": user_query})#fetch answer from llm
        assistant_response = response["response"]
    with st.chat_message("assistant"):
        st.markdown(assistant_response)#display answer
    st.session_state.chat_history.append(AIMessage(content=assistant_response))#record conversation in chat history
    


