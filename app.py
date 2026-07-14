import streamlit as st
from components.transcript import transcript_section
from components.sidebar import show_sidebar
from components.chat import chat_section
from components.notes import notes_section
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

# -------------------------------------------------
# Right Column
# -------------------------------------------------

with right:

    notes_section(transcript)

# ---------------------------------------
# Chat with Transcript
# ---------------------------------------

chat_section(transcript)