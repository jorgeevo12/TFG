import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_0_chatbot_generated" / "data" / "nlu.yml"
DOMAIN_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_0_chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_0_chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_0_chatbot_generated" / "data" / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer contenido actual ---
nlu_content = NLU_FILE.read_text(encoding="utf-8")
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Prompt mejorado ---
prompt = f"""
You are a RASA 3.1 assistant fixer.

You will receive four YAML files with possible formatting issues or invalid structures.
Your task is to correct and reformat them to be valid, clean, and executable for RASA 3.1.

---

📄 REQUIRED STRUCTURE:

1. nlu.yml
- Must include:
  version: "3.1"
  nlu:
    - intent: intent_name
      examples: |
        - phrase 1
        - phrase 2
- Do NOT include slots, entities, or markdown formatting.

2. domain.yml
- Must include:
  version: "3.1"
  intents: [list]
  entities: [list]
  slots:
    slot_name:
      type: text
      mappings:
        - type: from_entity
          entity: slot_name
  responses:
    utter_name:
      - text: "Example 1"
      - text: "Example 2"
  actions:
    - utter_name

3. stories.yml
- Must include:
  version: "3.1"
  stories:
    - story: name
      steps:
        - intent: intent_name
        - action: utter_name
        - slot_was_set:
            - slot_name: value (if applicable)
- Do NOT include `utterance:` or `slots: {{}}`

4. rules.yml
- Must include:
  version: "3.1"
  rules:
    - rule: name
      steps:
        - intent: intent_name
        - action: utter_name

---

‼️ RULES:
- Do not return markdown, triple backticks or explanations.
- Only return valid YAML, strictly following the RASA 3.1 structure.
- All utter_* must include at least two text variants.

---

# nlu.yml
{nlu_content}

# domain.yml
{domain_content}

# stories.yml
{stories_content}

# rules.yml
{rules_content}

Now return the corrected files:
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
