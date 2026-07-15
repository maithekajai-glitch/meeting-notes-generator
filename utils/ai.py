import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your local .env file "
        "or Streamlit Cloud Secrets."
    )

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_notes(transcript: str) -> str:
    """Generate structured meeting notes from a transcript."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional meeting assistant. "
                    "Create accurate, concise and well-structured meeting notes. "
                    "Do not invent information that is not present in the transcript."
                ),
            },
            {
                "role": "user",
                "content": f"""
Create professional meeting notes from the transcript below.

Use Markdown and include these sections:

# Executive Summary
# Participants
# Key Discussion Points
# Decisions Made
# Action Items
# Deadlines
# Risks and Blockers
# Next Steps
# Open Questions

For action items, include the owner and deadline when available.
Write "Not specified" when information is missing.

Meeting transcript:

{transcript}
""",
            },
        ],
        temperature=0.2,
        max_completion_tokens=1600,
    )

    return response.choices[0].message.content or ""


def ask_question(
    transcript: str,
    question: str,
    chat_history: list[dict[str, Any]] | None = None,
) -> str:
    """
    Answer a question using the transcript and previous conversation messages.

    chat_history format:
    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
    ]
    """

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    system_message = {
        "role": "system",
        "content": f"""
You are an AI Meeting Assistant.

Your primary source of truth is the meeting transcript below.

Rules:
1. Answer using only information supported by the transcript.
2. Use previous chat messages to understand follow-up questions and references.
3. Previous assistant answers are context, but the transcript remains authoritative.
4. Do not invent names, dates, decisions, deadlines or action items.
5. If the answer is not available, say:
   "I couldn't find that information in the transcript."
6. Keep answers clear and concise unless the user asks for detail.

Meeting transcript:

{transcript}
""",
    }

    messages: list[dict[str, str]] = [system_message]

    # Add previous conversation messages.
    if chat_history:
        for message in chat_history[-10:]:
            role = message.get("role")
            content = message.get("content", "").strip()

            if role in {"user", "assistant"} and content:
                messages.append(
                    {
                        "role": role,
                        "content": content,
                    }
                )

    # Add the latest question.
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