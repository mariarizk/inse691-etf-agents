import json
import time

import requests

from config import LLM_CONFIG

RETRYABLE_STATUS = frozenset({429, 500, 503})


class LlmError(RuntimeError):
    pass


class LlmClient:
    """Chat client for any OpenAI-compatible endpoint (Gemini by default, OpenAI via LLM_BASE_URL)."""

    def __init__(self, settings=None):
        self.settings = settings or LLM_CONFIG

    def complete(self, system_prompt, user_prompt, json_output=False):
        if not self.settings["api_key"]:
            raise LlmError("LLM_API_KEY (or GEMINI_API_KEY) is missing from .env")

        payload = {
            "model": self.settings["model"],
            "temperature": self.settings["temperature"],
            "max_tokens": self.settings["max_output_tokens"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if json_output:
            payload["response_format"] = {"type": "json_object"}

        body = self._post_with_retry(payload)
        try:
            return body["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise LlmError(f"Unexpected LLM response: {str(body)[:300]}") from exc

    def complete_json(self, system_prompt, user_prompt):
        text = self.complete(system_prompt, user_prompt, json_output=True)
        cleaned = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise LlmError(f"LLM did not return valid JSON: {text[:300]}") from exc

        if not isinstance(parsed, dict):
            raise LlmError(f"LLM returned JSON that is not an object: {text[:300]}")
        return parsed

    def _post_with_retry(self, payload):
        url = f"{self.settings['base_url']}/chat/completions"
        headers = {"Authorization": f"Bearer {self.settings['api_key']}"}
        retries = self.settings["max_retries"]

        for attempt in range(retries + 1):
            try:
                response = requests.post(
                    url, json=payload, headers=headers, timeout=self.settings["timeout_seconds"]
                )
            except requests.RequestException as exc:
                raise LlmError(f"Could not reach the LLM: {exc}") from exc

            if response.ok:
                try:
                    return response.json()
                except ValueError as exc:
                    raise LlmError("LLM response was not JSON") from exc

            if response.status_code not in RETRYABLE_STATUS or attempt == retries:
                raise LlmError(f"LLM request failed with HTTP {response.status_code}: {response.text[:300]}")

            time.sleep(self.settings["retry_wait_seconds"] * (attempt + 1))

        raise LlmError("LLM retries exhausted")
