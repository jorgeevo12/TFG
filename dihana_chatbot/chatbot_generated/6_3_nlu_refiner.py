import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "dihana_chatbot" / "chatbot_generated" / "data" / "nlu.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

nlu_content = NLU_FILE.read_text(encoding="utf-8")

# Prompt para refinar el contenido del NLU existente
prompt = f"""
You are a RASA 3.1 assistant builder.

You will receive the current `nlu.yml` content of a travel assistant that uses a form called `trip_form` to collect these slots:
- date
- time
- origin
- destination
- price

---

📄 TASK:
Improve and extend the `nlu.yml` content:
- Ensure each of these intents has at least 10 high-quality, diverse training examples:
  - inform_date
  - inform_time
  - inform_origin
  - inform_destination
  - inform_price
  - request_trip

- Annotate slot values using [value](entity) format.
- Add realistic phrases for each intent.
- Keep existing examples, but expand and improve where possible.

---

‼️ INSTRUCTIONS:
- Return only valid YAML (Rasa 3.1 format).
- Do not include markdown, code fences or explanations.
- Do not regenerate the entire file from scratch — build on top of the existing examples provided.

Here is the current nlu.yml content:

{nlu_content}

Now output the improved:
# nlu.yml
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

if response.status_code == 200:
    result = response.json().get("response", "")
    print(result)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
