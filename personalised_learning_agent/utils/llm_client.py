import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing from the .env file."
    )

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1200,
) -> str:

    response = _client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=0.5,
    )

    if not response.choices:
        raise RuntimeError(
            "OpenRouter returned no response choices. "
            "Try running the command again."
        )

    message = response.choices[0].message
    content = message.content

    if content:
        return content.strip()

    print("Model used:", response.model)
    print("Finish reason:", response.choices[0].finish_reason)

    raise RuntimeError(
        "The selected free model returned no final text. "
        "Run the command again or change OPENROUTER_MODEL."
    )