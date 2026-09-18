import json
import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import memory
from core.commands import process_command
from core.context import resolve_command
from core.intent import detect_intent


class CoreBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"
        self.memory_file.write_text(
            json.dumps({"user": {}, "history": []}),
            encoding="utf-8",
        )
        self.memory_file_patch = patch.object(
            memory,
            "MEMORY_FILE",
            str(self.memory_file),
        )
        self.memory_file_patch.start()
        self.addCleanup(self.memory_file_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_intent_detection_covers_core_commands(self):
        self.assertEqual(detect_intent("hey stark"), "greeting")
        self.assertEqual(detect_intent("what time is it"), "time")
        self.assertEqual(
            detect_intent("please remember my favorite color is black"),
            "remember",
        )
        self.assertEqual(detect_intent("recall"), "recall")
        self.assertEqual(detect_intent("goodbye"), "exit")

    def test_natural_language_memory_command_saves_and_recalls(self):
        self.assertEqual(
            process_command("please remember that my favorite color is black"),
            "I'll remember that, Atharva.",
        )
        self.assertEqual(
            process_command("what is my favorite color"),
            "Your favorite color is black.",
        )

    def test_recall_returns_all_saved_memories(self):
        memory.remember("favorite language", "Python")
        memory.remember("favorite color", "black")

        response = process_command("recall")

        self.assertIn("favorite language: Python", response)
        self.assertIn("favorite color: black", response)

    def test_malformed_memory_file_recovers_as_empty_memory(self):
        self.memory_file.write_text("not valid json", encoding="utf-8")

        self.assertEqual(memory.load_memory(), {"user": {}, "history": []})

    def test_context_resolves_follow_up_reference(self):
        memory.add_history("What is Python?", "Python is a programming language.")

        self.assertEqual(
            resolve_command("Who created it?"),
            "who created python",
        )

    def test_ai_engine_rejects_missing_api_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            ai_module = importlib.import_module("ai.engine")

        with patch.object(ai_module.os, "getenv", return_value=None):
            with self.assertRaisesRegex(
                RuntimeError,
                "GEMINI_API_KEY is not set",
            ):
                ai_module.AIEngine()

    def test_brain_returns_fallback_when_ai_provider_fails(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            brain_module = importlib.import_module("core.brain")

        with patch.object(
            brain_module.ai_engine,
            "ask",
            side_effect=RuntimeError("provider unavailable"),
        ):
            response = brain_module.think("Explain quantum computing")

        self.assertEqual(
            response,
            "I'm having trouble connecting to my AI system right now.",
        )


if __name__ == "__main__":
    unittest.main()