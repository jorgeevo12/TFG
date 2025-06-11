import json
from pathlib import Path
import requests

# --- Configuración de rutas y modelo ---
BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_FILE = BASE_DIR / "multiwoz_chatbot" / "results" / "deepseek_results.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer los diálogos anotados ---
with RESULTS_FILE.open(encoding="utf-8") as f:
    all_dialogues = json.load(f)

# --- Extraer solo los "act" de cada turno ---
for dialogue in all_dialogues:
    for turn in dialogue["turns"]:
        turn.pop("utterance", None)  # Eliminar texto natural
        turn.pop("speaker", None)    # También eliminamos speaker redundante

# --- Construir el prompt ---
raw_content = json.dumps(all_dialogues, indent=2, ensure_ascii=False)

prompt = f"""
You are a RASA chatbot builder.

You will receive dialogue acts extracted from real user-system dialogues from the MultiWOZ dataset. These involve multi-domain interactions (e.g., restaurant bookings, hotel info, taxi requests, train inquiries, attractions, etc.).

Each dialogue act follows the format: {{domain}}_{{speaker}}_{{dialogue_act}}_{{slot}}
  - domain: the domain the turn belongs to (e.g., restaurant, hotel, train, taxi, attraction)
  - speaker: user or system
  - dialogue_act: one of [inform, answer, confirm, disconfirm, question, request, suggest]
  - slot: the main slot referred to (e.g., area, food, stars, time, destination, price, etc.). Use only one slot per intent in the nlu.yml (not per sentence)

Your goal is to create a **fully functional RASA chatbot** by generating these files:

---

📁 nlu.yml
- List all user intents using this format:
nlu:
- intent: domain_intent_name
  examples: |
    - sentence with [value](slot)
    - another sentence with [value](slot)

---

📁 domain.yml
- Must contain:
  - intents (from nlu)
  - entities (slots used in nlu)
  - slots (from entity annotations), using this format:
    slot_name:
      type: text
      mappings:
        - type: from_text
  - responses for every utter_*, with 2+ variants (one utter per intent):
    responses:
      domain_utter_example:
        - text: "First example"
        - text: "Another variant"
  - actions: include all utter_* responses

---

📁 stories.yml
- Format:
version: "3.1"
stories:
- story: story_name
  steps:
  - intent: domain_intent_name
  - action: domain_utter_response_name

- One user → one system turn per story, following the dialogue act order.

---

📁 rules.yml
- Format:
version: "3.1"
rules:
- rule: respond to user intent
  steps:
  - intent: domain_intent_name
  - action: domain_utter_response_name

---

‼️ INSTRUCTIONS:
- Generate 10 diverse training phrases per intent
- Use realistic slot values from MultiWOZ (e.g., [cheap](price), [north](area), [Chinese](food), [4 stars](stars))
- Include entities in `nlu.yml`, slots in `domain.yml`, and use them in `rules.yml` and `stories.yml`
- Slot names must match between intent examples, slot annotations, and domain slot definitions
- No explanations, no markdown, only valid YAML
- Use the exact dialogue act order to guide story flow

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

# --- Mostrar resultado por pantalla ---
if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("❌ Error:", response.status_code)
    print(response.text)
