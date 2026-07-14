import streamlit as st
from components.transcript import transcript_section
from components.sidebar import show_sidebar
from utils.ai import generate_notes, ask_question
from utils.file_parser import extract_text
from utils.exporter import (
    export_markdown,
    export_docx,
    export_pdf,
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="📝",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:1rem;
}

.block-container{
    padding-top:2rem;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:50px;
    font-size:17px;
    font-weight:600;
}

textarea{
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "notes" not in st.session_state:
    st.session_state.notes = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

show_sidebar()
# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("📝 AI Meeting Assistant")

st.caption(
    "Generate professional meeting notes and ask questions about your meeting transcript."
)

# -------------------------------------------------
# Layout
# -------------------------------------------------

left, right = st.columns(2)

transcript = ""

# -------------------------------------------------
# Left Column
# -------------------------------------------------

with left:

    transcript = transcript_section()

    if st.button("📝 Generate Meeting Notes"):

        if transcript.strip() == "":

            st.warning("Please provide a meeting transcript.")

        else:

            with st.spinner("Generating meeting notes..."):

                st.session_state.notes = generate_notes(transcript)

# -------------------------------------------------
# Right Column
# -------------------------------------------------

with right:

    st.subheader("📑 Generated Meeting Notes")

    if st.session_state.notes:

        st.markdown(st.session_state.notes)

        st.divider()

        st.subheader("📥 Download Meeting Notes")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "⬇ Markdown",
                data=export_markdown(st.session_state.notes),
                file_name="meeting_notes.md",
                mime="text/markdown"
            )

        with col2:
            st.download_button(
                "⬇ DOCX",
                data=export_docx(st.session_state.notes),
                file_name="meeting_notes.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        with col3:
            st.download_button(
                "⬇ PDF",
                data=export_pdf(st.session_state.notes),
                file_name="meeting_notes.pdf",
                mime="application/pdf"
            )

    else:

        st.info("Meeting notes will appear here.")

# ---------------------------------------
# Chat with Transcript
# ---------------------------------------

st.divider()

st.subheader("💬 Chat with your Meeting")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask anything about the meeting...")

if question:

    if transcript.strip() == "":
        st.warning("Please upload or paste a transcript first.")

    else:

        # Show user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_question(
                    transcript,
                    question
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )