import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "dihana_chatbot" / "results" / "formatted_dialogues.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Cargar diálogos originales ---
with INPUT_FILE.open(encoding="utf-8") as f:
    raw_dialogues = json.load(f)

# --- Reunir los enunciados del usuario ---
user_utterances = []
for dialogue in raw_dialogues:
    for turn in dialogue["turns"]:
        if "USER" in turn:
            user_utterances.append(turn["USER"])

# --- Formatear para el prompt ---
examples = "\n".join([f"- {utt}" for utt in user_utterances])

# --- Prompt ---
prompt = f"""
You are a RASA 3.1 assistant expert.

You will receive a list of user utterances written in **Spanish**, each from a dialogue related to train travel (e.g., booking, times, locations, prices).

Your task is to create a complete RASA **nlu.yml** training file:
- Each utterance must be converted to English.
- For each utterance, infer:
  - a user **intent** name (e.g., inform_date, request_schedule, inform_origin).
  - any relevant **entities** mentioned (e.g., [Salamanca](destination), [10th July](date)).
- Group similar utterances under the same intent and annotate entities using the `[value](entity)` format.

---

📄 Output format:
nlu:
  - intent: intent_name
    examples: |
      - phrase with [entity](slot)
      - another training example...

‼️ INSTRUCTIONS:
- Output only valid YAML.
- Return only NLU format (no markdown, no explanations).
- Utterances must be in **English**, even if input is Spanish.
- Include at least 5 diverse examples per intent.
- Each intent must include realistic entity annotations.

---

Here are user utterances:
{examples}

Now return:
# nlu.yml
"""

# --- Petición al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Mostrar resultado ---
if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("❌ Error:", response.status_code)
    print(response.text)
