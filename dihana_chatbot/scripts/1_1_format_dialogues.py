import json
from pathlib import Path

# --- Configuración de rutas relativas ---
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "dihana" / "dihana_dialogues" / "processed_dialogues.json"
OUTPUT_DIR = BASE_DIR / "dihana_chatbot" / "results"
OUTPUT_FILE = OUTPUT_DIR / "formatted_dialogues.json"

# --- Crear directorio de salida si no existe ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Cargar y reformatear los primeros 10 diálogos ---
with INPUT_FILE.open(encoding="utf-8") as f:
    dialogues = json.load(f)

formatted_dialogues = []
for dialog in dialogues[:10]:
    formatted_turns = [{turn["speaker"]: turn["text"]} for turn in dialog["turns"]]
    formatted_dialogues.append({
        "dialogue_id": dialog["dialogue_id"],
        "turns": formatted_turns
    })

# --- Guardar resultado ---
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(formatted_dialogues, f, indent=2, ensure_ascii=False)

print(f"Saved to: {OUTPUT_FILE}")
