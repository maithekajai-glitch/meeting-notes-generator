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

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:48px;
    font-weight:600;
}

.stDownloadButton>button{
    width:100%;
    border-radius:10px;
}

textarea{
    font-size:15px;
}

.stMetric{
    border:1px solid #ddd;
    border-radius:12px;
    padding:12px;
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
st.sidebar.title("📝 AI Meeting Assistant")

st.sidebar.markdown("---")

st.sidebar.success("✅ Groq Connected")

st.sidebar.markdown("### Features")

st.sidebar.markdown("""
- 📝 Generate Notes
- 💬 Chat
- 📄 Upload Files
- 📥 Export
- ⚡ Fast Responses
""")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Supported Files

• TXT

• PDF

• DOCX
"""
)
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

left, right = st.columns(
    [1.1, 0.9]
)

transcript = ""

# -------------------------------------------------
# Left Column
# -------------------------------------------------

with left:

    transcript = transcript_section()

    col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Transcript Length",
        f"{len(transcript):,} chars"
    )

with col2:

    words = len(transcript.split())

    st.metric(
        "Words",
        words
    )

with col3:

    st.metric(
        "Chat Messages",
        len(st.session_state.get("messages", []))
    )

st.divider()

# -------------------------------------------------
# Right Column
# -------------------------------------------------
tab1, tab2 = st.tabs(
    ["📝 Meeting Notes", "💬 Chat"]
)

with tab1:
    notes_section(transcript)

with tab2:
    chat_section(transcript)

# ---------------------------------------
# Chat with Transcript
# ---------------------------------------


st.divider()

st.caption(
    "Built using Streamlit • Groq • OpenAI SDK • Python"
)