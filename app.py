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
# Session state
# -------------------------------------------------

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------
# Light theme styling
# -------------------------------------------------

st.markdown(
    """
<style>
:root {
    --app-bg: #F7F8FC;
    --surface: #FFFFFF;
    --surface-soft: #F1F3F8;
    --border: #DDE1EA;
    --text-main: #172033;
    --text-muted: #667085;
    --accent: #6D5DFB;
    --accent-dark: #5848E5;
    --accent-light: #EDEAFF;
}

/* Entire application */
.stApp {
    background:
        radial-gradient(
            circle at 85% 2%,
            rgba(109, 93, 251, 0.12),
            transparent 27rem
        ),
        var(--app-bg);
    color: var(--text-main);
}

.block-container {
    max-width: 1280px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1,
h2,
h3,
h4,
p,
label {
    color: var(--text-main);
}

h1,
h2,
h3 {
    letter-spacing: -0.025em;
}

/* Hero card */
.hero-container {
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(109, 93, 251, 0.22);
    border-radius: 22px;
    background:
        radial-gradient(
            circle at top right,
            rgba(109, 93, 251, 0.16),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #FFFFFF,
            #F1EFFF
        );
    box-shadow: 0 14px 38px rgba(30, 41, 59, 0.08);
}

/* Metrics */
[data-testid="stMetric"] {
    min-height: 105px;
    padding: 1rem 1.15rem;
    border: 1px solid var(--border);
    border-radius: 16px;
    background: var(--surface);
    box-shadow: 0 7px 22px rgba(30, 41, 59, 0.06);
}

[data-testid="stMetric"]:hover {
    border-color: rgba(109, 93, 251, 0.5);
    transform: translateY(-1px);
    transition: 0.15s ease;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-size: 0.84rem;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: var(--text-main);
    font-size: 1.45rem;
    font-weight: 800;
}

/* Main buttons */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border: 1px solid var(--accent);
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        var(--accent),
        var(--accent-dark)
    );
    color: #FFFFFF;
    font-weight: 700;
    box-shadow: 0 7px 18px rgba(109, 93, 251, 0.2);
    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.stButton > button:hover {
    border-color: var(--accent-dark);
    background: linear-gradient(
        135deg,
        #796AFF,
        var(--accent)
    );
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(109, 93, 251, 0.28);
}

.stButton > button:disabled {
    border-color: #D8DCE5;
    background: #E8EAF0;
    color: #98A2B3;
    box-shadow: none;
}

/* Download buttons */
.stDownloadButton > button {
    width: 100%;
    min-height: 43px;
    border: 1px solid var(--border);
    border-radius: 11px;
    background: var(--surface);
    color: var(--text-main);
    font-weight: 700;
}

.stDownloadButton > button:hover {
    border-color: var(--accent);
    background: var(--accent-light);
    color: var(--accent-dark);
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 0.4rem;
    padding: 0.4rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: #EEF0F6;
}

[data-baseweb="tab"] {
    min-height: 45px;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
    border-radius: 10px;
    color: var(--text-muted);
    font-weight: 700;
}

[data-baseweb="tab"]:hover {
    color: var(--text-main);
    background: #FFFFFF;
}

[aria-selected="true"][data-baseweb="tab"] {
    color: #FFFFFF;
    background: var(--accent);
    box-shadow: 0 5px 16px rgba(109, 93, 251, 0.22);
}

/* File upload */
[data-testid="stFileUploader"] {
    padding: 0.5rem;
    border: 1px dashed rgba(109, 93, 251, 0.65);
    border-radius: 16px;
    background: rgba(109, 93, 251, 0.035);
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 145px;
    border-radius: 13px;
    background: #FFFFFF;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--text-muted);
}

/* Text input */
textarea,
input {
    color: var(--text-main) !important;
}

textarea {
    border: 1px solid var(--border) !important;
    border-radius: 13px !important;
    background: #FFFFFF !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* Dropdown */
[data-baseweb="select"] > div {
    border-color: var(--border) !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
    color: var(--text-main) !important;
}

[data-baseweb="popover"] {
    color: var(--text-main);
}

[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[role="option"] {
    color: var(--text-main) !important;
    background: #FFFFFF !important;
}

[role="option"]:hover {
    background: var(--accent-light) !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    padding: 0.95rem 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 16px;
    background: var(--surface);
    box-shadow: 0 5px 16px rgba(30, 41, 59, 0.05);
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    margin-left: 7%;
    border-color: rgba(109, 93, 251, 0.35);
    background: #F3F1FF;
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) {
    margin-right: 7%;
}

[data-testid="stChatInput"] {
    border: 1px solid var(--border);
    border-radius: 15px;
    background: #FFFFFF;
}

/* Alerts and expanders */
[data-testid="stAlert"] {
    border-radius: 13px;
}

[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--surface);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
    border-radius: 15px !important;
    background: var(--surface);
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
    background: #FFFFFF;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] hr {
    border-color: var(--border);
}

/* Dividers */
hr {
    border-color: var(--border);
}

/* Footer */
.app-footer {
    margin-top: 2rem;
    padding: 1.4rem 0 0.45rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    text-align: center;
    font-size: 0.83rem;
}

.tech-badge {
    display: inline-block;
    padding: 0.25rem 0.55rem;
    margin: 0.18rem;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: #FFFFFF;
    color: var(--text-muted);
    font-size: 0.76rem;
}

footer {
    visibility: hidden;
}

/* Responsive */
@media (max-width: 700px) {
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
# Sidebar
# -------------------------------------------------

show_sidebar()


# -------------------------------------------------
# Hero section
# -------------------------------------------------

with st.container(border=True):
    st.caption("AI-POWERED MEETING INTELLIGENCE")

    st.title("📝 AI Meeting Assistant")

    st.markdown(
        """
Turn documents, audio recordings, browser recordings, and meeting videos
into structured insights. Generate professional notes, identify action
items, ask contextual follow-up questions, and export the results.
"""
    )


# -------------------------------------------------
# Meeting source
# -------------------------------------------------

transcript = transcript_section()


# -------------------------------------------------
# Metrics
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
# Workspace
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
- Generate structured notes
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