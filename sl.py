import streamlit as st
from streamlit_chat import message
import openai
from openai import OpenAI
import time
from langdetect import detect

# os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("胖胖 Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0301",
            # response_format={ 'type': "json_object"},
            messages=[
                {"role": "system", "content": "你叫胖胖"},
                # {"role": "user", "content": message},
                # {"role": "assistant", "content": history},
                {"role": "user", "content": prompt}
            ],
            # seed = 1000000
            stream = True
        )
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = completion

        for chunk in completion:
            if chunk.choices[0].delta.content == None:
                break
            full_response += chunk.choices[0].delta.content
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
