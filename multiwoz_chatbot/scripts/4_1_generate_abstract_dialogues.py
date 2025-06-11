import json
from pathlib import Path
from collections import defaultdict

# Definir BASE_DIR y rutas relativas
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "multiwoz_chatbot" / "results" / "llama3_results.json"
OUTPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "abstract_dialogues_slots.json"

def generate_structured_abstract_dialogues():
    with INPUT_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    dialogues = defaultdict(list)

    for turn in data["details"]:
        dialogue_id = turn["dialogue_id"]
        expected_da = turn.get("expected_DA", "other")
        slot_values = turn.get("slots", [])
        speaker = turn.get("speaker", "").lower()

        # Añadir el prefijo user- o system- al act
        act = f"{speaker}-{expected_da.lower()}" if speaker in ["user", "system"] else expected_da.lower()

        dialogues[dialogue_id].append({
            "act": act,
            "slots": slot_values
        })

    output = []
    for dialogue_id, turns in dialogues.items():
        output.append({
            "dialogue_id": dialogue_id,
            "abstract_dialogue": turns
        })

    OUTPUT_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"✅ Saved structured dialogues with slots to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_structured_abstract_dialogues()
