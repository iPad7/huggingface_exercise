import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("GPT-4o-mini Tutorial")

# input UI below
model = ChatOpenAI(model = 'gpt-4o-mini')
prompt = st.chat_input("User Prompt")
parser = StrOutputParser()
chain = model | parser
if prompt:
    res = chain.invoke(prompt)
    st.session_state["messages"].append({'role':'user', 'content':prompt}) 
    st.session_state["messages"].append({'role':'AI', 'content':res})    
    
for message_dict in st.session_state['messages']:
    with st.chat_message(message_dict['role']):   # Returns: Container with messages(So, Whose message is this? -> "User")
        st.write(message_dict['content'])