from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_notes(transcript):
    prompt = f"""
You are an expert meeting assistant.

Analyze the following meeting transcript and generate the output in Markdown format.

Include the following sections:

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