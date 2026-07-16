import streamlit as st

from components.downloads import download_section
from utils.ai import generate_notes


MEETING_TYPES = [
    "General Meeting",
    "Stand-up Meeting",
    "Client Meeting",
    "Interview",
    "Brainstorming",
    "Sprint Planning",
    "Sales Call",
]


def notes_section(transcript: str) -> None:
    """Generate and display meeting notes."""

    if "notes" not in st.session_state:
        st.session_state.notes = ""

    if "meeting_type" not in st.session_state:
        st.session_state.meeting_type = "General Meeting"

    st.subheader("📑 Generated Meeting Notes")

    meeting_type = st.selectbox(
        "Choose meeting type",
        options=MEETING_TYPES,
        index=MEETING_TYPES.index(
            st.session_state.meeting_type
        ),
        key="meeting_type_selector",
    )

    st.session_state.meeting_type = meeting_type

    st.caption(
        "The selected meeting type will determine how the notes are structured."
    )

    if st.button(
        "✨ Generate Meeting Notes",
        key="generate_notes_button",
        use_container_width=True,
        disabled=not bool(transcript.strip()),
    ):
        if not transcript.strip():
            st.warning(
                "Paste, upload, record, or transcribe a meeting first."
            )
        else:
            try:
                with st.spinner(
                    f"Generating {meeting_type.lower()} notes..."
                ):
                    # Step 2 will pass meeting_type to this function.
                    st.session_state.notes = generate_notes(
    transcript=transcript,
    meeting_type=meeting_type,
)

                st.success(
                    f"{meeting_type} notes generated successfully."
                )

            except Exception as error:
                st.error(
                    "The meeting notes could not be generated. "
                    "Please try again."
                )

                print(f"Meeting-note generation error: {error}")

    if st.session_state.notes:
        st.markdown(st.session_state.notes)

        download_section(
            st.session_state.notes
        )
    else:
        st.info(
            "Generated notes will appear here."
        )