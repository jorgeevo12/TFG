import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "dihana_chatbot" / "PATH_0_chatbot_generated" / "data" / "nlu.yml"
DOMAIN_FILE = BASE_DIR / "dihana_chatbot" / "PATH_0_chatbot_generated" / "domain.yml"
STORIES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_0_chatbot_generated" / "data" / "stories.yml"
RULES_FILE = BASE_DIR / "dihana_chatbot" / "PATH_0_chatbot_generated" / "data" / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivos originales ---
nlu_content = NLU_FILE.read_text(encoding="utf-8")
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Prompt específico para arreglar PATH_0 ---
prompt = f"""
You are a RASA 3.1 assistant fixer.

You will receive 4 YAML files generated from raw dialogue data. These files contain formatting issues, outdated RASA structures, or misplaced content. Your job is to FIX and normalize these files for use in a production-ready RASA 3.1 assistant.

---

🎯 TASKS (fix all of these):

1. nlu.yml:
- Use header: `version: "3.1"`
- Under `nlu:`, list each `- intent: name` with `examples: |`
- Move training examples from domain.yml into nlu.yml
- Use entity annotation like: [value](entity)
- Add at least 4 examples per intent

2. domain.yml:
- Use header: `version: "3.1"`
- Structure:
  intents:
    - intent_name
  entities:
    - entity_name
  slots:
    slot_name:
      type: text
      mappings:
        - type: from_entity
          entity: slot_name
  responses:
    utter_*:
      - text: "..."
  actions:
    - utter_*

3. stories.yml:
- Use header: `version: "3.1"`
- Each story:
  - intent: intent_name
  - action: utter_*
  - slot_was_set:
      - slot_name: value

4. rules.yml:
- Use header: `version: "3.1"`
- Use `steps:` instead of `condition:` or `action:` directly
- Format:
  - rule: rule_name
    steps:
      - intent: intent_name
      - action: utter_*

---

‼️ INSTRUCTIONS:
- Do NOT include markdown (no triple backticks).
- Return ONLY fixed valid YAML.
- Order: nlu.yml, domain.yml, stories.yml, rules.yml

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
