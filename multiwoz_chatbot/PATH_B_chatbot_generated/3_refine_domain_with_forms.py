import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
DOMAIN_FILE = BASE_DIR / "multiwoz_chatbot" / "PATH_B_chatbot_generated" / "domain.yml"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

# --- Leer archivo ---
def read(file_path):
    with file_path.open(encoding="utf-8") as f:
        return f.read()

domain_content = read(DOMAIN_FILE)

# --- Construir prompt específico para domain.yml ---
prompt = f"""
You are a RASA 3.1 assistant expert.

You will receive the current contents of domain.yml. Your task is to convert it into a form-based assistant using **one form per domain**.

--- TASKS ---

1. The assistant handles the following domains:
   - `restaurant`
   - `hotel`
   - `train`
   - `taxi`
   - `attraction`

2. For each domain, create a form:
   - `restaurant_form`: food, price, phone, area, people
   - `hotel_form`: price, phone, area, people
   - `train_form`: area, price, phone
   - `taxi_form`: area, phone, price
   - `attraction_form`: area, attraction, price, phone

3. Under `slots:`, define each slot using:
   slot_name:
     type: text
     mappings:
       - type: from_entity
         entity: slot_name

4. Add a `forms:` section with the required slots for each form.

5. For each required slot, define a response named `utter_ask_<slot>` with 2-3 variants that are **appropriate for the domain**.
   - Example (restaurant): `utter_ask_food` → "What type of food would you like?"

6. For each form, add a confirmation utterance at the end:
   - `utter_confirm_all_<domain>` summarizing all slots with {{slot}} format.
   - Example (hotel): "You're booking a hotel in {{area}} with a budget of {{price}} for {{people}} person/people. We'll call {{phone}} to confirm your reservation."

‼️ INSTRUCTIONS:
- Return only valid YAML. No markdown or comments.
- Do not include explanations.
- Use only the slots present in the original domain.yml or needed for the forms.
- Use the following format for responses:

responses:
  utter_ask_slot_name:
    - text: "First option."
    - text: "Second option."
    - text: "Third option."

- Each `utter_*` listed in `responses:` must also be included under `actions:`.
- The `utter_confirm_all_<domain>` must use {{slot}} placeholders for each slot.

Example format:

responses:
  utter_ask_time:
    - text: "What time would you like to depart?"
    - text: "Can you confirm the departure time?"

actions:
  - utter_ask_time

--- Current domain.yml ---
{domain_content}

Now return the updated domain.yml:
"""

# --- Llamada al modelo ---
response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=1800
)

# --- Imprimir resultado ---
if response.status_code == 200:
    print(response.json().get("response", ""))
else:
    print("❌ Error:", response.status_code)
    print(response.text)
