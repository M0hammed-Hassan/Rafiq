from openai import OpenAI
from app.config.settings import CHAT_MODEL, EMBEDDING_MODEL, OPENAI_API_KEY, REQUEST_TIMEOUT_SECONDS


client = OpenAI(api_key=OPENAI_API_KEY, timeout=REQUEST_TIMEOUT_SECONDS)


def chat_completion(messages:list[dict], temperature: float = 0.2, max_tokens: int = 200) -> dict:
    """
    This function for calling the openai model.

    Args:
        messages: The input messages to the client (OpenAI model).
        temperature: This hyperparameter controls the creativity of the model and diversity of response.
        max_tokens: The max output tokens of the model.
    
    Returns:
    A dictionary that contains th answer, finish_reason, usage.
    """
    completion = client.chat.completions.create(
        model = CHAT_MODEL, 
        messages=messages, 
        temperature=temperature, 
        max_tokens=max_tokens
    )

    choice = completion.choices[0]
    return {
        "answer":choice.message.content or "",
        "finish_reason": choice.finish_reason,
        "usgae":
        {
            "prompt_tokens":completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }

def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(model = EMBEDDING_MODEL, input=text)
    return response.data[0].embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]