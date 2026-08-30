import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


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

Answer the user's questions clearly and naturally.
Do not pretend to control systems or devices unless
the user explicitly asks for a capability that exists.
"""

        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.7,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        )

    def ask(self, prompt, context=None):
        """
        Send a prompt to Gemini and return the response.
        """

        if context:
            contents = f"""
Context:
{context}

User:
{prompt}
"""
        else:
            contents = prompt

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=self.config,
        )

        if not response or not response.text:
            return "I received an empty response from my AI system."

        return response.text.strip()


ai_engine = AIEngine()