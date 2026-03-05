import requests
import os
import time
from typing import Optional

ASI1_URL = "https://api.asi1.ai/v1/chat/completions"


def call_asi1(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 1000,
    retries: int = 3,
) -> str:
    """
    Reusable wrapper for ASI-1 API calls.
    Handles auth, retries, and error extraction.
    """
    api_key = os.getenv("ASI1_API_KEY")
    if not api_key:
        raise EnvironmentError("ASI1_API_KEY not set in environment variables.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": "asi1-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(ASI1_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                # Rate limited — wait and retry
                wait = 2 ** attempt
                print(f"[ASI-1] Rate limited. Retrying in {wait}s... (attempt {attempt}/{retries})")
                time.sleep(wait)
            else:
                raise RuntimeError(f"ASI-1 API error {response.status_code}: {response.text}") from e

        except requests.exceptions.Timeout:
            if attempt == retries:
                raise RuntimeError("ASI-1 API timed out after multiple retries.")
            time.sleep(2)

        except Exception as e:
            raise RuntimeError(f"Unexpected error calling ASI-1: {str(e)}") from e

    raise RuntimeError("ASI-1 API call failed after all retries.")
