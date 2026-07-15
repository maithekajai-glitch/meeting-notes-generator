import streamlit as st


def show_sidebar():
    with st.sidebar:
        st.title("📝 Meeting Assistant")
        st.caption("AI-powered meeting intelligence")

        st.divider()

        st.success("Groq connected", icon="✅")

        st.markdown("### Workspace")

        st.markdown(
            """
            **Generate notes**  
            Create structured summaries and action items.

            **Chat with transcript**  
            Ask grounded questions about the meeting.

            **Export results**  
            Download PDF, DOCX, or Markdown.
            """
        )

        st.divider()

        st.markdown("### Supported files")

        st.caption("TXT · PDF · DOCX")

        st.divider()

        if st.button(
            "Clear session",
            key="clear_session_button",
            use_container_width=True,
        ):
            st.session_state.notes = ""
            st.session_state.messages = []
            st.session_state.last_transcript = ""
            st.rerun()