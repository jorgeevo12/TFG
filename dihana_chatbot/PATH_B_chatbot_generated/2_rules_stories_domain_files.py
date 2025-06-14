import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DIALOGUE_ACTS_FILE = BASE_DIR / "dihana_chatbot" / "results" / "correct_deepseek_results_with_act_dialogue.json"
NLU_FILE = BASE_DIR / "dihana_chatbot" / "PATH_B_chatbot_generated" / "data" / "nlu.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivos de entrada ---
nlu_content = NLU_FILE.read_text(encoding="utf-8")
raw_content = DIALOGUE_ACTS_FILE.read_text(encoding="utf-8")

# --- Prompt para generar domain, stories y rules ---
prompt = f"""
You are a RASA 3.1 assistant builder.

You will receive:
- A valid `nlu.yml` file already generated
- A list of user/system dialogue acts extracted from real Spanish train-related conversations

Your task is to complete the assistant by generating:
`domain.yml`
`stories.yml`
`rules.yml`

--- CONTEXT ---

The slot names used are the same as the entity names from `nlu.yml`.
Each utter_* in domain must match the responses that a system would give to the associated user intent.

--- FORMAT ---

domain.yml:
- version: "3.1"
- intents: from `nlu.yml`
- entities: from `nlu.yml` annotations
- slots:
    slot_name:
      type: text
      mappings:
        - type: from_entity
          entity: slot_name
- responses: include utter_* with 2 variants each
- actions: list all utter_* responses

stories.yml:
version: "3.1"
stories:
- story: intent_name flow
  steps:
    - intent: inform_date
    - slot_was_set:
        - date: "10th July"
    - action: utter_confirm_date

rules.yml:
version: "3.1"
rules:
- rule: respond to user intent
  steps:
    - intent: intent_name
    - action: utter_response_name

--- INSTRUCTIONS ---

- Use only valid YAML (no markdown, no explanations)
- Do not regenerate nlu.yml — it is already defined
- Align intents and entities with those found in the provided nlu.yml
- Slot names = entity names
- Ensure domain, rules, stories align with the dialogue act sequence
- Each user act → system response should appear as a story
- Include slot_was_set when a value is informed

---

# nlu.yml
{nlu_content}

# dialogue_acts.json
{raw_content}

Now return:
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
    print("Error:", response.status_code)
    print(response.text)
