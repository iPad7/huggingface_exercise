# My Code
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chain" not in st.session_state:
    model = ChatOpenAI(model = 'gpt-4o-mini')
    parser = StrOutputParser()
    st.session_state["chain"] = model | parser
    
st.title("GPT-4o-mini Tutorial")

# input UI below
prompt = st.chat_input("User Prompt")
if prompt:
    res = st.session_state["chain"].invoke(prompt)
    st.session_state["messages"].append({'role':'user', 'content':prompt}) 
    st.session_state["messages"].append({'role':'AI', 'content':res})    
    
for message_dict in st.session_state['messages']:
    with st.chat_message(message_dict['role']):   # Returns: Container with messages(So, Whose message is this? -> "User")
        st.write(message_dict['content'])


# Instructor's Code
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# st.title("GPT-4o-mini Tutorial")

# @st.cache_resource
# # Note that we should clear cache When modifying codes.
# def get_llm_model():
#     load_dotenv()
#     return ChatOpenAI(model_name = 'gpt-4o-mini')

# model = get_llm_model()

# prompt = st.chat_input("User Prompt")
# if prompt:
#     res = st.session_state["chain"].invoke(prompt)
#     st.session_state["messages"].append({'role':'user', 'content':prompt})
#     ai_message = model.invoke(prompt).content 
#     st.session_state["messages"].append({'role':'AI', 'content':ai_message})    

# for message_dict in st.session_state['messages']:
#     with st.chat_message(message_dict['role']):   # Returns: Container with messages(So, Whose message is this? -> "User")
#         st.write(message_dict['content'])