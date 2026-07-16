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


def generate_notes(
    transcript: str,
    meeting_type: str = "General Meeting",
) -> str:
    """Generate notes tailored to the selected meeting type."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    meeting_templates = {
        "General Meeting": """
Use these sections:

# Executive Summary
# Participants
# Key Discussion Points
# Decisions Made
# Action Items
# Deadlines and Dates
# Risks and Blockers
# Next Steps
# Open Questions
""",
        "Stand-up Meeting": """
Use these sections:

# Stand-up Summary
# Participants
# Completed Work
# Work in Progress
# Today's Plans
# Blockers
# Action Items
# Follow-up Items
""",
        "Client Meeting": """
Use these sections:

# Client Meeting Summary
# Participants
# Client Requirements
# Key Discussion Points
# Client Concerns
# Decisions and Agreements
# Deliverables
# Action Items
# Deadlines
# Follow-up Plan
""",
        "Interview": """
Use these sections:

# Interview Summary
# Participants
# Candidate Background
# Skills and Experience
# Strengths
# Concerns or Gaps
# Questions Discussed
# Candidate Responses
# Follow-up Actions

Do not make a hiring decision unless the transcript explicitly contains one.
""",
        "Brainstorming": """
Use these sections:

# Brainstorming Summary
# Participants
# Problem or Goal
# Ideas Suggested
# Promising Ideas
# Concerns and Constraints
# Ideas Selected for Further Review
# Action Items
# Open Questions
# Next Brainstorming Steps
""",
        "Sprint Planning": """
Use these sections:

# Sprint Planning Summary
# Participants
# Sprint Goal
# Stories or Tasks Discussed
# Priorities
# Estimates Mentioned
# Assignments
# Dependencies
# Risks and Blockers
# Sprint Commitments
# Next Steps
""",
        "Sales Call": """
Use these sections:

# Sales Call Summary
# Participants
# Prospect Needs
# Pain Points
# Product or Service Discussed
# Objections
# Buying Signals
# Pricing or Commercial Discussion
# Commitments
# Follow-up Actions
# Next Steps
""",
    }

    selected_template = meeting_templates.get(
        meeting_type,
        meeting_templates["General Meeting"],
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional meeting analyst. "
                    "Create accurate, concise and actionable notes. "
                    "Use only information supported by the transcript. "
                    "Do not invent participants, facts, decisions, "
                    "deadlines, tasks or recommendations."
                ),
            },
            {
                "role": "user",
                "content": f"""
Create professional notes for a {meeting_type}.

{selected_template}

Formatting rules:

- Use Markdown.
- Keep the notes concise and easy to scan.
- Use bullet points where appropriate.
- For action items, create this Markdown table:

| Owner | Task | Deadline | Status |
|---|---|---|---|

- Use "Not specified" when an owner, deadline or status is missing.
- Clearly distinguish confirmed decisions from suggestions.
- Do not treat general discussion as an action item.
- Merge duplicate points.
- Preserve names and dates exactly as stated.
- When a section has no information, state that clearly.

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

Use this structure:

{{
  "participants": [],
  "topics": [],
  "decisions": [],
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
  "risks": [],
  "open_questions": [],
  "sentiment": {{
    "label": "Positive, Neutral, Mixed, or Negative",
    "explanation": "Brief explanation"
  }},
  "summary": "A concise meeting overview"
}}

Rules:
- Use only information found in the transcript.
- Do not invent names, decisions, dates, or tasks.
- Use empty arrays when nothing is found.
- Return JSON only.

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
            "explanation": "No sentiment information was available.",
        },
    )
    analytics.setdefault("summary", "")

    return analytics

def generate_followup_email(
    transcript: str,
    tone: str = "Professional",
    meeting_type: str = "General Meeting",
) -> str:
    """Generate a professional follow-up email from a meeting transcript."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    valid_tones = {
        "Professional",
        "Friendly",
        "Formal",
        "Concise",
    }

    if tone not in valid_tones:
        tone = "Professional"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional business communication assistant. "
                    "Write accurate follow-up emails using only information "
                    "supported by the meeting transcript. Do not invent names, "
                    "decisions, deadlines, or tasks."
                ),
            },
            {
                "role": "user",
                "content": f"""
Create a {tone.lower()} follow-up email for a {meeting_type}.

Use exactly this structure:

Subject: [clear and specific email subject]

Dear Sir/Ma'am,

[Brief opening sentence thanking the recipient or acknowledging the meeting.]

Meeting Summary:
[Short paragraph summarizing the meeting.]

Key Decisions:
- [Confirmed decision]

Action Items:
- [Owner] — [Task] — [Deadline]

Next Steps:
- [Next step]

Open Questions:
- [Unresolved question]

Best regards,
[Your Name]

Rules:

- Use only information supported by the transcript.
- Always begin the greeting with "Dear Sir/Ma'am,".
- Do not ask for or insert a recipient name.
- Keep the email professional and easy to scan.
- Preserve names and deadlines exactly as stated.
- Include only confirmed decisions.
- Include only genuine commitments as action items.
- Use "Not specified" when an owner or deadline is missing.
- Write "No confirmed decisions were recorded" when needed.
- Write "No action items were recorded" when needed.
- Write "No open questions were recorded" when needed.
- Do not use Markdown headings with # symbols.
- Do not write anything before "Subject:".

Meeting transcript:

{transcript}
""",
            },
        ],
        temperature=0.2,
        max_completion_tokens=1200,
    )

    email = response.choices[0].message.content or ""

    if not email.strip():
        raise RuntimeError("The email draft was empty.")

    return email.strip()


    

    