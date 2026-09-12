import logging
from fastapi import FastAPI
from app.routes.ask_routes import router as ask_router
from app.routes.upload_routes import router as upload_router
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

app = FastAPI(title="Rafiq")
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["POST"],
)

app.include_router(ask_router)
app.include_router(upload_router)