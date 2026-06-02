from services.mbart_service import run_mbart
from services.mt5_service import run_mt5

def run_both_models(text: str):
    mbart_output = run_mbart(text)
    mt5_output   = run_mt5(text)
    return {
        "mbart": mbart_output,
        "mt5":   mt5_output
    }
