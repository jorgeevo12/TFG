import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "nlu.yml"
DOMAIN_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivos existentes ---
nlu_content = NLU_FILE.read_text(encoding="utf-8")
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Prompt mejorado ---
prompt = f"""
You are a RASA 3.1 assistant builder.

You are given the four YAML files generated from a train-travel assistant. They include:
- `nlu.yml`: user intents with examples
- `domain.yml`: assistant configuration
- `stories.yml`: dialogue flows
- `rules.yml`: conversation rules

Your task is to FIX and STRUCTURE the assistant so it works in a fully guided slot-filling dialogue using a form.

---

🎯 OBJECTIVE:
- The assistant must:
  1. Start when the user expresses intent to plan a trip.
  2. Ask for and collect the following slots: date, time, origin, destination, price.
  3. Once all slots are filled, confirm all details.
  4. End the conversation.

---

📌 FILE INSTRUCTIONS:

- `nlu.yml`:
  - Separate entity mentions into individual intents (one slot per intent).
  - Use this format:
      - intent: inform_date
        examples: |
          - I want to travel on [15th April](date)
          - On [20th May](date)
  - Keep at least 5 examples per intent.

- `domain.yml`:
  - Include all intents, entities, slots, forms, responses and actions.
  - Define a `trip_form` with required slots: date, time, origin, destination, price.
  - For each slot, use:
        slot_name:
          type: text
          mappings:
            - type: from_entity
              entity: slot_name
  - Add `utter_ask_slot` responses for all slots.
  - Add `utter_confirm_all` with at least 2 variants.

- `stories.yml`:
  - Use a single form-based dialogue flow like this:
      - intent: request_trip
      - action: trip_form
      - active_loop: trip_form
      - intent: inform_date
        entities: ...
      - slot_was_set: ...
      - ...
      - active_loop: null
      - action: utter_confirm_all

- `rules.yml`:
  - Define:
      - A rule that activates the form when intent `request_trip` is triggered.
      - A rule that submits the form and triggers `utter_confirm_all`.

---

‼️ OUTPUT:
- Only return valid YAML (no markdown).
- Output all 4 fixed files in this order:
  - nlu.yml
  - domain.yml
  - stories.yml
  - rules.yml

Here are the original files:

# nlu.yml
{nlu_content}

# domain.yml
{domain_content}

# stories.yml
{stories_content}

# rules.yml
{rules_content}

Now return:
# nlu.yml
[...]

# domain.yml
[...]

# stories.yml
[...]

# rules.yml
[...]
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("❌ Error:", response.status_code)
    print(response.text)
