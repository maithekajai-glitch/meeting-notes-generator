import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your .env file locally "
        "or to Streamlit Cloud Secrets when deployed."
    )

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_notes(transcript: str) -> str:
    """Generate detailed, structured meeting notes."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional meeting analyst. "
                    "Create accurate, concise, and actionable meeting notes. "
                    "Use only information present in the transcript. "
                    "Never invent names, dates, deadlines, decisions, or tasks."
                ),
            },
            {
                "role": "user",
                "content": f"""
Analyze the following meeting transcript and create professional notes in Markdown.

Use exactly these sections:

# Executive Summary
Write a short overview of the meeting in 3 to 5 sentences.

# Participants
List each participant mentioned in the transcript.
Write "Not identified" if no names are available.

# Key Discussion Points
Summarize the main topics discussed as bullet points.

# Decisions Made
List confirmed decisions.
Write "No confirmed decisions found" if none are present.

# Action Items
Create a Markdown table with these columns:

| Owner | Task | Deadline | Status |
|---|---|---|---|

Use "Not specified" when the owner, deadline, or status is missing.

# Deadlines and Dates
List every deadline, review date, release date, or scheduled event mentioned.

# Risks and Blockers
List problems, risks, dependencies, or blockers discussed.
Write "No risks or blockers identified" if none are present.

# Next Steps
List the immediate next steps in chronological order when possible.

# Open Questions
List unresolved questions or issues.
Write "No open questions identified" if none are present.

Important rules:
- Do not add facts that are not in the transcript.
- Preserve names and dates exactly as stated.
- Merge duplicate discussion points.
- Keep the notes concise and professional.
- Clearly distinguish confirmed decisions from suggestions.
- Do not treat every statement as an action item.

Meeting transcript:

{transcript}
""",
            },
        ],
        temperature=0.15,
        max_completion_tokens=1800,
    )

    return response.choices[0].message.content or ""


def ask_question(
    transcript: str,
    question: str,
    chat_history: list[dict[str, Any]] | None = None,
) -> str:
    """Answer questions using the transcript and previous chat history."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": f"""
You are an AI Meeting Assistant.

The meeting transcript below is the main source of truth.

Rules:
1. Answer only using information supported by the transcript.
2. Use previous messages to understand follow-up questions.
3. Do not invent names, dates, deadlines, decisions, or action items.
4. If the information is unavailable, reply:
   "I couldn't find that information in the transcript."
5. Keep the answer concise unless more detail is requested.

Meeting transcript:

{transcript}
""",
        }
    ]

    if chat_history:
        for message in chat_history[-10:]:
            role = message.get("role")
            content = str(message.get("content", "")).strip()

            if role in {"user", "assistant"} and content:
                messages.append(
                    {
                        "role": role,
                        "content": content,
                    }
                )

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_completion_tokens=700,
    )

    return response.choices[0].message.content or ""

def transcribe_audio(audio_file) -> str:
    """Convert uploaded or recorded audio into text using Groq."""

    if audio_file is None:
        raise ValueError("Audio file is required.")

    audio_file.seek(0)

    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(
            getattr(audio_file, "name", "meeting_audio.wav"),
            audio_file.read(),
        ),
        response_format="text",
        temperature=0.0,
    )

    if isinstance(transcription, str):
        return transcription.strip()

    return str(getattr(transcription, "text", "")).strip()