import streamlit as st
from utils.ai import generate_notes


def notes_section(transcript):

    if "notes" not in st.session_state:
        st.session_state.notes = ""

    st.subheader("📑 Generated Meeting Notes")

    if st.button("📝 Generate Meeting Notes"):

        if transcript.strip() == "":

            st.warning("Please provide a meeting transcript.")

        else:

            with st.spinner("Generating meeting notes..."):

                st.session_state.notes = generate_notes(transcript)

    if st.session_state.notes:

        st.markdown(st.session_state.notes)

    else:

        st.info("Meeting notes will appear here.")