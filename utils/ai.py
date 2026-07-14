from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_notes(transcript):
    prompt = f"""
You are an expert meeting assistant.

Analyze the following meeting transcript and generate professional meeting notes.

Include the following sections in Markdown format:

# Executive Summary

# Key Discussion Points

# Decisions Made

# Action Items

# Next Steps

Meeting Transcript:

{transcript}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional meeting assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content


def ask_question(transcript, question):

    prompt = f"""
You are an intelligent Meeting Assistant.

Use ONLY the meeting transcript below.

If the answer isn't present in the transcript,
reply:

"I couldn't find that information in the transcript."

Meeting Transcript:

{transcript}

User Question:

{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You answer questions only from meeting transcripts."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content