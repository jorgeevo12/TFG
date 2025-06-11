import requests
from pathlib import Path

# --- Configuración de rutas ---
BASE_DIR = Path(__file__).resolve().parents[2]
CHATBOT_DIR = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated"
DATA_DIR = CHATBOT_DIR / "data"

NLU_FILE = DATA_DIR / "nlu.yml"
DOMAIN_FILE = CHATBOT_DIR / "domain.yml"
STORIES_FILE = DATA_DIR / "stories.yml"
RULES_FILE = DATA_DIR / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer contenidos de los ficheros ---
nlu_content = NLU_FILE.read_text(encoding="utf-8")
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Construir el prompt ---
prompt = f"""
You are a RASA chatbot expert.

You will be given four YAML files that define a task-oriented assistant for MultiWOZ-style dialogues, which span multiple domains (e.g., restaurant, hotel, taxi, train, attraction).

Your task is to **improve the assistant**, keeping the structure of each file intact. Specifically:

- Expand `nlu.yml`:
  - Add more user examples to each intent (at least 10 diverse and realistic examples per intent)
  - Use slot annotation format: [value](entity)
  - Ensure slot names are consistent across files

- Improve `domain.yml`:
  - Add 2 or more response variants for each `utter_*` response
  - Keep intents, entities, slots and responses consistent
  - Use meaningful slot values (e.g., [cheap](price), [Italian](food), [north](area))

- Extend `stories.yml` and `rules.yml`:
  - Add new plausible interaction flows involving the domains and slots
  - Use real-world examples from MultiWOZ dialogue style
  - Preserve the format, indentation, and version syntax (Rasa 3.1)

- DO NOT alter the file structure
- DO NOT remove or rename existing slots, intents, or actions
- DO NOT explain anything — only output valid YAML

---

🗂️ Files to improve:

# domain.yml
{domain_content}

# nlu.yml
{nlu_content}

# stories.yml
{stories_content}

# rules.yml
{rules_content}

Now output the improved files below (starting from `nlu.yml`):
"""



# --- Enviar prompt al modelo ---
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
