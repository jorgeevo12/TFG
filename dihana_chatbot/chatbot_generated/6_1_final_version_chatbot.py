import requests
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "dihana_chatbot" / "chatbot_generated" / "domain.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# Leer contenido actual del dominio
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")

# Prompt para actualizar solo domain.yml
prompt = f"""
You are a RASA 3.1 assistant expert.

You will receive the current contents of domain.yml. Your task is to convert it into a form-based assistant that uses a form called `trip_form` to collect 5 required slots:

- date
- time
- origin
- destination
- price

---

🎯 Your task:

1. Add a `forms:` section with `trip_form` and the 5 required slots.
2. Ensure that each slot is declared under `slots:` with mappings using `type: from_entity`.
3. Add the following responses:
   - utter_ask_date
   - utter_ask_time
   - utter_ask_origin
   - utter_ask_destination
   - utter_ask_price
   - utter_confirm_all
4. Ensure all structure and indentation follows RASA 3.1 syntax.

❗ Do not return anything else. Only valid YAML for domain.yml.
Do not include markdown or triple backticks.

---

Here is the current domain.yml:
{domain_content}

Now return the updated domain.yml:
"""

# Enviar prompt al modelo
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# Mostrar el resultado generado
if response.status_code == 200:
    result = response.json().get("response", "")
    print(result)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
