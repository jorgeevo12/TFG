import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_B_chatbot_generated" / "domain.yml"
RULES_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_B_chatbot_generated" / "data" / "rules.yml"
STORIES_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_B_chatbot_generated" / "data" / "stories.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivos ---
def read(file_path):
    with file_path.open(encoding="utf-8") as f:
        return f.read()

domain_content = read(DOMAIN_FILE)
rules_content = read(RULES_FILE)
stories_content = read(STORIES_FILE)

# --- Construir prompt ---
prompt = f"""
You are a RASA 3.1 assistant builder.

The assistant has multiple forms defined in domain.yml:
- restaurant_form
- hotel_form
- train_form
- taxi_form
- attraction_form

Each form collects specific required slots listed in domain.yml.

Your task is to update ONLY the `rules.yml` and `stories.yml` so that:
- Each form is activated by a matching intent (e.g., request_restaurant)
- The assistant enters the form, asks the user for each slot via utter_ask_*, and fills them
- The form ends with a confirmation utterance: `utter_confirm_all_<domain>`

---

RULES.YML:
For each form:
- Add a rule to activate the form:
    - intent: request_<domain>
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
- Start with the triggering intent (e.g., request_hotel)
- Activate the form
- Simulate the user filling each required slot:
    - intent: inform_<slot>
    - entities: with realistic example values
    - slot_was_set: with same value
- End with form deactivation and final utterance

Format example:
- intent: request_restaurant
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
- Return only valid YAML for `rules.yml` and `stories.yml`.
- No markdown, no comments, no extra text.
- Use realistic slot values (e.g., "Chinese", "city center", "0123456789").
- Match confirmation utterance to the form (e.g., `utter_confirm_all_attraction`).

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

# --- Mostrar salida ---
if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("Error:", response.status_code)
    print(response.text)
