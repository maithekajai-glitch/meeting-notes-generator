import streamlit as st

from utils.ai import generate_followup_email


EMAIL_TONES = [
    "Professional",
    "Friendly",
    "Formal",
    "Concise",
]


def email_draft_section(transcript: str) -> None:
    """Generate, edit, copy, and download a meeting follow-up email."""

    st.subheader("📧 Follow-up Email Generator")

    st.caption(
        "Create an editable email summarizing the meeting, decisions, "
        "action items, and next steps."
    )

    if "email_draft" not in st.session_state:
        st.session_state.email_draft = ""

    recipient_col, tone_col = st.columns(2)

    with recipient_col:
        recipient = st.text_input(
            "Recipient",
            value="Team",
            placeholder="Team, Client, Hiring Manager...",
            key="email_recipient",
        )

    with tone_col:
        tone = st.selectbox(
            "Email tone",
            options=EMAIL_TONES,
            key="email_tone",
        )

    meeting_type = st.session_state.get(
        "meeting_type",
        "General Meeting",
    )

    st.caption(f"Meeting type: {meeting_type}")

    if st.button(
        "✨ Draft Follow-up Email",
        key="generate_followup_email_button",
        use_container_width=True,
        disabled=not bool(transcript.strip()),
    ):
        if not transcript.strip():
            st.warning(
                "Paste, upload, record, or transcribe a meeting first."
            )
        else:
            try:
                with st.spinner("Drafting the follow-up email..."):
                    email = generate_followup_email(
                        transcript=transcript,
                        recipient=recipient.strip() or "Team",
                        tone=tone,
                        meeting_type=meeting_type,
                    )

                st.session_state.email_draft = email

                st.success("Follow-up email generated successfully.")

            except Exception as error:
                st.error(
                    "The follow-up email could not be generated. "
                    "Please try again."
                )

                print(f"Follow-up email generation error: {error}")

    if not st.session_state.email_draft:
        st.info("Your generated email will appear here.")
        return

    edited_email = st.text_area(
        "Edit email draft",
        value=st.session_state.email_draft,
        height=440,
        key="email_draft_editor",
    )

    st.session_state.email_draft = edited_email

    st.download_button(
        label="⬇ Download Email as TXT",
        data=edited_email.encode("utf-8"),
        file_name="meeting_followup_email.txt",
        mime="text/plain",
        key="download_followup_email",
        use_container_width=True,
    )