import ollama


class LocalAIEngine:
    def __init__(self):
        self.model = "qwen2.5-coder:14b"

        self.system_instruction = """
You are STARK, Atharva's local AI assistant.
You are part of the STARK-OS personal AI workstation project.

Give practical, structured, useful answers.
Help with advanced technical questions and STARK-OS development.
Never claim to have modified files or controlled the computer unless a tool
actually performed that action.
"""

    def ask(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            return "Please enter a command."

        print("[LOCAL AI] Connecting to Ollama...", flush=True)
        print(f"[LOCAL AI] Loading model: {self.model}", flush=True)

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_instruction,
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                },
            ],
        )

        print("[LOCAL AI] Response received.", flush=True)

        answer = response.get("message", {}).get("content", "").strip()

        if not answer:
            return "The local AI returned an empty response."

        return answer


local_ai_engine = LocalAIEngine()
