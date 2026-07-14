import streamlit as st
from utils.ai import generate_notes, ask_question

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="📝",
    layout="wide",
)

# -------------------------
# Custom CSS
# -------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton>button {
    width:100%;
    border-radius:12px;
    height:50px;
    font-size:18px;
}

.stTextArea textarea{
    border-radius:10px;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.title("📝 AI Meeting Assistant")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
✅ Generate Meeting Notes

✅ Ask Questions

🚀 Fast AI Responses

📄 Markdown Output
""")

    st.markdown("---")

    st.info(
        "Paste a meeting transcript and let AI summarize it instantly."
    )

# -------------------------
# Title
# -------------------------

st.title("📝 AI Meeting Assistant")

st.caption("Generate professional meeting notes and chat with your meeting transcript.")

# -------------------------
# Session State
# -------------------------

if "notes" not in st.session_state:
    st.session_state.notes = ""

# -------------------------
# Layout
# -------------------------

left, right = st.columns([1,1])

# -------------------------
# LEFT
# -------------------------

with left:

    st.subheader("📄 Meeting Transcript")

    transcript = st.text_area(
        "",
        height=450,
        placeholder="Paste your meeting transcript here..."
    )

    st.caption(f"Characters : {len(transcript)}")

    if st.button("📝 Generate Meeting Notes"):

        if transcript.strip() == "":
            st.warning("Please paste a meeting transcript.")

        else:

            with st.spinner("Generating meeting notes..."):

                st.session_state.notes = generate_notes(transcript)

# -------------------------
# RIGHT
# -------------------------

with right:

    st.subheader("📑 Generated Notes")

    if st.session_state.notes:

        st.markdown(st.session_state.notes)

    else:

        st.info("Meeting notes will appear here.")

# -------------------------
# Divider
# -------------------------

st.divider()

# -------------------------
# Ask Questions
# -------------------------

st.subheader("💬 Ask Questions About the Meeting")

question = st.text_input(
    "Ask anything about the transcript..."
)

if st.button("🤖 Ask AI"):

    if transcript.strip() == "":

        st.warning("Please paste a transcript first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            answer = ask_question(
                transcript,
                question
            )

        st.success("Answer")

        st.write(answer)