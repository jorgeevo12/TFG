import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "dihana_chatbot" / "chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "dihana_chatbot" / "chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "dihana_chatbot" / "chatbot_generated" / "data" / "rules.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

prompt = f"""
You are a RASA 3.1 assistant builder.

The assistant has a form called `trip_form` in domain.yml that collects 5 required slots: date, time, origin, destination, and price.

Your task is to update ONLY the `rules.yml` and `stories.yml` so that the **system asks for each slot**, and the **user provides values in response**.

---

RULES.YML:
- Add a rule to activate the form:
  - intent: request_trip
  - action: trip_form
  - active_loop: trip_form

- Add a rule for form submission:
  - action: trip_form
  - active_loop: null
  - action: utter_confirm_all

- These rules should use correct Rasa 3.1 structure: `action`, `active_loop`, `intent`, and so on.

---

STORIES.YML:
- Add 2 stories showing the system asking and the user providing each slot.
- Format:
  - intent: request_trip
  - action: trip_form
  - active_loop: trip_form
  - intent: inform_date
    entities:
      - date: "2024-06-01"
  - slot_was_set:
      - date: "2024-06-01"
  - intent: inform_time
    entities:
      - time: "10:00"
  - slot_was_set:
      - time: "10:00"
  ...
  - active_loop: null
  - action: utter_confirm_all

---

INSTRUCTIONS:
- Do NOT modify domain.yml or nlu.yml.
- Only return valid YAML.
- Do not include markdown or comments.
- The system always asks each slot using `utter_ask_*`, and user responds using `inform_*`.
- Ensure all slots are collected before `utter_confirm_all`.

---

# domain.yml (for reference)
{domain_content}

# Existing rules.yml
{rules_content}

# Existing stories.yml
{stories_content}

Now output the updated:

# rules.yml
[...]

# stories.yml
[...]
"""

response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("Error:", response.status_code)
    print(response.text)
