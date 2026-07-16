import os
from typing import Any
import json
import re
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

def transcribe_media(media_file) -> str:
    """Transcribe speech from an uploaded audio or video file."""

    if media_file is None:
        raise ValueError("An audio or video file is required.")

    media_file.seek(0)

    file_name = getattr(
        media_file,
        "name",
        "meeting_recording.wav",
    )

    media_bytes = media_file.read()

    if not media_bytes:
        raise ValueError("The uploaded media file is empty.")

    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file_name, media_bytes),
        response_format="text",
        temperature=0.0,
    )

    if isinstance(transcription, str):
        transcript = transcription
    else:
        transcript = getattr(transcription, "text", "")

    transcript = str(transcript).strip()

    if not transcript:
        raise RuntimeError(
            "No speech could be extracted from the uploaded media."
        )

    return transcript

def extract_action_items(transcript: str) -> list[dict[str, str]]:
    """Extract structured action items from a meeting transcript."""

    if not transcript.strip():
        return []

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract action items from meeting transcripts. "
                    "Return only valid JSON. Do not include Markdown, explanations, "
                    "or code fences. Do not invent information."
                ),
            },
            {
                "role": "user",
                "content": f"""
Extract every confirmed action item from the meeting transcript.

Return a JSON array using exactly this structure:

[
  {{
    "owner": "Person responsible",
    "task": "Specific task",
    "deadline": "Deadline stated in transcript",
    "priority": "High, Medium, Low, or Not specified",
    "status": "Pending"
  }}
]

Rules:

1. Include only genuine tasks or commitments.
2. Do not treat general discussion as an action item.
3. Preserve names and deadlines exactly as stated.
4. Use "Not specified" when the owner or deadline is missing.
5. Set status to "Pending".
6. Infer priority only when clearly supported:
   - High: urgent, critical, blocking, or immediate
   - Medium: normal committed work
   - Low: optional or non-urgent
   - Otherwise: Not specified
7. If there are no action items, return [].
8. Return only valid JSON.

Meeting transcript:

{transcript}
""",
            },
        ],
        temperature=0.0,
        max_completion_tokens=1200,
    )

    raw_output = response.choices[0].message.content or "[]"

    # Remove accidental Markdown code fences.
    cleaned_output = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        raw_output.strip(),
        flags=re.IGNORECASE,
    )

    try:
        parsed_items = json.loads(cleaned_output)
    except json.JSONDecodeError:
        return []

    if not isinstance(parsed_items, list):
        return []

    validated_items: list[dict[str, str]] = []

    for item in parsed_items:
        if not isinstance(item, dict):
            continue

        task = str(item.get("task", "")).strip()

        if not task:
            continue

        priority = str(
            item.get("priority", "Not specified")
        ).strip()

        if priority not in {
            "High",
            "Medium",
            "Low",
            "Not specified",
        }:
            priority = "Not specified"

        validated_items.append(
            {
                "Owner": str(
                    item.get("owner", "Not specified")
                ).strip()
                or "Not specified",
                "Task": task,
                "Deadline": str(
                    item.get("deadline", "Not specified")
                ).strip()
                or "Not specified",
                "Priority": priority,
                "Status": str(
                    item.get("status", "Pending")
                ).strip()
                or "Pending",
            }
        )

    return validated_items


def extract_meeting_analytics(transcript: str) -> dict[str, Any]:
    """Extract structured analytics from a meeting transcript."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a meeting analytics specialist. "
                    "Extract accurate structured information from meeting "
                    "transcripts. Use only information supported by the "
                    "transcript. Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": f"""
Analyze the meeting transcript and return one valid JSON object.

Use exactly this structure:

{{
  "participants": [
    "Participant name"
  ],
  "topics": [
    "Main topic"
  ],
  "decisions": [
    "Confirmed decision"
  ],
  "action_items": [
    {{
      "owner": "Person responsible",
      "task": "Task description",
      "deadline": "Deadline or Not specified",
      "priority": "High, Medium, Low, or Not specified"
    }}
  ],
  "deadlines": [
    {{
      "date": "Date or time exactly as mentioned",
      "event": "Associated task or event"
    }}
  ],
  "risks": [
    "Risk or blocker"
  ],
  "open_questions": [
    "Unresolved question"
  ],
  "sentiment": {{
    "label": "Positive, Neutral, Mixed, or Negative",
    "explanation": "Brief explanation supported by the transcript"
  }},
  "summary": "A concise two or three sentence overview"
}}

Rules:

1. Use only information found in the transcript.
2. Do not invent participant names, dates, deadlines or decisions.
3. Include only confirmed decisions under decisions.
4. Include only genuine commitments under action_items.
5. Use empty arrays when no items are found.
6. Use "Not specified" when an action-item field is missing.
7. Keep topics concise.
8. Return JSON only, with no Markdown or code fences.

Meeting transcript:

{transcript}
""",
            },
        ],
        temperature=0.0,
        max_completion_tokens=1800,
        response_format={"type": "json_object"},
    )

    raw_output = response.choices[0].message.content or "{}"

    # Remove accidental Markdown fences if the model includes them.
    cleaned_output = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        raw_output.strip(),
        flags=re.IGNORECASE,
    )

    try:
        analytics = json.loads(cleaned_output)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "The analytics response was not valid JSON."
        ) from error

    if not isinstance(analytics, dict):
        raise RuntimeError(
            "The analytics response must be a JSON object."
        )

    # Ensure every expected field exists.
    analytics.setdefault("participants", [])
    analytics.setdefault("topics", [])
    analytics.setdefault("decisions", [])
    analytics.setdefault("action_items", [])
    analytics.setdefault("deadlines", [])
    analytics.setdefault("risks", [])
    analytics.setdefault("open_questions", [])
    analytics.setdefault(
        "sentiment",
        {
            "label": "Neutral",
            "explanation": "No sentiment analysis was available.",
        },
    )
    analytics.setdefault("summary", "")

    # Validate list fields.
    list_fields = [
        "participants",
        "topics",
        "decisions",
        "action_items",
        "deadlines",
        "risks",
        "open_questions",
    ]

    for field in list_fields:
        if not isinstance(analytics[field], list):
            analytics[field] = []

    if not isinstance(analytics["sentiment"], dict):
        analytics["sentiment"] = {
            "label": "Neutral",
            "explanation": "No sentiment analysis was available.",
        }

    return analytics