import requests
import config

resp = requests.post(
    f"{config.OPENROUTER_BASE_URL}/embeddings",
    headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
    json={"model": config.EMBEDDING_MODEL, "input": ["first sentence", "second sentence"]},
)
print(resp.status_code)
print(resp.text)