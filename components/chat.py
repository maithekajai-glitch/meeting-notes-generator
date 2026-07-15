import streamlit as st

from utils.ai import ask_question


def chat_section(transcript: str) -> None:
    """Display the transcript chat interface with conversation memory."""

    st.subheader("💬 Chat with your Meeting")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not transcript.strip():
        st.info(
            "Paste or upload a meeting transcript before starting the chat."
        )

    # Display existing conversation.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask anything about the meeting...",
        key="meeting_chat_input",
        disabled=not bool(transcript.strip()),
    )

    if not prompt:
        return

    # Copy the history before adding the latest question.
    previous_messages = list(st.session_state.messages)

    # Store and display the latest user message.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate an answer using the previous conversation.
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer = ask_question(
                    transcript=transcript,
                    question=prompt,
                    chat_history=previous_messages,
                )

            st.markdown(answer)

        except Exception as error:
            answer = (
                "I couldn't generate an answer. "
                "Please check your connection and try again."
            )

            st.error(answer)

            # The full error is visible in local or Streamlit Cloud logs.
            print(f"Chat error: {error}")

    # Save assistant response.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.rerun()