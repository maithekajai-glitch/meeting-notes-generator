import streamlit as st

st.sidebar.image(
    "assets/favicon.png",
    use_container_width=True,
)

def show_sidebar():
    with st.sidebar:

        # ----------------------------------------
        # Header
        # ----------------------------------------

        st.sidebar.markdown(
    """
### AI Meeting Assistant
AI-powered meeting intelligence workspace.
"""
)

        st.divider()

        # ----------------------------------------
        # Supported Inputs
        # ----------------------------------------

        st.markdown("### 📥 Import")

        st.markdown("""
📄 **Documents**

- TXT
- PDF
- DOCX

🎙 **Audio**

- MP3
- WAV
- M4A

🎥 **Video**

- MP4
- MOV
- AVI
- WEBM
""")

        st.divider()

        # ----------------------------------------
        # AI Features
        # ----------------------------------------

        st.markdown("### ⚡ AI Capabilities")

        st.markdown("""
✅ Smart Meeting Notes

💬 Transcript Chat

🎤 Audio Transcription

🎥 Video Transcription

📌 Action Item Detection

📅 Deadline Extraction

📋 AI Meeting Summary

📤 Export (PDF / DOCX / Markdown)
""")

        st.divider()

        # ----------------------------------------
        # Current Session
        # ----------------------------------------

        st.markdown("### 📊 Current Session")

        st.caption("Session data is stored until you clear it.")

        st.divider()

        # ----------------------------------------
        # Clear Session
        # ----------------------------------------

        if st.button(
            "🗑 Clear Session",
            use_container_width=True,
            type="primary",
        ):

            keys = [
    "notes",
    "messages",
    "meeting_analytics",
    "email_draft",
    "email_tone",
    "current_transcript",
    "audio_transcript",
    "video_transcript",
    "recorded_transcript",
    "pasted_transcript",
]

            for key in keys:
                st.session_state.pop(key, None)

            st.success("Session cleared!")

            st.rerun()

        st.divider()

        # ----------------------------------------
        # Footer
        # ----------------------------------------

        st.caption("🚀 Powered by Groq + Streamlit")