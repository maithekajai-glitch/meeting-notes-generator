import streamlit as st
from utils.ai import generate_notes

st.set_page_config(
    page_title="Meeting Notes Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Meeting Notes Generator")

st.write("Paste your meeting transcript below and let AI generate structured meeting notes.")

transcript = st.text_area(
    "Meeting Transcript",
    height=300,
    placeholder="Paste your meeting transcript here..."
)

if st.button("Generate Notes"):

    if not transcript.strip():
        st.warning("Please paste a meeting transcript.")
    else:
        with st.spinner("Generating meeting notes..."):
            notes = generate_notes(transcript)

        st.success("Meeting notes generated successfully!")

        st.markdown(notes)