import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "processed_dialogues.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer y seleccionar los primeros 10 diálogos ---
dialogues = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
sample_dialogues = dialogues

# --- Formatear los diálogos correctamente ---
formatted_dialogs = []
for dialog in sample_dialogues:
    formatted_turns = [f'{turn["speaker"].lower()}: {turn["utterance"]}' for turn in dialog["turns"]]
    formatted_dialogs.append(f"# Dialogue ID: {dialog['dialogue_id']}\n" + "\n".join(formatted_turns))

# --- Construir el prompt para el LLM ---
prompt = f"""
You are a RASA assistant builder.

You will receive a set of English dialogue examples between a USER and a SYSTEM. Your goal is to build a fully functional RASA chatbot from these unstructured conversations.

---

🗂️ DIALOGUE DATA:
- Each conversation is a sequence of turns in format:
  - `user:` or `system:` followed by text
- Dialogues cover multiple domains such as restaurant, hotel, train, taxi, etc.
- Topics include reservations, bookings, confirmations, schedule queries, etc.

---

📁 OUTPUT FILES TO GENERATE (structured as separate YAML blocks):

1. `nlu.yml`:
   - Define all user intents with realistic examples (at least 5 per intent).
   - Use entity annotation: e.g. [italian](food), [cambridge](location), [01234 567890](phone)
   - Do NOT include system utterances or actions here.
   - Structure:
     version: "3.1"
     nlu:
       - intent: intent_name
         examples: |
           - example 1
           - example 2
           ...

2. `domain.yml`:
   - Must include:
     version: "3.1"
     intents: list of all intent names (no examples here)
     entities: names of entities used in the examples
     slots: one per entity, each using:
       slot_name:
         type: text
         mappings:
           - type: from_entity
             entity: slot_name
     responses: define `utter_*` responses used by the system (2+ variations each)
     actions: only include the utter_* names used in `responses`

3. `stories.yml`:
   - version: "3.1"
   - Add one story per dialogue
   - Follow this format:
     - intent: intent_name
     - action: utter_response_name
     - (repeat as needed)
   - Preserve turn order between user and system.

4. `rules.yml`:
   - version: "3.1"
   - Add simple rules to map user intent to system utterance:
     - rule: short description
       steps:
         - intent: intent_name
         - action: utter_response_name

---

‼️ INSTRUCTIONS:
- Use only valid YAML per file — no markdown, no explanations, no multi-file merging.
- Group each file under a clear header (e.g. `# nlu.yml`) before its content.
- All content must follow RASA 3.1 syntax and conventions.
- Only use `utter_*` actions (do not generate `action_*` unless absolutely necessary).
- Ensure all entities and slots are consistently defined across files.
- Use clear and meaningful intent names (e.g. `inform_location`, `request_restaurant`, `confirm_booking`)

---

DIALOGUES (raw user/system conversations):
{chr(10).join(formatted_dialogs)}
"""

# --- Enviar a Ollama ---
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
