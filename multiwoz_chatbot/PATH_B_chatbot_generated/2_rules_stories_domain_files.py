import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_B_chatbot_generated" / "data" / "nlu.yml"
DIALOGUE_ACTS_FILE = BASE_DIR / "multiwoz_chatbot" / "results" / "deepseek_results.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivos de entrada ---
with NLU_FILE.open(encoding="utf-8") as f:
    nlu_content = f.read()

with DIALOGUE_ACTS_FILE.open(encoding="utf-8") as f:
    all_dialogues = json.load(f)

# Limpiar los turnos (dejar solo los actos)
for dialogue in all_dialogues:
    for turn in dialogue["turns"]:
        turn.pop("utterance", None)
        turn.pop("speaker", None)

raw_content = json.dumps(all_dialogues, indent=2)

# --- Construir el prompt ---
prompt = f"""
You are a RASA 3.1 assistant builder.

You will receive:
- A valid `nlu.yml` file with intents and entity annotations.
- A list of user/system dialogue acts extracted from MultiWOZ dialogues.

Your task is to generate:
✅ domain.yml
✅ stories.yml
✅ rules.yml

---

🧠 CONTEXT:

Each intent in `nlu.yml` represents a user goal (e.g., restaurant_food, hotel_rooms, taxi_phone).
Each entity represents a slot that needs to be captured.

Dialogue acts are structured in format:
  domain_speaker_act_slot (e.g., hotel_user_request_area)

You MUST:
- Include ALL intents found in `nlu.yml → intents` inside `domain.yml → intents`.
- Include ALL entities used in `nlu.yml` examples inside `domain.yml → entities` and `slots`.

---

📁 domain.yml:
```yaml
version: "3.1"
intents:
  - restaurant_food
  - hotel_rooms
  ...
entities:
  - food
  - area
  ...
slots:
  food:
    type: text
    mappings:
      - type: from_entity
        entity: food
  area:
    type: text
    mappings:
      - type: from_entity
        entity: area
responses:
  utter_restaurant_food:
    - text: "What kind of food are you looking for?"
    - text: "Any preferred cuisine?"
actions:
  - utter_restaurant_food

📁 stories.yml:

version: "3.1"
stories:
- story: user_asks_about_restaurant_food
  steps:
    - intent: restaurant_food
    - slot_was_set:
        - food: "Italian"
    - action: utter_restaurant_food

📁 rules.yml:

version: "3.1"
rules:
- rule: handle restaurant food intent
  steps:
    - intent: restaurant_food
    - action: utter_restaurant_food

‼️ INSTRUCTIONS:

Return only valid YAML (no markdown, no explanations).

DO NOT regenerate nlu.yml.

Slot names = entity names = nlu annotation keys.

Each intent must:

Appear in domain.yml intents

Have a matching utter_* response

Be used in at least 1 story and 1 rule

Dialogue acts should guide example stories logically.

Responses should be natural and helpful.

nlu.yml
{nlu_content}

dialogue_acts.json
{raw_content}

Now return:

domain.yml
[...]

stories.yml
[...]

rules.yml
[...]
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
