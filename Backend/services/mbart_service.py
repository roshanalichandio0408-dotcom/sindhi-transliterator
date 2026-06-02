from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "mbart")

print("⏳ Loading MBART...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()
print("✅ MBART loaded!")

def run_mbart(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
