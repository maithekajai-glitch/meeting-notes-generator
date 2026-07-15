import streamlit as st

from utils.ai import transcribe_audio
from utils.file_parser import extract_text


def transcript_section() -> str:
    """Collect transcript text from paste, document upload, audio upload, or recording."""

    st.subheader("📄 Meeting Transcript")

    input_method = st.radio(
        "Choose input method",
        [
            "Paste Transcript",
            "Upload Document",
            "Upload Audio",
            "Record Audio",
        ],
        horizontal=True,
        key="transcript_input_method",
    )

    transcript = ""

    if input_method == "Paste Transcript":
        transcript = st.text_area(
            "Paste your transcript",
            height=360,
            placeholder="Paste your meeting transcript here...",
            label_visibility="collapsed",
            key="pasted_transcript",
        )

    elif input_method == "Upload Document":
        uploaded_file = st.file_uploader(
            "Upload a TXT, PDF, or DOCX transcript",
            type=["txt", "pdf", "docx"],
            key="document_uploader",
        )

        if uploaded_file is not None:
            try:
                transcript = extract_text(uploaded_file)

                st.success("Document processed successfully.")

            except Exception as error:
                st.error(
                    "The document could not be processed. "
                    "Check that it contains readable text."
                )
                print(f"Document parsing error: {error}")

    elif input_method == "Upload Audio":
        uploaded_audio = st.file_uploader(
            "Upload a meeting recording",
            type=["mp3", "wav", "m4a", "mp4", "mpeg", "webm"],
            key="audio_uploader",
        )

        if uploaded_audio is not None:
            st.audio(uploaded_audio)

            if st.button(
                "🎙️ Transcribe Uploaded Audio",
                key="transcribe_uploaded_audio_button",
                use_container_width=True,
            ):
                try:
                    with st.spinner("Transcribing the meeting audio..."):
                        transcript = transcribe_audio(uploaded_audio)

                    st.session_state.audio_transcript = transcript
                    st.success("Audio transcribed successfully.")

                except Exception as error:
                    st.error(
                        "The audio could not be transcribed. "
                        "Check the file and try again."
                    )
                    print(f"Uploaded audio transcription error: {error}")

            transcript = st.session_state.get("audio_transcript", "")

    else:
        recorded_audio = st.audio_input(
            "Record the meeting",
            sample_rate=16000,
            key="meeting_audio_recorder",
        )

        if recorded_audio is not None:
            st.audio(recorded_audio)

            if st.button(
                "🎙️ Transcribe Recording",
                key="transcribe_recording_button",
                use_container_width=True,
            ):
                try:
                    with st.spinner("Transcribing your recording..."):
                        transcript = transcribe_audio(recorded_audio)

                    st.session_state.recorded_transcript = transcript
                    st.success("Recording transcribed successfully.")

                except Exception as error:
                    st.error(
                        "The recording could not be transcribed. "
                        "Please record it again and retry."
                    )
                    print(f"Recorded audio transcription error: {error}")

            transcript = st.session_state.get(
                "recorded_transcript",
                "",
            )

    if transcript:
        with st.expander("Preview transcript", expanded=False):
            st.text_area(
                "Transcript preview",
                value=transcript,
                height=260,
                disabled=True,
                label_visibility="collapsed",
                key="transcript_preview",
            )

    if "last_transcript" not in st.session_state:
        st.session_state.last_transcript = ""

    if transcript != st.session_state.last_transcript:
        st.session_state.messages = []
        st.session_state.notes = ""
        st.session_state.last_transcript = transcript

    st.caption(f"Words: {len(transcript.split()):,}")

    return transcript