import json
from pathlib import Path

# --- Configuración de rutas ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "dihana_chatbot" / "results" / "correct_deepseek_results.json"
OUTPUT_FILE = BASE_DIR / "dihana_chatbot" / "results" / "correct_deepseek_results_with_act_dialogue.json"

# --- Cargar datos originales ---
with INPUT_FILE.open(encoding="utf-8") as f:
    dialogues = json.load(f)

# --- Construir nueva estructura ---
processed = {}

for dialogue in dialogues:
    dialogue_id = dialogue["dialogue_id"]
    turns = dialogue["turns"]

    act_dialogue_list = [
        {"act_dialogue": turn["act"]} for turn in turns if "act" in turn
    ]

    processed[dialogue_id] = act_dialogue_list

# --- Guardar resultado ---
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print(f"Archivo generado en: {OUTPUT_FILE}")
