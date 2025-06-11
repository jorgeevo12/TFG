import requests
from pathlib import Path

# --- Configuración de rutas ---
BASE_DIR = Path(__file__).resolve().parents[2]
CHATBOT_DIR = BASE_DIR / "dihana_chatbot" / "chatbot_generated"
DATA_DIR = CHATBOT_DIR / "data"

DOMAIN_FILE = CHATBOT_DIR / "domain.yml"
NLU_FILE = DATA_DIR / "nlu.yml"
STORIES_FILE = DATA_DIR / "stories.yml"
RULES_FILE = DATA_DIR / "rules.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer los contenidos YAML como texto ---
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")
nlu_content = NLU_FILE.read_text(encoding="utf-8")
stories_content = STORIES_FILE.read_text(encoding="utf-8")
rules_content = RULES_FILE.read_text(encoding="utf-8")

# --- Construir el prompt ---
prompt = f"""
You are a RASA chatbot expert.

You will be given four YAML files that define a task-oriented assistant for train-related interactions (e.g., schedules, destinations, prices, preferences, etc.).

Your task is to **improve the assistant**, keeping the structure of each file intact. Specifically:

- Add more user examples to each intent in `nlu.yml` (at least 10 diverse examples per intent)
- Make responses in `domain.yml` more varied and realistic (2+ variants per `utter_*`)
- Improve and expand `stories.yml` and `rules.yml` to reflect plausible and natural conversation flows
- Keep all YAML syntax valid
- DO NOT change file structure
- Use realistic slot values and reuse slot names (e.g. `[Madrid](origin)`, `[7 AM](time)`, `[50](price)€`)
- DO NOT explain your changes — only output the improved YAML content for each file

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

# --- Enviar al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Mostrar el resultado en pantalla ---
if response.status_code == 200:
    result = response.json().get("response", "")
    print(result)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
