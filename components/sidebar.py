import streamlit as st


def show_sidebar() -> None:
    with st.sidebar:
        st.markdown("## 🤖 Meeting Assistant")

        st.caption(
            "AI-powered meeting intelligence workspace"
        )

        st.divider()

        st.success(
            "Groq AI connected",
            icon="✅",
        )

        st.markdown("### Navigation")

        st.markdown(
            """
🏠 **Dashboard**

📄 **Meeting source**

📝 **Generated notes**

💬 **Transcript chat**

📥 **Downloads**
"""
        )

        st.divider()

        st.markdown("### Supported sources")

        st.markdown(
            """
- TXT, PDF and DOCX
- MP3, WAV and M4A
- MP4, MPEG and WebM
- Browser microphone recording
"""
        )

        st.divider()

        notes_exist = bool(st.session_state.get("notes", ""))
        messages = st.session_state.get("messages", [])

        st.markdown("### Session")

        st.caption(
            f"Notes: {'Ready' if notes_exist else 'Not generated'}"
        )

        st.caption(
            f"Messages: {len(messages)}"
        )

        if st.button(
            "🗑️ Clear session",
            key="clear_session_button",
            use_container_width=True,
        ):
            keys_to_clear = [
                "notes",
                "messages",
                "last_transcript",
                "audio_transcript",
                "video_transcript",
                "recorded_transcript",
                "pasted_transcript",
            ]

            for key in keys_to_clear:
                st.session_state.pop(key, None)

            st.rerun()