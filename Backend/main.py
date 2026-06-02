from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.router import router
from router.auth_router import router as auth_router
from database import engine, Base
import models

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Sindhi Transliterator API running"}