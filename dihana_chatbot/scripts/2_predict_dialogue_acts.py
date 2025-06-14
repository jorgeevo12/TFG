import json
from pathlib import Path
import requests

# --- Configuración de rutas y modelo ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "dihana_chatbot" / "results" / "formatted_dialogues.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Cargar las conversaciones ---
with INPUT_FILE.open(encoding="utf-8") as f:
    all_dialogues = json.load(f)

sample_dialogues = all_dialogues[:4]


prompt = f"""
You are a dialogue act annotator based on the ISO 24617-2 standard.

You will be given a list of conversations in Spanish about train-related interactions, formatted as JSON. Each conversation includes a list of turns between "user" and "system".

Your task is to return the **same JSON structure**, but with an additional field "act" in each turn. This field should follow the format:

  "act": "speaker_dialogueact_slot"

Where:
- speaker: "user" or "system"
- dialogueact: one of [inform, answer, confirm, disconfirm, question, request, suggest]
- slot: the main concept (only one word) discussed (like time, destination, location, etc.) or "none" if it's unclear

Respond ONLY with valid JSON. Do not include explanations or extra text. Do not forget the tag slot.

Here is the data to annotate:

{json.dumps(sample_dialogues, indent=2, ensure_ascii=False)}
"""



# --- Enviar prompt al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1200
)

# --- Imprimir la respuesta ---
if response.status_code == 200:
    result = response.json()["response"]
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("No se pudo interpretar la respuesta como JSON. Output bruto:\n")
        print(result)
else:
    print("Error:", response.status_code)
    print(response.text)