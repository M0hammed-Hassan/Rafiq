import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set."
    )

CHAT_MODEL = os.getenv("OPENAI_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
REQUEST_TIMEOUT_SECONDS = 20


MAX_QUESTION_CHARS = 300

TOP_K = 4
CHUNK_SIZE_TOKENS = 200
CHUNK_OVERLAP_TOKENS = 50
COMPANY_KB_SCOPE = "company_kb"
SUPPORTED_DOC_EXTENSIONS = (".md", ".txt", ".pdf")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_DIR = os.path.join(BASE_DIR, "data", "docs")
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma_db")
COLLECTION_NAME = "rafiq_docs"
