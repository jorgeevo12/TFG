import json
from pathlib import Path

# Definir BASE_DIR y rutas relativas
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "processed_dialogues.json"
OUTPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "abstract_dialogues.json"

def generate_abstract_dialogues():
    with INPUT_FILE.open(encoding="utf-8") as f:
        dialogues = json.load(f)

    abstract_dialogues = []

    for dialog in dialogues:
        sequence = [turn["expected_DA"] for turn in dialog["turns"] if turn.get("expected_DA")]
        abstract_dialogues.append({
            "dialogue_id": dialog["dialogue_id"],
            "abstract_dialogue": sequence
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(abstract_dialogues, indent=2, ensure_ascii=False))
    print(f"Saved {len(abstract_dialogues)} abstract dialogues to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_abstract_dialogues()
