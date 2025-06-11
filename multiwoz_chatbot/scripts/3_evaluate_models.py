import json
import time
import requests
from pathlib import Path
from utils import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELS = ["llama3"]
MAX_DIALOGUES = 10  

def get_predicted_da_and_slots(utterance, speaker, model):
    prompt = build_prompt(utterance, speaker)
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=15
        )
        if response.status_code == 200:
            raw = response.json().get("response", "").strip().lower()

            # Separar la parte de slots si existe
            if "[" in raw and "]" in raw:
                da_part = raw.split("[")[0].strip()
                slot_str = raw.split("[")[1].split("]")[0].strip()
                slot_names = [s.split("=")[-1].strip() for s in slot_str.split(",") if "slot" in s]
            else:
                da_part = raw
                slot_names = []

            das = [d.strip() for d in da_part.split(",") if d]
            return das if das else ["empty"], slot_names
        return ["error"], []
    except Exception as e:
        return [f"error_{str(e)}"], []

def evaluate_models():
    Path("results").mkdir(exist_ok=True)
    
    try:
        with open("data/processed_dialogues.json", encoding='utf-8') as f:
            dialogues = json.load(f)
    except Exception as e:
        print(f"Error loading dialogues: {str(e)}")
        return

    for model in MODELS:
        print(f"\nEvaluating {model} (first {MAX_DIALOGUES} dialogues)...")
        results = []
        correct = 0
        partial = 0
        total = 0
        
        for dialog in dialogues[:MAX_DIALOGUES]: 
            print(f"\nProcessing dialogue: {dialog['dialogue_id']}")
            for turn in dialog["turns"]:
                pred_das, slots = get_predicted_da_and_slots(turn["utterance"], turn["speaker"], model)
                expected_da = turn["expected_DA"]
                
                # Determine evaluation result
                if expected_da in pred_das:
                    result = "correct" if len(pred_das) == 1 else "partial"
                    correct += result == "correct"
                    partial += result == "partial"
                else:
                    result = "incorrect"
                total += 1
                
                results.append({
                    "dialogue_id": dialog["dialogue_id"],
                    "turn_id": turn["turn_id"],
                    "speaker": turn["speaker"],
                    "utterance": turn["utterance"][:100] + ("..." if len(turn["utterance"]) > 100 else ""),
                    "full_dialog_act": turn["dialog_act"],
                    "expected_DA": expected_da,
                    "predicted_DAs": pred_das,
                    "slots": slots,
                    "result": result
                })
                
                color = {
                    "correct": "\033[92m",
                    "partial": "\033[93m",
                    "incorrect": "\033[91m"
                }.get(result, "")
                
                print(f"  Turn {turn['turn_id']}: {color}{', '.join(pred_das)} | slots: {slots} \033[0m (Expected: {expected_da})")
                time.sleep(1)

        # Guardar resultados
        output_path = Path(f"results/{model}_results.json")
        with output_path.open("w", encoding="utf-8") as f:
            json.dump({
                "accuracy": correct / total if total > 0 else 0,
                "partial_accuracy": (correct + partial/2) / total if total > 0 else 0,
                "total_dialogues": min(MAX_DIALOGUES, len(dialogues)),
                "total_turns": total,
                "correct_turns": correct,
                "partial_turns": partial,
                "incorrect_turns": total - correct - partial,
                "details": results
            }, f, indent=2)
        
        print(f"\nModel: {model}")
        print(f"Evaluated dialogues: {min(MAX_DIALOGUES, len(dialogues))}/{len(dialogues)}")
        print(f"Correct: {correct} ({correct/total:.2%})")
        print(f"Partial: {partial} ({partial/total:.2%})")
        print(f"Incorrect: {total - correct - partial} ({1 - (correct + partial)/total:.2%})")
        print(f"Partial Accuracy (correct + partial/2): {(correct + partial/2)/total:.2%}")
        print(f"Results saved to {output_path}")

if __name__ == "__main__":
    print("Starting evaluation...")
    evaluate_models()
    print("\nEvaluation completed.")
