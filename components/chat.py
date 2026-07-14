import streamlit as st
from utils.ai import ask_question


def chat_section(transcript):

    st.divider()

    st.subheader("💬 Chat with your Meeting")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input(
    "Ask anything about the meeting...",
    key="meeting_chat_input"
)
    if prompt:

        if transcript.strip() == "":
            st.warning("Please paste or upload a transcript first.")
            return

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_question(
                    transcript,
                    prompt
                )

                st.markdown(answer)

        # Store AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )