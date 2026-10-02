class LLMSentimentInterpreter:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def interpret(self, data):
        prompt = f"""
        You are a sentiment analyst. Interpret the following sentiment metrics:

        {data}

        Provide:
        - news tone
        - social sentiment
        - analyst consensus
        - a concise summary
        """

        if self.llm is None:
            return "LLM not connected yet."
        return self.llm(prompt)
