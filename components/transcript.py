import streamlit as st
from utils.file_parser import extract_text


def transcript_section():

    st.subheader("📄 Meeting Transcript")

    input_method = st.radio(
        "Choose Input Method",
        ["Paste Transcript", "Upload File"],
        horizontal=True
    )

    transcript = ""

    if input_method == "Paste Transcript":

        transcript = st.text_area(
            "",
            height=420,
            placeholder="Paste your meeting transcript here..."
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload Transcript",
            type=["txt", "pdf", "docx"]
        )

        if uploaded_file is not None:

            transcript = extract_text(uploaded_file)

            st.success("✅ File uploaded successfully!")

            with st.expander("Preview Transcript"):
                st.write(transcript)

    # Clear chat when transcript changes
    if "last_transcript" not in st.session_state:
        st.session_state.last_transcript = ""

    if transcript != st.session_state.last_transcript:

        if "messages" in st.session_state:
            st.session_state.messages = []

        st.session_state.last_transcript = transcript

    st.caption(f"Characters: {len(transcript)}")

    return transcript