import os
import time

from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    """Thin Gemini wrapper with lazy client creation."""

    def __init__(self, api_key=None):
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client = None

    @property
    def available(self):
        return bool(self._api_key)

    def _get_client(self):
        if not self._api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        if self._client is None:
            from google import genai

            self._client = genai.Client(api_key=self._api_key)

        return self._client

    def generate(self, prompt):
        client = self._get_client()

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise RuntimeError(f"Gemini request failed: {e}")
