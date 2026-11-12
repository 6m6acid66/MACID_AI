import requests

from .config import OLLAMA_URL, MODEL_NAME


def generate_response(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=180
        )

        response.raise_for_status()
        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to local Ollama. "
            "Check that Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The local AI engine took too long to respond."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Local AI engine error: {error}"
        )
