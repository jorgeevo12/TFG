import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "dihana" / "dihana_dialogues" / "processed_dialogues.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Cargar diálogos y seleccionar una muestra representativa ---
dialogues = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
sample_dialogues = dialogues[:8]

# --- Formatear los diálogos para el prompt ---
formatted_dialogs = []
for d in sample_dialogues:
    lines = [f'{turn["speaker"]}: {turn["text"]}' for turn in d["turns"]]
    formatted_dialogs.append(f"# Dialogue ID: {d['dialogue_id']}\n" + "\n".join(lines))

# --- Prompt robusto y claro ---
prompt = f"""
You are a RASA 3.1 assistant builder.

You will receive a list of Spanish conversations between a USER and a SYSTEM. These are unstructured natural dialogues (without annotation), focused on train-related tasks like timetables, destinations, prices, confirmations, etc.

---

Your task:
Build a functional RASA 3.1 assistant based on these dialogues. You must infer:
- intents (from USER utterances)
- entities (relevant slot values)
- slots (based on extracted entities)
- system responses (utter_*)
- stories (based on turn order)
- rules (intent-to-action pairs)

---

You must generate 4 valid YAML files:

nlu.yml
version: "3.1"
nlu:
  - intent: intent_name
    examples: |
      - sentence with [value](entity)
      - another example with [city](origin)

domain.yml
version: "3.1"
intents:
  - ...
entities:
  - ...
slots:
  slot_name:
    type: text
    mappings:
      - type: from_entity
        entity: slot_name
responses:
  utter_action_name:
    - text: "First variant"
    - text: "Second variant"
actions:
  - utter_action_name

stories.yml
version: "3.1"
stories:
  - story: short_description
    steps:
      - intent: intent_name
      - action: utter_action
      - slot_was_set:
          - slot: value

rules.yml
version: "3.1"
rules:
  - rule: respond to intent
    steps:
      - intent: intent_name
      - action: utter_action

---

INSTRUCTIONS:
- Use only valid YAML syntax (no markdown, no explanations).
- Use realistic slot values (e.g., [Madrid](origin), [8 AM](time), [40](price)€).
- 1 intent ↔ 1 slot when possible.
- Every utter_* response must have 2+ variations.
- Each story must follow the original turn order (user → system → user...).

---

Dialogues:
{chr(10).join(formatted_dialogs)}
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

if response.status_code == 200:
    result = response.json().get("response", "")
    print(result)
else:
    print("Error:", response.status_code)
    print(response.text)
