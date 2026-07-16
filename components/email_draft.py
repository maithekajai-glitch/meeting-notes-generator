from urllib.parse import quote

import streamlit as st

from utils.ai import generate_followup_email


EMAIL_TONES = [
    "Professional",
    "Friendly",
    "Formal",
    "Concise",
]


def _extract_subject_and_body(email_text: str) -> tuple[str, str]:
    """Extract a Subject line from the generated draft when present."""

    default_subject = "Meeting Follow-up"
    clean_text = email_text.strip()

    if not clean_text:
        return default_subject, ""

    first_line, separator, remaining_text = clean_text.partition("\n")

    if first_line.lower().startswith("subject:"):
        subject = first_line.split(":", maxsplit=1)[1].strip()

        return (
            subject or default_subject,
            remaining_text.strip() if separator else "",
        )

    return default_subject, clean_text


def email_draft_section(transcript: str) -> None:
    """Generate, edit, download, and share a follow-up email."""

    st.subheader("📧 Follow-up Email Generator")

    st.caption(
        "Create an editable email summarizing the meeting, "
        "then open it in Gmail or your default email application."
    )

    if "email_draft" not in st.session_state:
        st.session_state.email_draft = ""

    recipient_col, tone_col = st.columns(2)

    with recipient_col:
        recipient_name = st.text_input(
            "Recipient name or group",
            value="Team",
            placeholder="Team, Client, Hiring Manager...",
            key="email_recipient_name",
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
        try:
            with st.spinner("Drafting the follow-up email..."):
                email = generate_followup_email(
                    transcript=transcript,
                    recipient=recipient_name.strip() or "Team",
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

    subject, email_body = _extract_subject_and_body(
        edited_email
    )

    st.divider()
    st.markdown("### 📨 Share Email")

    recipient_email = st.text_input(
        "Recipient email address",
        placeholder="recipient@example.com",
        key="share_recipient_email",
    )

    safe_recipient = recipient_email.strip()

    gmail_url = (
        "https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={quote(safe_recipient)}"
        f"&su={quote(subject)}"
        f"&body={quote(email_body)}"
    )

    mailto_url = (
        f"mailto:{quote(safe_recipient)}"
        f"?subject={quote(subject)}"
        f"&body={quote(email_body)}"
    )

    share_col1, share_col2 = st.columns(2)

    with share_col1:
        st.link_button(
            "📨 Open in Gmail",
            gmail_url,
            use_container_width=True,
            disabled=not bool(safe_recipient),
        )

    with share_col2:
        st.link_button(
            "✉️ Open Email App",
            mailto_url,
            use_container_width=True,
            disabled=not bool(safe_recipient),
        )

    st.caption(
        "Review the recipient and draft in your email provider "
        "before pressing Send."
    )

    st.download_button(
        label="⬇ Download Email as TXT",
        data=edited_email.encode("utf-8"),
        file_name="meeting_followup_email.txt",
        mime="text/plain",
        key="download_followup_email",
        use_container_width=True,
    )