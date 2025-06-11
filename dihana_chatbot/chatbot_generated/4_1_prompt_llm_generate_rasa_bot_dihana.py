import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DIALOGUE_ACTS_FILE = BASE_DIR / "dihana_chatbot" / "results" / "correct_deepseek_results_with_act_dialogue.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer el contenido completo del archivo JSON como texto ---
raw_content = DIALOGUE_ACTS_FILE.read_text(encoding="utf-8")

# --- Construir el prompt ---
prompt = f"""
You are a RASA chatbot builder.

You will receive dialogue acts extracted from real user-system dialogues, about train-related interactions (reservations, schedules, times, destinations, confirmations, prices, etc.).

Each dialogue act follows the format: `{{speaker}}_{{dialogue_act}}_{{slot}}`
  - speaker: user or system
  - dialogue_act: one of [inform, answer, confirm, disconfirm, question, request, suggest]
  - slot: what the act refers to (e.g., date, time, origin, price, etc.)

Your goal is to create a **fully functional RASA chatbot** by generating these files:

---

📁 `nlu.yml`
- List all user intents using this format:
nlu:
- intent: intent_name
  examples: |
    - sentence with [entity](slot)
    - another sentence with [value](slot)

---

📁 `domain.yml`
- Must contain:
  - intents (from nlu)
  - entities (used in nlu)
  - slots (from entity annotations), using this format:
    slot_name:
      type: text
      mappings:
        - type: from_text
  - responses for every utter_*, with 2+ variants:
    responses:
      utter_example:
        - text: "First example"
        - text: "Another variant"
  - actions: include all utter_* responses

---

📁 `stories.yml`
- Format:
version: "3.1"
stories:
- story: story_name
  steps:
  - intent: intent_name
  - action: utter_response_name
- story: user_inform_date
  steps:
  - intent: user_question_date
  - slot_was_set:
   - date: 15th April
  - action: utter_confirm_date

- One user → one system turn per story, following the dialogue act order.

---

📁 `rules.yml`
- Format:
version: "3.1"
rules:
- rule: respond to user intent
  steps:
  - intent: intent_name
  - action: utter_response_name

---

‼️ INSTRUCTIONS:
- Generate 10 diverse training phrases per intent
- Use realistic slot values (e.g., [Madrid](origin), [8 AM](time), [40](price)€)
- Include entities in nlu.yml, slots in rules.yml and stories.yml and in domain.yml when data are being provided or handled, for example in the question, inform xxx dialogue acts
- Slot values must match the slot name used in domain
- No explanations, no markdown, only valid YAML
- Use the exact dialogue act order to guide conversation flow

---

DIALOGUE ACTS (JSON input):
{raw_content}

Now build the assistant:
# nlu.yml
[...]

# domain.yml
[...]

# stories.yml
[...]

# rules.yml
[...]
"""

# --- Llamar al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Mostrar resultado ---
if response.status_code == 200:
    result = response.json().get("response", "")
    print(result)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
