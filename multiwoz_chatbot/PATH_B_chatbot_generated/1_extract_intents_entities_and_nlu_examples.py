import json
import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "multiwoz_chatbot" / "results" / "deepseek_results.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Cargar resultados ---
with INPUT_FILE.open(encoding="utf-8") as f:
    deepseek_data = json.load(f)

# --- Extraer frases de usuario ---
user_utterances = [entry["utterance"] for entry in deepseek_data if "utterance" in entry]

# --- Formatear para el prompt ---
examples = "\n".join([f"- {utt}" for utt in user_utterances])

# --- Prompt ---
prompt = f"""
You are a RASA 3.1 assistant expert.

You will receive a list of English user utterances from real MultiWOZ dialogues. These cover domains such as restaurant, hotel, train, taxi, and attraction.

Your task is to extract structured training data and generate:

1. `nlu.yml`: intents and training examples
2. `slots`: the list of extracted entity names (used in entity annotations)

---

OUTPUT FORMAT:

# nlu.yml
nlu:
  - intent: intent_name
    examples: |
      - example with one [value](entity)
      - another example with one [value](entity)
      - ...

# slots
- entity_name_1
- entity_name_2
- ...

---

INSTRUCTIONS:
- Extract the **maximum number of distinct intents and slots** from the utterances.
- Each intent must include **only one entity/slot type**.
- Each example must have exactly **one entity annotation**, using `[value](entity)` format.
- Group utterances with similar purpose and same slot into one intent.
- Do NOT include multiple slots per example or intent.
- Use realistic values from MultiWOZ (e.g., [north](area), [Italian](food), [cheap](price), [2](people), [01223 351707](phone))
- Do NOT include markdown, comments, or explanations.
- Include at least 5 diverse examples per intent.
- Do NOT include a `slots:` section in `nlu.yml`. Return it separately under `# slots`.

---

Here are the user utterances:
{examples}

Now return:
# nlu.yml
[...]

# slots
- ...
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
    print("Error:", response.status_code)
    print(response.text)
