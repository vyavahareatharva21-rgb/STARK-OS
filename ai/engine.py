import os
from google import genai
from google.genai import types


class AIEngine:
    """
    STARK-OS AI Engine.

    Gemini handles natural-language questions and
    requests that the local command system does not understand.
    """

    def __init__(self):
        self.provider = "gemini"
        self.model = "gemini-3.6-flash"

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

        self.system_instruction = """
You are STARK, a personal AI assistant.

Your personality:
- Intelligent
- Calm
- Helpful
- Concise
- Professional
- Slightly futuristic

You are running inside STARK-OS.

Rules:
- Answer the user's question directly.
- Keep responses reasonably concise.
- Do not claim to control the computer unless STARK-OS explicitly provides that capability.
- Do not pretend to have performed actions you cannot perform.
"""

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
            ),
        )

        return response.text.strip()


ai_engine = AIEngine()
