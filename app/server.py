from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.brain import think
from core.intent import detect_intent
from core.memory import add_history
from ui.status import get_system_status


app = FastAPI(title="STARK-OS")


WEB_DIR = Path(__file__).resolve().parent.parent / "ui" / "web"


app.mount(
    "/ui/web",
    StaticFiles(directory=WEB_DIR),
    name="web",
)


@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/status")
def system_status():
    return get_system_status()


@app.post("/api/chat")
def chat(payload: dict):
    command = payload.get("message", "").strip()

    if not command:
        return {
            "response": "Please enter a command.",
            "intent": "empty",
        }

    intent = detect_intent(command)

    response = think(command)

    if response != "EXIT":
        add_history(command, response)

    return {
        "response": response,
        "intent": intent,
    }