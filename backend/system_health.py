import os


class SystemHealth:

    @staticmethod
    def get_status():

        return {
            "gemini_api_key": (
                "online"
                if os.getenv("GEMINI_API_KEY")
                else "offline"
            ),
            "pipeline": "online",
            "blackboard": "online"
        }