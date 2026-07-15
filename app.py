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
    initial_sidebar_state="expanded",
)


# -------------------------------------------------
# GitHub Dark + Purple UI
# -------------------------------------------------

st.markdown(
    """
<style>
:root {
    --app-bg: #0D1117;
    --surface: #161B22;
    --surface-soft: #1C2128;
    --surface-hover: #21262D;
    --border: #30363D;
    --border-purple: rgba(124, 58, 237, 0.55);
    --text-main: #F0F6FC;
    --text-muted: #8B949E;
    --purple: #7C3AED;
    --purple-light: #A78BFA;
    --green: #3FB950;
}

/* Main page */
.stApp {
    background:
        radial-gradient(
            circle at 80% 5%,
            rgba(124, 58, 237, 0.12),
            transparent 24rem
        ),
        #0D1117;
}

.block-container {
    max-width: 1280px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text-main);
    letter-spacing: -0.025em;
}

/* Hero */
.hero-section {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2.3rem;
    margin-bottom: 1.5rem;
    border: 1px solid var(--border-purple);
    border-radius: 22px;
    background:
        linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.19),
            rgba(22, 27, 34, 0.92) 45%,
            rgba(13, 17, 23, 0.98)
        );
    box-shadow:
        0 18px 55px rgba(0, 0, 0, 0.34),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.hero-section::after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    top: -110px;
    right: -70px;
    border-radius: 50%;
    background: rgba(124, 58, 237, 0.18);
    filter: blur(14px);
}

.hero-badge {
    position: relative;
    z-index: 1;
    display: inline-block;
    padding: 0.38rem 0.78rem;
    margin-bottom: 0.9rem;
    border: 1px solid rgba(167, 139, 250, 0.35);
    border-radius: 999px;
    background: rgba(124, 58, 237, 0.18);
    color: #C4B5FD;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.075em;
}

.hero-title {
    position: relative;
    z-index: 1;
    margin: 0;
    color: var(--text-main);
    font-size: 2.45rem;
    font-weight: 850;
}

.hero-description {
    position: relative;
    z-index: 1;
    max-width: 790px;
    margin-top: 0.72rem;
    margin-bottom: 0;
    color: #B1BAC4;
    font-size: 1.02rem;
    line-height: 1.7;
}

/* Metrics */
[data-testid="stMetric"] {
    min-height: 108px;
    padding: 1rem 1.15rem;
    border: 1px solid var(--border);
    border-radius: 16px;
    background:
        linear-gradient(
            145deg,
            rgba(28, 33, 40, 0.98),
            rgba(22, 27, 34, 0.98)
        );
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
}

[data-testid="stMetric"]:hover {
    border-color: rgba(124, 58, 237, 0.65);
    transform: translateY(-1px);
    transition: 0.15s ease;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-size: 0.82rem;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: var(--text-main);
    font-size: 1.45rem;
    font-weight: 800;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border: 1px solid rgba(167, 139, 250, 0.38);
    border-radius: 12px;
    background:
        linear-gradient(
            135deg,
            #7C3AED,
            #6D28D9
        );
    color: white;
    font-weight: 750;
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.2);
    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.stButton > button:hover {
    border-color: #C4B5FD;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 11px 26px rgba(124, 58, 237, 0.33);
}

.stButton > button:disabled {
    background: #21262D;
    color: #6E7681;
    border-color: #30363D;
    box-shadow: none;
}

.stDownloadButton > button {
    width: 100%;
    min-height: 43px;
    border: 1px solid #484F58;
    border-radius: 11px;
    background: #21262D;
    color: #F0F6FC;
    font-weight: 700;
}

.stDownloadButton > button:hover {
    border-color: var(--purple-light);
    color: white;
    background: #292E36;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 0.45rem;
    padding: 0.4rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: #161B22;
}

[data-baseweb="tab"] {
    min-height: 45px;
    padding-left: 1.15rem;
    padding-right: 1.15rem;
    border-radius: 10px;
    color: #8B949E;
    font-weight: 750;
}

[data-baseweb="tab"]:hover {
    color: #F0F6FC;
    background: #21262D;
}

[aria-selected="true"][data-baseweb="tab"] {
    color: #FFFFFF;
    background:
        linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.82),
            rgba(109, 40, 217, 0.72)
        );
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.23);
}

/* File uploader */
[data-testid="stFileUploader"] {
    padding: 0.5rem;
    border: 1px dashed rgba(167, 139, 250, 0.65);
    border-radius: 16px;
    background:
        linear-gradient(
            145deg,
            rgba(124, 58, 237, 0.08),
            rgba(22, 27, 34, 0.88)
        );
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 150px;
    border-radius: 13px;
    background: rgba(13, 17, 23, 0.55);
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #C9D1D9;
}

/* Inputs */
textarea,
input {
    color: #F0F6FC !important;
}

textarea {
    border: 1px solid #30363D !important;
    border-radius: 13px !important;
    background: #0D1117 !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 1px #7C3AED !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    border-color: #30363D !important;
    border-radius: 12px !important;
    background: #161B22 !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    padding: 0.95rem 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid #30363D;
    border-radius: 16px;
    background: #161B22;
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.16);
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    margin-left: 7%;
    border-color: rgba(124, 58, 237, 0.5);
    background: rgba(124, 58, 237, 0.12);
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) {
    margin-right: 7%;
    background: #161B22;
}

[data-testid="stChatInput"] {
    border: 1px solid #30363D;
    border-radius: 15px;
    background: #161B22;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid #30363D;
}

/* Expanders and containers */
[data-testid="stExpander"] {
    border: 1px solid #30363D;
    border-radius: 14px;
    background: #161B22;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #30363D !important;
    border-radius: 15px !important;
    background: rgba(22, 27, 34, 0.72);
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid #30363D;
    background:
        linear-gradient(
            180deg,
            #010409,
            #0D1117
        );
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] hr {
    border-color: #30363D;
}

/* Dividers */
hr {
    border-color: #30363D;
}

/* Footer */
.app-footer {
    margin-top: 2rem;
    padding: 1.4rem 0 0.45rem;
    border-top: 1px solid #30363D;
    color: #8B949E;
    text-align: center;
    font-size: 0.83rem;
}

.tech-badge {
    display: inline-block;
    padding: 0.25rem 0.55rem;
    margin: 0.18rem;
    border: 1px solid #30363D;
    border-radius: 999px;
    background: #161B22;
    color: #B1BAC4;
    font-size: 0.76rem;
}

/* Hide default footer */
footer {
    visibility: hidden;
}

/* Mobile */
@media (max-width: 700px) {
    .hero-section {
        padding: 1.45rem;
    }

    .hero-title {
        font-size: 1.85rem;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ),
    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) {
        margin-left: 0;
        margin-right: 0;
    }
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
# Hero
# -------------------------------------------------

st.markdown(
    """
<div class="hero-section">
    <div class="hero-badge">AI-POWERED MEETING INTELLIGENCE</div>

    <div class="hero-title">
        📝 AI Meeting Assistant
    </div>

    <div class="hero-description">
        Convert documents, audio recordings, browser recordings, and meeting
        videos into structured insights. Generate professional notes, identify
        action items, continue contextual conversations, and export results.
    </div>
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
# Source status
# -------------------------------------------------

if transcript.strip():
    st.success(
        "Transcript loaded successfully.",
        icon="✅",
    )
else:
    st.info(
        "Paste, upload, or record a meeting to begin.",
        icon="📂",
    )

st.divider()


# -------------------------------------------------
# Main workspace
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
            st.markdown("### 📂 Add your meeting")

            st.markdown(
                """
Choose one source:

- Paste a transcript
- Upload TXT, PDF, or DOCX
- Upload meeting audio
- Upload a meeting video
- Record audio through the browser
"""
            )

    with guide_col2:
        with st.container(border=True):
            st.markdown("### ✨ Use the AI tools")

            st.markdown(
                """
- Generate structured meeting notes
- Identify decisions and action items
- Ask transcript-grounded questions
- Continue with follow-up questions
- Export PDF, DOCX, or Markdown
"""
            )

    with st.container(border=True):
        st.markdown("### 💡 Example questions")

        st.markdown(
            """
- What decisions were confirmed?
- Who owns each action item?
- Which deadlines were mentioned?
- What risks or blockers remain?
- Summarize the meeting in five bullet points.
- What happens after the next review?
"""
        )


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown(
    """
<div class="app-footer">
    <div>Powered by</div>
    <div>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Groq</span>
        <span class="tech-badge">Whisper</span>
        <span class="tech-badge">Python</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)