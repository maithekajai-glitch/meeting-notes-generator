import streamlit as st

def show_sidebar():

    with st.sidebar:

        st.title("📝 AI Meeting Assistant")

        st.markdown("---")

        st.markdown("""
### Features

- 📝 Generate Meeting Notes
- 💬 Chat with Transcript
- 📄 Upload TXT/PDF/DOCX
- 📥 Export Notes
- ⚡ Powered by Groq
""")

        st.markdown("---")

        st.info(
            "Upload or paste a meeting transcript to generate AI-powered meeting notes."
        )