import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Session State
# dictionary. personal histories.  {"messages": list}
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("Chatbot Widget Tutorial")

# input UI below
prompt = st.chat_input("User Prompt")
model = ChatOpenAI(model = 'gpt-4o-mini')

if prompt:
    res = model.invoke(prompt)
    st.session_state["messages"].append({'role':'user', 'content':prompt}) 
    st.session_state["messages"].append({'role':'AI', 'content':res.content})    
    
for message_dict in st.session_state['messages']:
    with st.chat_message(message_dict['role']):   # Returns: Container with messages(So, Whose message is this? -> "User")
        st.write(message_dict['content'])
