import logging
from fastapi import FastAPI
from app.routes.ask_routes import router
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

app = FastAPI(title="Rafiq")
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["POST"],
)

app.include_router(router)