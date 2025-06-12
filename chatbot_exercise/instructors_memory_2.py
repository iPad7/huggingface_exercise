import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from sqlalchemy import create_engine
from langchain_core.runnables import RunnableWithMessageHistory

@st.cache_resource
# Note that we should clear cache When modifying codes.
def get_llm_model():
    load_dotenv()
    prompt_template = ChatPromptTemplate(
        messages = [
            ('system', '답변을 100단어 이내로 작성해주세요.'),
            MessagesPlaceholder(variable_name = 'history', optional = True),
            ("user","{query}")
        ]
    )
    model =  ChatOpenAI(model_name = 'gpt-4o-mini')
    base_chain = prompt_template | model | StrOutputParser()
    return base_chain

@st.cache_resource
def get_chain():
    runnable = get_llm_model()
    print(type(runnable),"---------------------")
    engine = create_engine('sqlite:///chat_history.sqlite')
    chain = RunnableWithMessageHistory(
        runnable = runnable,
        get_session_history = lambda session_id: SQLChatMessageHistory(session_id = session_id, connection = engine),
        input_messages_key = 'query',
        history_messages_key = 'history'
    )
    return chain

model = get_chain()

st.title("GPT-4o-mini Tutorial")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

session_id = st.sidebar.text_input("Session ID", placeholder = "대화 ID를 입력하세요.")

messages_list = st.session_state['messages']

for message in messages_list:
    with st.chat_message(message['role']):
        st.write(message['content'])

prompt = st.chat_input("User Prompt")
if prompt:
    messages_list.append({'role':'user', 'content':prompt})
    with st.chat_message('user'):
        st.write(prompt)
    if st.session_state['session_id'] is None:
        st.session_state['session_id'] = session_id
    
    config = {"configurable": {'session_id':st.session_state['session_id']}}

    with st.chat_message('ai'):
        message_placeholder = st.empty()   # Updatable Container
        full_message = ""
        for token in model.stream({"query":prompt}, config = config):
            full_message += token
            message_placeholder.write(full_message)

        st.session_state["messages"].append({"role":"ai", "content":full_message})

# HISTORY CAN BE IN A PROMPT AS # Context.