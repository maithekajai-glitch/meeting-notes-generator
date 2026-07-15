import streamlit as st


def show_sidebar() -> None:
    with st.sidebar:
        st.markdown("## 📝 Meeting Assistant")

        st.caption(
            "Summaries, transcript chat, and meeting intelligence."
        )

        st.divider()

        st.success(
            "Groq AI connected",
            icon="✅",
        )

        st.markdown("### Input options")

        st.markdown(
            """
            📄 Documents  
            TXT, PDF and DOCX

            🎙️ Audio  
            MP3, WAV, M4A and more

            🎥 Video  
            MP4, MPEG and WebM

            🎤 Live recording  
            Record directly in the browser
            """
        )

        st.divider()

        st.markdown("### Workspace")

        notes_exist = bool(st.session_state.get("notes", ""))
        messages = st.session_state.get("messages", [])

        st.caption(
            f"Notes: {'Generated' if notes_exist else 'Not generated'}"
        )

        st.caption(
            f"Conversation messages: {len(messages)}"
        )

        st.divider()

        if st.button(
            "🗑️ Clear current session",
            key="clear_current_session",
            width="stretch",
        ):
            for key in [
                "notes",
                "messages",
                "last_transcript",
                "audio_transcript",
                "video_transcript",
                "recorded_transcript",
                "pasted_transcript",
            ]:
                st.session_state.pop(key, None)

            st.rerun()

        st.caption(
            "Your API key is stored securely in Streamlit Secrets."
        )