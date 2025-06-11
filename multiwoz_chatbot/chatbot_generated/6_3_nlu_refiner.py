import requests
from pathlib import Path

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parents[2]
NLU_FILE = BASE_DIR / "multiwoz_chatbot" / "chatbot_generated" / "data" / "nlu.yml"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:14b"

nlu_content = NLU_FILE.read_text(encoding="utf-8")

# Prompt para refinar el contenido del NLU existente
prompt = f"""
You are a RASA 3.1 assistant builder.

You will receive the current `nlu.yml` content of a multi-domain assistant based on the MultiWOZ dataset. The assistant includes four forms: restaurant_form, hotel_form, train_form, and taxi_form. These forms use the following slots:

- price
- food
- phone
- location
- station
- reservation

---

📄 TASK:
Improve and extend the `nlu.yml` content:
- Ensure each of these intents has at least 6 high-quality, diverse training examples:

  🔹 Form activation (requests):
    - restaurant_request
    - hotel_request
    - train_request
    - taxi_request

  🔹 Slot provision (inform):
    - inform_price
    - inform_food
    - inform_phone
    - inform_location
    - inform_station
    - inform_reservation

📌 IMPORTANT:
- All phrases must represent what the **user** would say. These examples should simulate user input — including both **requests to initiate a task** and **providing values for specific slots**.
- For the `inform_reservation` intent, assume the user is providing their **name or reservation name**. Examples: "The booking is under [Alice Smith](reservation)", "It's for [John](reservation)", "My name is [Emma](reservation)".

- Annotate slot values using [value](entity) format.
- Add realistic, natural-sounding user messages for each intent.
- Keep existing examples, but expand and improve them.

---

‼️ INSTRUCTIONS:
- Return only valid YAML (Rasa 3.1 format).
- Do not include markdown, code fences or explanations.
- Do not regenerate the file from scratch — improve what is already present.

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
