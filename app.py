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

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero-card {
        padding: 1.5rem 1.7rem;
        border: 1px solid rgba(108, 99, 255, 0.18);
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            rgba(108, 99, 255, 0.12),
            rgba(255, 255, 255, 0.92)
        );
        margin-bottom: 1.4rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #667085;
        margin-bottom: 0;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.35rem;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 11px;
        font-weight: 650;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
    }

    textarea {
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
    }

    [data-testid="stFileUploader"] {
        border: 1px dashed #C7C9FF;
        border-radius: 14px;
        padding: 0.5rem;
        background: rgba(108, 99, 255, 0.03);
    }

    [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding-left: 1rem;
        padding-right: 1rem;
        font-weight: 600;
    }

    hr {
        margin-top: 1.4rem;
        margin-bottom: 1.4rem;
    }

    .footer {
        text-align: center;
        color: #8A94A6;
        font-size: 0.85rem;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">📝 AI Meeting Assistant</div>
        <p class="hero-subtitle">
            Turn transcripts into structured notes, ask follow-up questions,
            and export your meeting summary in seconds.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
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

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(
        label="📝 Words",
        value=f"{len(transcript.split()):,}"
    )

with metric_col2:
    st.metric(
        label="💬 Chat Messages",
        value=len(st.session_state.get("messages", []))
    )

st.divider()

# -------------------------------------------------
# Right Column
# -------------------------------------------------
notes_tab, chat_tab, help_tab = st.tabs(
    [
        "📝 Meeting Notes",
        "💬 Chat",
        "ℹ️ How to Use",
    ]
)

with notes_tab:
    notes_section(transcript)

with chat_tab:
    chat_section(transcript)

with help_tab:
    st.markdown(
        """
        ### How to use the assistant

        1. Paste a transcript or upload a TXT, PDF, or DOCX file.
        2. Open **Meeting Notes** and generate structured notes.
        3. Open **Chat** to ask questions about the transcript.
        4. Download the notes as Markdown, DOCX, or PDF.

        ### Example questions

        - What decisions were made?
        - Who owns each action item?
        - What deadlines were mentioned?
        - What blockers or risks were discussed?
        """
    )

# ---------------------------------------
# Chat with Transcript
# ---------------------------------------


st.divider()

st.caption(
    "Built using Streamlit • Groq • OpenAI SDK • Python"
)

if transcript:
    st.success("✅ Transcript loaded successfully")
else:
    st.info("📄 Paste or upload a meeting transcript to begin.")

st.markdown(
    """
    <div class="footer">
        Built with Streamlit, Groq and Python
    </div>
    """,
    unsafe_allow_html=True,
)