import requests
import json

BASE_URL = "http://127.0.0.1:8000/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer dummy-key"
}

MODELS = {
    "thinking_not_search": True,
    "thinking_search": True,
    "not_thinking_not_search": True,
    "not_thinking_search": True
}

TEST_STREAMING = {
    "stream": False,
    "non_stream": True,
}

PAYLOAD_TEMPLATE = {
    "messages": [
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "temperature": 0.7
}

def run_request(model_id, stream: bool):
    payload = dict(PAYLOAD_TEMPLATE)
    payload["model"] = model_id
    payload["stream"] = stream

    print(f"\n=== Running model={model_id} stream={stream} ===")

    if stream:
        with requests.post(BASE_URL, headers=HEADERS, json=payload, stream=True) as r:
            for chunk in r.iter_lines():
                if chunk:
                    decoded = chunk.decode("utf-8")
                    print(decoded)
    else:
        r = requests.post(BASE_URL, headers=HEADERS, json=payload)
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text)

def main():
    for model_id, enabled in MODELS.items():
        if not enabled:
            continue

        if TEST_STREAMING["non_stream"]:
            run_request(model_id, stream=False)

        if TEST_STREAMING["stream"]:
            run_request(model_id, stream=True)

if __name__ == "__main__":
    main()