import os

from dotenv import load_dotenv
from google import genai
import time
load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt):

        for attempt in range(3):

            try:

                response = (
                    self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                )

                return response.text

            except Exception as e:

                if attempt < 2:

                    time.sleep(2)

                else:

                    raise RuntimeError(
                        f"Gemini request failed: {e}"
                    )