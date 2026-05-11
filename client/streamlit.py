# streamlit_app.py

import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Conversational SHL Assessment Recommender")

st.markdown(
    "Ask hiring requirements and get grounded SHL assessment recommendations."
)

# SESSION STATE


if "messages" not in st.session_state:
    st.session_state.messages = []




for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



prompt = st.chat_input("Type your hiring requirement...")








if prompt:


    # Add user message
   

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)


    payload = {
        "messages": st.session_state.messages
    }








   
# API CALL
   

    try:

        response = requests.post(API_URL, json=payload)

        print(response.text)

        data = response.json()

        reply = data.get(
            "reply",
            "No response generated."
        )

        recommendations = data.get(
            "recommendations",
            []
        )

        # built assistant response
       

        assistant_text = reply

        if recommendations:

            assistant_text += "\n\n### Recommended Assessments\n"

            for item in recommendations:

                assistant_text += f"""
- **{item['name']}**
  - Type: {item['test_type']}
  - URL: {item['url']}
"""

     
        # save assistant response
        

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_text
        })

       

        with st.chat_message("assistant"):
            st.markdown(assistant_text)

    except Exception as e:

        st.error(
            f"error connecting to fastapi server: {e}"
        )