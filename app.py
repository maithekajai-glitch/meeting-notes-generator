import streamlit as st

st.set_page_config(
    page_title="Meeting Notes Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Meeting Notes Generator")

st.write(
    "Upload a meeting transcript or paste one below, and let AI generate professional meeting notes."
)

# Input method
option = st.radio(
    "Choose an input method:",
    ["Paste Transcript", "Upload File"]
)

if option == "Paste Transcript":
    transcript = st.text_area(
        "Paste your meeting transcript",
        height=300,
        placeholder="Paste your meeting transcript here..."
    )

else:
    uploaded_file = st.file_uploader(
        "Upload a transcript",
        type=["txt", "pdf", "docx"]
    )

if st.button("Generate Notes"):
    st.success("✅ Ready to generate meeting notes (AI will be added in the next milestone).")