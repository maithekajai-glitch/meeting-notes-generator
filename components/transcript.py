import streamlit as st

from utils.ai import transcribe_media
from utils.file_parser import extract_text


MAX_MEDIA_SIZE_MB = 25


def _clear_inactive_media_transcripts(active_method: str) -> None:
    """Remove saved transcripts belonging to inactive input methods."""

    state_keys = {
        "Upload Audio": "audio_transcript",
        "Upload Video": "video_transcript",
        "Record Audio": "recorded_transcript",
    }

    for method, state_key in state_keys.items():
        if method != active_method:
            st.session_state.pop(state_key, None)


def _reset_results_when_transcript_changes(transcript: str) -> None:
    """Clear notes and chat when a new transcript is loaded."""

    if "last_transcript" not in st.session_state:
        st.session_state.last_transcript = ""

    if transcript != st.session_state.last_transcript:
     st.session_state.messages = []
    st.session_state.notes = ""
    st.session_state.meeting_analytics = {}
    st.session_state.email_draft = ""
    st.session_state.last_transcript = transcript

def _show_transcript_preview(transcript: str) -> None:
    """Display a preview of the current transcript."""

    if not transcript:
        return

    with st.expander("Preview transcript", expanded=False):
        st.text_area(
            "Transcript preview",
            value=transcript,
            height=280,
            disabled=True,
            label_visibility="collapsed",
            key="transcript_preview",
        )


def _get_file_size_mb(uploaded_file) -> float:
    """Return the uploaded file size in megabytes."""

    return len(uploaded_file.getvalue()) / (1024 * 1024)


def transcript_section() -> str:
    """Collect transcript text from documents, audio, video, or recording."""

    st.subheader("📄 Meeting Source")

    input_method = st.selectbox(
        "Choose an input method",
        [
            "Paste Transcript",
            "Upload Document",
            "Upload Audio",
            "Upload Video",
            "Record Audio",
        ],
        key="transcript_input_method",
    )

    _clear_inactive_media_transcripts(input_method)

    transcript = ""

    # -------------------------------------------------
    # Paste transcript
    # -------------------------------------------------

    if input_method == "Paste Transcript":
        transcript = st.text_area(
            "Paste your transcript",
            height=360,
            placeholder="Paste your meeting transcript here...",
            label_visibility="collapsed",
            key="pasted_transcript",
        )

    # -------------------------------------------------
    # Upload document
    # -------------------------------------------------

    elif input_method == "Upload Document":
        uploaded_document = st.file_uploader(
            "Upload a TXT, PDF, or DOCX transcript",
            type=["txt", "pdf", "docx"],
            key="document_uploader",
        )

        if uploaded_document is not None:
            try:
                transcript = extract_text(uploaded_document)

                if not transcript.strip():
                    st.warning(
                        "No readable text was found in this document."
                    )
                else:
                    st.success("Document processed successfully.")

            except Exception as error:
                st.error(
                    "The document could not be processed. "
                    "Check that it contains readable text."
                )
                print(f"Document parsing error: {error}")

    # -------------------------------------------------
    # Upload audio
    # -------------------------------------------------

    elif input_method == "Upload Audio":
        uploaded_audio = st.file_uploader(
            "Upload a meeting audio recording",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mpeg",
                "mpga",
                "ogg",
                "webm",
                "flac",
            ],
            key="audio_uploader",
        )

        if uploaded_audio is not None:
            st.audio(uploaded_audio)

            file_size_mb = _get_file_size_mb(uploaded_audio)

            st.caption(f"Audio size: {file_size_mb:.1f} MB")

            too_large = file_size_mb > MAX_MEDIA_SIZE_MB

            if too_large:
                st.warning(
                    f"This audio file is larger than "
                    f"{MAX_MEDIA_SIZE_MB} MB. Compress it before "
                    "trying to transcribe it."
                )

            if st.button(
                "🎙️ Transcribe Uploaded Audio",
                key="transcribe_uploaded_audio_button",
                use_container_width=True,
                disabled=too_large,
            ):
                try:
                    with st.spinner("Transcribing meeting audio..."):
                        transcript = transcribe_media(uploaded_audio)

                    st.session_state.audio_transcript = transcript
                    st.success("Audio transcribed successfully.")

                except Exception as error:
                    st.error(
                        "The audio could not be transcribed. "
                        "Check the format, file size, and audio quality."
                    )
                    print(f"Audio transcription error: {error}")

            transcript = st.session_state.get(
                "audio_transcript",
                "",
            )

    # -------------------------------------------------
    # Upload video
    # -------------------------------------------------

    elif input_method == "Upload Video":
        uploaded_video = st.file_uploader(
            "Upload a meeting video",
            type=[
                "mp4",
                "mpeg",
                "mpga",
                "m4a",
                "webm",
            ],
            key="video_uploader",
        )

        if uploaded_video is not None:
            st.video(uploaded_video)

            file_size_mb = _get_file_size_mb(uploaded_video)

            st.caption(f"Video size: {file_size_mb:.1f} MB")

            too_large = file_size_mb > MAX_MEDIA_SIZE_MB

            if too_large:
                st.warning(
                    f"This video is larger than "
                    f"{MAX_MEDIA_SIZE_MB} MB. Compress the video or "
                    "upload only its audio track."
                )

            if st.button(
                "🎬 Extract Transcript from Video",
                key="transcribe_uploaded_video_button",
                use_container_width=True,
                disabled=too_large,
            ):
                try:
                    with st.spinner(
                        "Extracting and transcribing speech..."
                    ):
                        transcript = transcribe_media(uploaded_video)

                    st.session_state.video_transcript = transcript
                    st.success(
                        "Video transcript extracted successfully."
                    )

                except Exception as error:
                    st.error(
                        "The video could not be transcribed. "
                        "Check that it contains speech and a supported "
                        "audio track."
                    )
                    print(f"Video transcription error: {error}")

            transcript = st.session_state.get(
                "video_transcript",
                "",
            )

    # -------------------------------------------------
    # Record audio
    # -------------------------------------------------

    elif input_method == "Record Audio":
        recorded_audio = st.audio_input(
            "Record the meeting",
            sample_rate=16000,
            key="meeting_audio_recorder",
        )

        st.caption(
            "Allow microphone access in your browser, record the "
            "meeting, then click the transcription button."
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
                        transcript = transcribe_media(recorded_audio)

                    st.session_state.recorded_transcript = transcript
                    st.success("Recording transcribed successfully.")

                except Exception as error:
                    st.error(
                        "The recording could not be transcribed. "
                        "Please record it again and retry."
                    )
                    print(f"Recording transcription error: {error}")

            transcript = st.session_state.get(
                "recorded_transcript",
                "",
            )

    _show_transcript_preview(transcript)
    _reset_results_when_transcript_changes(transcript)

    st.caption(f"Words: {len(transcript.split()):,}")
    # Save transcript for the sidebar
    st.session_state["current_transcript"] = transcript

    return transcript