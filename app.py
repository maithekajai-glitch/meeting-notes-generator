import streamlit as st

from components.analytics import analytics_section
from components.chat import chat_section
from components.notes import notes_section
from components.sidebar import show_sidebar
from components.transcript import transcript_section
from components.email_draft import email_draft_section


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="assets/favicon.png",
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

/* ---------- App Background ---------- */

.stApp{
background:
radial-gradient(circle at top left, rgba(124,58,237,.14), transparent 28%),
radial-gradient(circle at bottom right, rgba(59,130,246,.12), transparent 32%),
linear-gradient(180deg,#F8FAFC,#EEF4FF);
}

/* ---------- Page ---------- */

.block-container{
max-width:1280px;
padding-top:1.5rem;
padding-bottom:2.5rem;
}

/* ---------- Hero ---------- */

.hero-section{

padding:2.2rem;

border-radius:24px;

background:
linear-gradient(
135deg,
rgba(255,255,255,.82),
rgba(255,255,255,.65)
);

backdrop-filter:blur(18px);

border:1px solid rgba(255,255,255,.55);

box-shadow:
0 20px 60px rgba(60,72,88,.12);

margin-bottom:2rem;

}

.hero-badge{

display:inline-block;

padding:.45rem .8rem;

border-radius:999px;

background:#F3E8FF;

color:#7C3AED;

font-size:.8rem;

font-weight:700;

margin-bottom:1rem;

}

.hero-title{

font-size:2.7rem;

font-weight:800;

color:#111827;

margin-bottom:.6rem;

}

.hero-description{

font-size:1.08rem;

line-height:1.8;

color:#64748B;

max-width:780px;

}

/* ---------- Glass Cards ---------- */

[data-testid="stVerticalBlockBorderWrapper"]{

background:
rgba(255,255,255,.72);

backdrop-filter:blur(18px);

border:1px solid rgba(255,255,255,.65);

border-radius:20px;

box-shadow:
0 15px 40px rgba(30,41,59,.08);

padding:.4rem;

transition:.25s;

}

[data-testid="stVerticalBlockBorderWrapper"]:hover{

transform:translateY(-3px);

box-shadow:
0 22px 50px rgba(124,58,237,.12);

}

/* ---------- Metrics ---------- */

[data-testid="stMetric"]{

background:white;

border-radius:18px;

padding:1rem;

border:none;

box-shadow:
0 10px 25px rgba(30,41,59,.07);

}

[data-testid="stMetricValue"]{

font-size:1.7rem;

font-weight:800;

color:#111827;

}

[data-testid="stMetricLabel"]{

color:#64748B;

}

/* ---------- Buttons ---------- */

.stButton > button {

    width: 100%;

    border: none;

    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #7C3AED,
        #8B5CF6
    );

    color: #FFFFFF !important;

    font-weight: 700;

    font-size: 16px;

    height: 48px;

    transition: .2s;

    box-shadow:
        0 10px 20px rgba(124,58,237,.22);
}

.stButton > button p,
.stButton > button span,
.stButton > button div {

    color: #FFFFFF !important;
}

.stButton > button:hover {

    color: #FFFFFF !important;

    transform: translateY(-2px);

    box-shadow:
        0 18px 35px rgba(124,58,237,.28);
}

.stButton > button:focus,
.stButton > button:active {

    color: #FFFFFF !important;
}

/* ---------- Download Button ---------- */

.stDownloadButton>button{

background:white;

border:1px solid #E2E8F0;

border-radius:14px;

font-weight:600;

height:45px;

}

/* ---------- Tabs ---------- */

[data-baseweb="tab-list"]{

background:rgba(255,255,255,.55);

backdrop-filter:blur(14px);

padding:.4rem;

border-radius:18px;

gap:.4rem;

}

[data-baseweb="tab"]{

border-radius:12px;

font-weight:700;

color:#64748B;

}

[aria-selected="true"][data-baseweb="tab"]{

background:
linear-gradient(
135deg,
#7C3AED,
#8B5CF6
);

color:white;

box-shadow:
0 8px 20px rgba(124,58,237,.22);

}

/* ---------- File Upload ---------- */

[data-testid="stFileUploader"]{

border-radius:18px;

background:white;

border:2px dashed #C4B5FD;

}

/* ---------- Text Area ---------- */

textarea{

border-radius:15px !important;

border:1px solid #E2E8F0 !important;

background:white !important;

}

/* ---------- Chat ---------- */

[data-testid="stChatMessage"]{

background:white;

border-radius:18px;

border:none;

box-shadow:
0 8px 20px rgba(0,0,0,.05);

}

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#FFFFFF,
#F8FAFC
);

border-right:1px solid #E2E8F0;

}

/* ---------- Expander ---------- */

[data-testid="stExpander"]{

border-radius:16px;

overflow:hidden;

}

/* ---------- Scrollbar ---------- */

::-webkit-scrollbar{

width:8px;

}

::-webkit-scrollbar-thumb{

background:#C4B5FD;

border-radius:20px;

}

/* ---------- Footer ---------- */

.app-footer{

margin-top:2rem;

padding-top:1rem;

text-align:center;

color:#64748B;

}

footer{

visibility:hidden;

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

st.markdown(
    """
<div class="hero-section">

<div class="hero-badge">
🚀 AI Powered Meeting Intelligence
</div>

<div class="hero-title">
AI Meeting Assistant
</div>

<div class="hero-description">
Transform documents, audio recordings, browser recordings, and meeting videos into professional meeting notes, analytics, follow-up emails and contextual AI conversations.
</div>

</div>
""",
    unsafe_allow_html=True,
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

notes_tab, analytics_tab, email_tab, chat_tab, guide_tab = st.tabs(
    [
        "📝 Meeting Notes",
        "📊 Analytics",
        "📧 Follow-up Email",
        "💬 Ask the Meeting",
        "✨ Quick Guide",
    ]
)

with notes_tab:
    notes_section(transcript)

with analytics_tab:
    analytics_section(transcript)

with email_tab:
    email_draft_section(transcript)

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
- Generate structured meeting notes
- Review meeting analytics
- Draft a follow-up email
- Ask transcript-based questions
- Export the results
"""
            )

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

footer_col1, footer_col2 = st.columns([1, 8])

with footer_col1:
    st.image(
        "assets/icon.png",
        width=40,
    )

with footer_col2:
    st.caption(
        "AI Meeting Assistant • Powered by Streamlit • Groq • Whisper"
    )