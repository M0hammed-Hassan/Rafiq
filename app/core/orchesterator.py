from app.core.retrieval import retrieve
from app.core.synthesis import synthesize
from app.config.settings import COMPANY_KB_SCOPE
from app.core.direct_agent import answer_directly
from app.core.router import is_confident_direct_answer



def _answer_from_scope(question: str, scope:str, mode:str, not_found_note: str) -> dict:
    chunks = retrieve(question, scope=scope)
    if not chunks:
        return {
            "answer":f"{not_found_note} please upload a relevant document and I will answer from it",
            "finish_reason": "stop",
            "usage": {"prompt_tokens":0, "completion_tokens":0, "total_tokens":0},
            "sources": [],
            "mode":mode,
            "needs_upload":True
        }

    results = synthesize(question, chunks)
    results["mode"] = mode
    results["needs_upload"] = False
    return results


def handle_question(question:str, document_id: str | None = None) -> dict:
    if document_id:
        return _answer_from_scope(
            question,
            scope = f"session:{document_id}",
            mode="strict_document",
            not_found_note="No relevant content found in the uploaded document for this question."
        )
    if is_confident_direct_answer(question):
        result = answer_directly(question)
        result["mode"] = "direct"
        result["needs_upload"] = False
        return result

    return _answer_from_scope(
        question,
        COMPANY_KB_SCOPE,
        mode="retrieved",
        not_found_note="No relevant company documents found for this question"
    )

