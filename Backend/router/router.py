from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.ensemble_service import run_both_models
from database import SessionLocal
from models import History
from auth import decode_token

router = APIRouter()
bearer = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    username = decode_token(credentials.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return username

class InputText(BaseModel):
    text: str

@router.post("/convert")
def convert_text(data: InputText, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    text = data.text.strip()
    if not text:
        return {"mbart": "", "mt5": ""}
    results = run_both_models(text)
    db.add(History(
        input_text=text,
        mbart_output=results.get("mbart", ""),
        mt5_output=results.get("mt5", ""),
        username=current_user
    ))
    db.commit()
    return results

@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = db.query(History).filter(History.username == current_user).order_by(History.id.desc()).all()
    return [{"id": d.id, "input": d.input_text, "mbart": d.mbart_output or "", "mt5": d.mt5_output or ""} for d in data]

@router.delete("/history")
def delete_history(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db.query(History).filter(History.username == current_user).delete()
    db.commit()
    return {"message": "History cleared"}