import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("GPT-4o-mini Tutorial")

messages_list = st.session_state['messages']
history_messages_list = [(msg_dict['role'], msg_dict['content']) for msg_dict in messages_list]
# history_message_list = [i for i in message_list]


for message in messages_list:
    with st.chat_message(message['role']):
        st.write(message['content'])

@st.cache_resource
# Note that we should clear cache When modifying codes.
def get_llm_model():
    load_dotenv()
    prompt_template = ChatPromptTemplate(
        messages = [
            MessagesPlaceholder(variable_name = 'history', optional = True),
            ("user","{query}")
        ]
    )
    model =  ChatOpenAI(model_name = 'gpt-4o-mini')
    return prompt_template | model | StrOutputParser()

model = get_llm_model()

prompt = st.chat_input("User Prompt")
if prompt:
    messages_list.append({'role':'user', 'content':prompt})
    with st.chat_message('user'):
        st.write(prompt)

    with st.chat_message('ai'):
        message_placeholder = st.empty()   # Updatable Container
        full_message = ""
        for token in model.stream({"query":prompt, "history":history_messages_list}):
            full_message += token
            message_placeholder.write(full_message)

        st.session_state["messages"].append({"role":"ai", "content":full_message})

# HISTORY CAN BE IN A PROMPT AS # Context.