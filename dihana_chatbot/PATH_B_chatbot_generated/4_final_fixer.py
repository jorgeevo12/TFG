import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer contenido actual ---
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Prompt para corrección estructural ---
prompt = f"""
You are a RASA 3.1 assistant builder and validator.

You are given YAML files (`domain.yml`, `rules.yml`, `stories.yml`) that define a partially structured form-based chatbot. These files may contain formatting issues, logical inconsistencies, or outdated syntax.

Your job is to fix and complete these files using valid RASA 3.1 format and logic.

---

🎯 OBJECTIVE:
Build a functional assistant using `trip_form` to gather 5 required pieces of travel information:

1. User starts with `request_trip` intent
2. The assistant activates `trip_form`
3. The assistant asks for and collects these slots:
   - `date`, `time`, `origin`, `destination`, `price`
4. After collecting all slots, the form ends and `utter_confirm_all` is triggered

---

🛠 FIX THESE STRUCTURE ISSUES:

- **domain.yml**
  - Ensure it includes:
    - All required `intents` (inform_date, inform_time, etc. + request_trip)
    - All `entities`: date, time, origin, destination, price
    - All `slots`, using:
        slot_name:
          type: text
          mappings:
            - type: from_entity
              entity: slot_name
    - `forms:` must define `trip_form` using:
        trip_form:
          required_slots:
            slot_name:
              - type: from_entity
                entity: slot_name
    - Add all required `responses` for `utter_ask_*` and `utter_confirm_all`
    - Add all those `utter_*` actions to `actions:`

- **rules.yml**
  - Replace any `condition:` blocks with valid `steps:` syntax
  - Keep only two rules:
    - rule: activate_trip_form_on_request
      steps:
        - intent: request_trip
        - action: trip_form
        - active_loop: trip_form

    - rule: submit_trip_form_and_confirm
      steps:
        - action: trip_form
        - active_loop: null
        - action: utter_confirm_all

- **stories.yml**
  - version: "3.1"
  - Include at least one full story:
    - Starts with: intent: request_trip
    - Shows: action: trip_form, active_loop: trip_form
    - One intent per slot (e.g., inform_date), with `slot_was_set` updates
    - Ends with: active_loop: null and `utter_confirm_all`

- ❌ Remove any steps like:
  - `action: ask_time`
  - `action: submit_trip_form`
  - `action: confirm_all`
  - `action_name: ...`

---

‼️ INSTRUCTIONS:
- Return only valid YAML (no markdown, no explanations).
- Output files must appear in this order:
  1. domain.yml
  2. rules.yml
  3. stories.yml

--- INPUT FILES ---

# domain.yml
{domain_content}

# rules.yml
{rules_content}

# stories.yml
{stories_content}

Now return:
# domain.yml
[...]

# rules.yml
[...]

# stories.yml
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
