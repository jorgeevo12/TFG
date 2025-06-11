import json
from pathlib import Path
import requests

# --- Configuración de rutas y modelo ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "processed_dialogues.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Cargar los diálogos ---
with INPUT_FILE.open(encoding="utf-8") as f:
    all_dialogues = json.load(f)

sample_dialogues = all_dialogues[4:8]

# --- Construir el prompt ---
formatted_dialogs = []
for dialog in sample_dialogues:
    formatted_turns = [f'{turn["speaker"].lower()}: {turn["utterance"]}' for turn in dialog["turns"]]
    formatted_dialogs.append(f"# Dialogue ID: {dialog['dialogue_id']}\n" + "\n".join(formatted_turns))

prompt = f"""
You are a dialogue act annotator based on the ISO 24617-2 standard.

You will be given a list of dialogues in English between a USER and a SYSTEM. Each turn is a message that performs a specific communicative function.

Your task is:
- For **each turn** in each dialogue, predict the ISO-style dialogue act.
- Use the format: {{domain}}_{{speaker}}_{{dialogue_act}}, where:
    • domain: the domain the turn belongs to (restaurant, hotel, taxi, train, etc.)
    • speaker: "user" or "system"
    • dialogue_act: one of [inform, answer, confirm, disconfirm, question, request, suggest]
    • slot: the main concept the utterance refers to (e.g., price, area, stars, time, food, destination, none, etc.)
You must return a list of annotated dialogues like this:

[
  {{
    "dialogue_id": "...",
    "turns": [
      {{
        "speaker": "...",
        "utterance": "...",
        "act": "domain_speaker_dialogueact_slot"
      }},
      ...
    ]
  }},
  ...
]

Now annotate the following 4 dialogues:

{chr(10).join(formatted_dialogs)}
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Mostrar resultado ---
if response.status_code == 200:
    result = response.json().get("response", "")
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ No se pudo interpretar la respuesta como JSON. Resultado en bruto:\n")
        print(result)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
