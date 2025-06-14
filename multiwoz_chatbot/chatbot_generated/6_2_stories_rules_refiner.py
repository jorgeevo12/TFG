import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated" / "data" / "rules.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Lectura de archivos ---
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Prompt adaptado a multi-form ---
prompt = f"""
You are a RASA 3.1 assistant builder.

The assistant has multiple forms defined in domain.yml:
- restaurant_form
- hotel_form
- train_form
- taxi_form

Each form collects specific required slots listed in domain.yml.

Your task is to update ONLY the `rules.yml` and `stories.yml` so that:
- Each form is activated by a matching intent
- The system enters the form, fills each slot via user input
- The form ends with a domain-specific confirmation utterance

---

RULES.YML:
For each form:
- Add a rule to activate the form:
    - intent: <domain_request_intent>
    - action: <form_name>
    - active_loop: <form_name>

- Add a rule for form submission:
    - action: <form_name>
    - active_loop: null
    - action: utter_confirm_all_<domain>

Use valid Rasa 3.1 syntax: `action`, `active_loop`, `intent`.

---

STORIES.YML:
For each form, write 1 story:
- Start with triggering intent
- Activate the form
- Use `inform_*` and `slot_was_set` for each required slot
- End with `active_loop: null` and confirmation utterance

Format:
- intent: restaurant_request_price
- action: restaurant_form
- active_loop: restaurant_form
- intent: inform_food
  entities:
    - food: "Chinese"
- slot_was_set:
    - food: "Chinese"
...
- active_loop: null
- action: utter_confirm_all_restaurant

---

INSTRUCTIONS:
- Do NOT modify domain.yml or nlu.yml.
- Return only valid YAML.
- No markdown, no comments.
- Use realistic slot values (e.g., "Chinese", "city center", "0123456789").
- Match confirmation utterance to form (e.g., `utter_confirm_all_train`).

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


# --- Llamada al modelo ---
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
