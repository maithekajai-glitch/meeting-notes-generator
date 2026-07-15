import streamlit as st

from components.chat import chat_section
from components.notes import notes_section
from components.sidebar import show_sidebar
from components.transcript import transcript_section


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="📝",
    layout="wide",
)


# -------------------------------------------------
# Custom styling
# -------------------------------------------------

st.markdown(
    """
    <style>
    /* Main page */
    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* Hero section */
    .hero-section {
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(109, 93, 251, 0.18);
        border-radius: 22px;
        background:
            radial-gradient(
                circle at top right,
                rgba(109, 93, 251, 0.18),
                transparent 38%
            ),
            linear-gradient(
                135deg,
                #ffffff 0%,
                #f3f2ff 100%
            );
        box-shadow: 0 10px 35px rgba(30, 41, 59, 0.07);
    }

    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin-bottom: 0.85rem;
        border-radius: 999px;
        background: rgba(109, 93, 251, 0.11);
        color: #5546d7;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .hero-title {
        margin: 0;
        font-size: 2.25rem;
        font-weight: 800;
        color: #172033;
    }

    .hero-description {
        max-width: 780px;
        margin-top: 0.65rem;
        margin-bottom: 0;
        color: #667085;
        font-size: 1rem;
        line-height: 1.65;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        min-height: 100px;
        padding: 1rem 1.1rem;
        border: 1px solid #E6E8F0;
        border-radius: 16px;
        background: #FFFFFF;
        box-shadow: 0 5px 18px rgba(30, 41, 59, 0.045);
    }

    [data-testid="stMetricLabel"] {
        color: #667085;
        font-size: 0.82rem;
        font-weight: 650;
    }

    [data-testid="stMetricValue"] {
        color: #172033;
        font-size: 1.4rem;
        font-weight: 750;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 12px;
        font-weight: 700;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(109, 93, 251, 0.18);
    }

    .stDownloadButton > button {
        width: 100%;
        min-height: 43px;
        border-radius: 11px;
        font-weight: 650;
    }

    /* Tabs */
    [data-baseweb="tab-list"] {
        gap: 0.4rem;
        padding: 0.35rem;
        border-radius: 14px;
        background: #EEF0F7;
    }

    [data-baseweb="tab"] {
        min-height: 44px;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
        border-radius: 10px;
        font-weight: 700;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        background: #FFFFFF;
        box-shadow: 0 3px 10px rgba(30, 41, 59, 0.08);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        padding: 0.4rem;
        border: 1px dashed #B8B4F8;
        border-radius: 15px;
        background: rgba(109, 93, 251, 0.035);
    }

    /* Text areas */
    textarea {
        border-radius: 13px !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        border: 1px solid #E8EAF1;
        border-radius: 15px;
        background: #FFFFFF;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 13px;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #E6E8F0;
        border-radius: 14px;
        background: #FFFFFF;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid #E2E4F0;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* Footer */
    .app-footer {
        margin-top: 2rem;
        padding: 1.3rem 0 0.4rem;
        border-top: 1px solid #E5E7EB;
        color: #98A2B3;
        text-align: center;
        font-size: 0.83rem;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------
# Session state
# -------------------------------------------------

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

show_sidebar()


# -------------------------------------------------
# Hero section
# -------------------------------------------------

st.markdown(
    """
    <div class="hero-section">
        <div class="hero-badge">
            AI-POWERED MEETING INTELLIGENCE
        </div>

        <h1 class="hero-title">
            📝 AI Meeting Assistant
        </h1>

        <p class="hero-description">
            Turn documents, audio recordings, browser recordings, and meeting
            videos into structured notes. Ask follow-up questions, identify
            decisions and action items, and export professional summaries.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------
# Transcript input
# -------------------------------------------------

transcript = transcript_section()


# -------------------------------------------------
# Dashboard metrics
# -------------------------------------------------

word_count = len(transcript.split())
message_count = len(st.session_state.get("messages", []))
notes_ready = bool(st.session_state.get("notes", ""))

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="📝 Transcript words",
        value=f"{word_count:,}",
    )

with metric_col2:
    st.metric(
        label="💬 Chat messages",
        value=message_count,
    )

with metric_col3:
    st.metric(
        label="📑 Notes status",
        value="Ready" if notes_ready else "Not generated",
    )


# -------------------------------------------------
# Input status
# -------------------------------------------------

if transcript.strip():
    st.success("Transcript loaded successfully.", icon="✅")
else:
    st.info(
        "Paste, upload, or record a meeting to begin.",
        icon="📄",
    )

st.divider()


# -------------------------------------------------
# Main tabs
# -------------------------------------------------

notes_tab, chat_tab, guide_tab = st.tabs(
    [
        "📝 Meeting Notes",
        "💬 Ask the Meeting",
        "✨ Quick Guide",
    ]
)

with notes_tab:
    notes_section(transcript)

with chat_tab:
    chat_section(transcript)

with guide_tab:
    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        with st.container(border=True):
            st.markdown("### 1. Add your meeting")

            st.markdown(
                """
                Choose one input source:

                - Paste a transcript
                - Upload TXT, PDF, or DOCX
                - Upload meeting audio
                - Upload a meeting video
                - Record audio directly in the browser
                """
            )

    with guide_col2:
        with st.container(border=True):
            st.markdown("### 2. Use the AI tools")

            st.markdown(
                """
                - Generate structured meeting notes
                - Review decisions and action items
                - Ask transcript-based questions
                - Continue with follow-up questions
                - Download PDF, DOCX, or Markdown
                """
            )

    with st.container(border=True):
        st.markdown("### Example questions")

        st.markdown(
            """
            - What decisions were confirmed?
            - Who owns each action item?
            - What deadlines were mentioned?
            - What risks or blockers remain?
            - Summarize the meeting in five bullet points.
            - What happens after the review?
            """
        )


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown(
    """
    <div class="app-footer">
        Built with Streamlit, Groq, Whisper and Python
    </div>
    """,
    unsafe_allow_html=True,
)