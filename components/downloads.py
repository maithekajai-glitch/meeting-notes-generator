import streamlit as st

from utils.exporter import (
    export_markdown,
    export_docx,
    export_pdf,
)


def download_section(notes):

    if not notes:
        return

    st.divider()

    st.subheader("📥 Download Meeting Notes")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            label="⬇ Markdown",
            data=export_markdown(notes),
            file_name="meeting_notes.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="⬇ DOCX",
            data=export_docx(notes),
            file_name="meeting_notes.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col3:

        st.download_button(
            label="⬇ PDF",
            data=export_pdf(notes),
            file_name="meeting_notes.pdf",
            mime="application/pdf",
            use_container_width=True
        )