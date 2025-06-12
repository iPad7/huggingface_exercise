import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

####################################################################################################
# My Code:   NEED MODIFICATION
####################################################################################################

# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if 'model' not in st.session_state:
#     st.session_state['model'] = ChatOpenAI(model = 'gpt-4o-mini')
# if "chain" not in st.session_state:
#     parser = StrOutputParser()
#     st.session_state["chain"] = st.session_state['model'] | parser
    
# st.title("GPT-4o-mini Tutorial: Streaming")

# # input UI below
# prompt = st.chat_input("User Prompt")
# if prompt:
#     output = st.session_state['model'].stream(prompt)
#     st.write_stream(output)
#     res = ""
#     for token in output:
#         res += token
#     st.session_state["messages"].append({'role':'user', 'content':prompt}) 
#     st.session_state["messages"].append({'role':'AI', 'content':res})    
    
# for message_dict in st.session_state['messages']:
#     with st.chat_message(message_dict['role']):   # Returns: Container with messages(So, Whose message is this? -> "User")
#         st.write(message_dict['content'])

####################################################################################################
# Instructor's Code
####################################################################################################

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("GPT-4o-mini Tutorial")

for message in st.session_state["messages"]:
    with st.chat_message(message['role']):
        st.write(message['content'])

@st.cache_resource
# Note that we should clear cache When modifying codes.
def get_llm_model():
    load_dotenv()
    return ChatOpenAI(model_name = 'gpt-4o-mini')

model = get_llm_model()

prompt = st.chat_input("User Prompt")
if prompt:
    st.session_state["messages"].append({'role':'user', 'content':prompt})
    with st.chat_message('user'):
        st.write(prompt)

    with st.chat_message('ai'):
        message_placeholder = st.empty()   # Updatable Container
        # output_generator =model.stream(prompt)
        # message_placeholder.write_stream(output_generator)
        full_message = ""
        # for token in output_generator:
        for token in model.stream(prompt):
            full_message += token.content
            message_placeholder.write(full_message)
            st.empty().write_stream()

        st.session_state["messages"].append({"role":"ai", "content":full_message})