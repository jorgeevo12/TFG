import json
from pathlib import Path
import re

# Definir directorios
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "dihana" / "data"
OUTPUT_DIR = BASE_DIR / "data" / "dihana" / "dihana_dialogues"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "processed_dialogues.json"

# Patrón para detectar turnos del tipo M1:, U2:, etc.
TURN_HEADER = re.compile(r"^(M|U)\d+: (.+)$")
# Patrón para detectar anotaciones
ANNOTATION_LINE = re.compile(r"^\(.*?\)\s*pal:")

def parse_dialogue_file(file_path):
    turns = []

    with open(file_path, encoding="latin-1") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()

        match = TURN_HEADER.match(line)
        if match:
            speaker = "SYSTEM" if match.group(1) == "M" else "USER"
            text = match.group(2).strip()

            # Evitamos incluir líneas repetidas o anotaciones
            if text and not ANNOTATION_LINE.match(text):
                turns.append({
                    "speaker": speaker,
                    "text": text
                })

    return turns

def process_all_dialogues():
    all_dialogues = []

    for dia_file in INPUT_DIR.rglob("*.dia"):
        dialogue_id = dia_file.stem
        turns = parse_dialogue_file(dia_file)

        if turns:
            all_dialogues.append({
                "dialogue_id": dialogue_id,
                "turns": turns
            })

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_dialogues, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_dialogues)} dialogues to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_all_dialogues()
