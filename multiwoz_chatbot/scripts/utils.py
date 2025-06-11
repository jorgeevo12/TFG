import json
from pathlib import Path

DIALOG_ACTS_PATH = Path("data/multiwoz/data/MultiWOZ_2.2/dialog_acts.json")

# Cargar los actos de diálogo
try:
    with open(DIALOG_ACTS_PATH, encoding='utf-8') as f:
        ALL_DIALOG_ACTS = json.load(f)
except FileNotFoundError:
    ALL_DIALOG_ACTS = {}
    print(f"Warning: {DIALOG_ACTS_PATH} not found")

def get_dialog_acts(dialogue_id, turn_id):
    """Obtiene el dialog_act completo y su versión simplificada según las nuevas reglas"""
    if not dialogue_id.endswith('.json'):
        dialogue_id += '.json'
    
    dialog_acts = ALL_DIALOG_ACTS.get(dialogue_id, {})
    turn_acts = dialog_acts.get(str(turn_id), {})
    
    if turn_acts.get("dialog_act", {}):
        full_da = next(iter(turn_acts["dialog_act"].keys()))
        
        # Procesar expected_DA según las nuevas reglas
        if "-" in full_da:
            domain, da_part = full_da.split("-", 1)
            domain = domain.lower()
            da_part = da_part.lower()
            
            if domain == "general":
                expected_da = f"general-{da_part}"
            elif da_part in ["inform", "request"]:
                expected_da = f"{domain}-{da_part}"
            else:
                expected_da = f"{domain}-inform"
        else:
            expected_da = full_da.lower()
        
        return full_da, expected_da
    return None, "other"

def build_prompt(utterance, speaker):
    """Generates high-precision dialogue act classifier with slot-level clarity"""
    speaker_role = "System" if speaker == "SYSTEM" else "User"

    prompt = f"""
STRICT DIALOGUE ACT CLASSIFICATION
For this {speaker_role} utterance, respond EXACTLY with:
domain-dialogue_act [or comma-separated list if multiple]
AND for each `inform` or `request`, include the slot(s) using the format: [slot=slot_name]

VALID COMPONENTS:
┌───────────────┬──────────────────────────────┐
│ DOMAINS       │ DIALOGUE ACTS                │
├───────────────┼──────────────────────────────┤
│ restaurant    │ inform, request              │
│ hotel         │ inform, request              │
│ taxi          │ inform, request              │
│ train         │ inform, request              │
│ attraction    │ inform, request              │
│ booking       │ inform, request              │
│ general       │ greet, bye, welcome          │
└───────────────┴──────────────────────────────┘

IMPORTANT SLOT INSTRUCTIONS:
Only for dialogue_act `inform` and `request` there is an associated slot.
You must identify which slot is being provided or requested (e.g. `date`, `type_of_food`, `price_range`).
When naming the slots, please **always use the same name** for the same type of information.
Only include slots for the information that is actually **present** in the utterance (do not guess missing slots).
For every `inform` or `request` act, there is **at least one** slot.
Do not use synonyms or paraphrased slot names — be consistent.
Use the format: domain-dialogue_act [slot=slot_name]

❌ NEVER generate:
- general-inform
- general-request
- ANY tag that ends with `-dialogue_act` (e.g. train-dialogue_act ❌)
- ANY domain-act combination that is not in the VALID COMPONENTS table

✅ General domain can ONLY be: general-greet, general-bye, general-welcome

CRITICAL RULES:
1. GENERAL DOMAIN:
   • ONLY: general-greet, general-bye, general-welcome
   • NEVER combine with inform or request
2. SPECIFIC DOMAINS:
   • ONLY: inform or request
   • NEVER combine with greet/bye/welcome
3. FORMAT:
   • Strictly lowercase
   • No punctuation except commas between acts
   • No additional text/explanations

PARADIGMATIC EXAMPLES:
[Single Act]
• "Hello" → general-greet
• "Find hotels" → hotel-request [slot=location]
• "Taxi available?" → taxi-request [slot=destination]
• "Goodbye" → general-bye

[Multiple Acts]
• "Hi book taxi" → general-greet,taxi-request [slot=destination]
• "Thanks! Hotel info?" → general-welcome,hotel-request [slot=location]
• "Bye! Train at 5" → general-bye,train-inform [slot=time]

STRICT FORMAT RULES:
- ALWAYS lowercase, no spaces/punctuation
- Single acts: domain1-act1
- Multiple acts: domain1-act1,domain2-act2
- If slot(s), append with [slot=name], [slot=name2]
- ❌ NEVER use general-inform, general-request or anything ending in -dialogue_act

FINAL CLASSIFICATION:
{speaker_role} utterance: "{utterance}"
→ """
    
    return prompt
