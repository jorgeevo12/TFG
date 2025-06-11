import json
from pathlib import Path
from utils import get_dialog_acts

# Base del proyecto (dos niveles arriba de /scripts/)
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "multiwoz" / "data" / "MultiWOZ_2.2" / "train" / "dialogues_001.json"
OUTPUT_FILE = BASE_DIR / "data" / "multiwoz_dialogues" / "processed_dialogues.json"

def preprocess_dialogues():
    with open(INPUT_FILE, encoding='utf-8') as f:
        dialogues = json.load(f)
    
    processed = []
    for dialog in dialogues[:10]:  # Procesar primeros 10 diálogos
        turns = []
        for turn in dialog["turns"]:
            full_da, _ = get_dialog_acts(dialog["dialogue_id"], turn["turn_id"])

            # Procesar expected_DA según las nuevas reglas
            if full_da:
                full_da_lower = full_da.lower()
                if "-" in full_da_lower:
                    domain, da_part = full_da_lower.split("-", 1)
                    if domain == "general":
                        expected_da = full_da_lower
                    elif da_part not in ["inform", "request"]:
                        expected_da = f"{domain}-inform"
                    else:
                        expected_da = full_da_lower
                else:
                    expected_da = full_da_lower
            else:
                expected_da = "other"
            
            turns.append({
                "speaker": turn["speaker"],
                "utterance": turn["utterance"],
                "turn_id": turn["turn_id"],
                "dialog_act": full_da,
                "expected_DA": expected_da
            })
        
        processed.append({
            "dialogue_id": dialog["dialogue_id"],
            "turns": turns
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(processed, indent=2, ensure_ascii=False))
    print(f"✅ Processed {len(processed)} dialogues. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess_dialogues()
