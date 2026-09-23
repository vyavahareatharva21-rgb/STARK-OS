import os

from dotenv import load_dotenv

from ai.providers.gemini import GeminiProvider


load_dotenv()


class AIEngine:
    """
    STARK-OS AI Engine.

    Provides a stable interface between STARK and the selected AI provider.
    """

    def __init__(self):
        self.provider = GeminiProvider()
        self.provider_name = self.provider.provider
        self.model = self.provider.model

    def ask(self, prompt, context=None):
        """
        Send a focused prompt through the configured AI provider.
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

        return self.provider.ask(contents)


ai_engine = AIEngine()
