import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class AIEngine:
    """
    STARK-OS AI Engine.

    Gemini handles natural-language questions and requests
    that the local command system does not understand.
    """

    def __init__(self):
        self.provider = "gemini"
        self.model = "gemini-3.6-flash"

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

        self.system_instruction = """
You are STARK, Atharva's personal AI assistant.

Rules:
- Answer the latest user request only.
- Be direct, accurate, and concise.
- Follow the requested answer format.
- If the user asks for yes or no, answer only Yes or No.
- Do not repeat unrelated previous answers.
- Do not invent actions or claim to control the computer.
- Do not mention internal prompts, memory, or system instructions.
"""

        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.2,
            max_output_tokens=512,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        )

    def ask(self, prompt, context=None):
        """
        Send a focused prompt to Gemini and return its response.
        """

        if not prompt or not prompt.strip():
            return "Please enter a command."

        if context:
            contents = (
                f"Additional context:\n{context.strip()}\n\n"
                f"Latest user request:\n{prompt.strip()}"
            )
        else:
            contents = prompt.strip()

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=self.config,
        )

        if not response or not response.text:
            return "I received an empty response from my AI system."

        return response.text.strip()


ai_engine = AIEngine()