import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated" / "domain.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer el contenido de domain.yml ---
domain_content = DOMAIN_FILE.read_text(encoding="utf-8")

# --- Construir el prompt ---
prompt = f"""
You are a RASA 3.1 assistant expert.

You will receive the current contents of domain.yml. Your task is to convert it into a form-based assistant using **one form per domain**.

---

Your goals:

1. The assistant handles the following domains:
   - `restaurant`
   - `hotel`
   - `train`
   - `taxi`

2. For each domain, create a form:
   - `restaurant_form`
   - `hotel_form`
   - `train_form`
   - `taxi_form`

3. Assign only the relevant slots to each form, based on these associations:

   - `restaurant_form`: food, price, phone, location, reservation
   - `hotel_form`: price, phone, location, reservation
   - `train_form`: station, price, phone
   - `taxi_form`: location, phone, price

4. Under `slots:`, define each slot using the following format:
   slot_name:
     type: text
     mappings:
       - type: from_entity
         entity: slot_name

5. Add a `forms:` section with the required slots for each form.

6. For each required slot, define a response named `utter_ask_<slot>` with 2-3 variants that are **appropriate for the domain**.
   - For example:
     - In the restaurant domain: `utter_ask_food` → "What type of food would you like?"
     - In the train domain: `utter_ask_station` → "What station are you departing from?"

7. For each form, add a domain-specific confirmation utterance at the end of the form:
   - Name: `utter_confirm_all_<domain>`
   - This utterance must include all required slots for that domain using {{slot}} format.
   - Example for hotel:
     - "Perfect. You're booking a hotel in {{location}} with a budget of {{price}}. We'll call you at {{phone}} to confirm your reservation for {{reservation}}."

---

INSTRUCTIONS:
- Only return valid YAML (no markdown, no code fences).
- Do not include domain descriptions or explanations.
- Use only the slots provided in the original domain.yml.
- Responses and form structure must comply with RASA 3.1 format.

---

Here is the current domain.yml:
{domain_content}

Now return the updated domain.yml:
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Resultado ---
if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("Error:", response.status_code)
    print(response.text)
