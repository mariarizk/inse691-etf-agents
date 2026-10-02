class LLMTechnicalInterpreter:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def interpret(self, data):
        prompt = f"""
        You are a technical analyst. Interpret the following technical indicators:

        {data}

        Provide:
        - trend direction
        - momentum
        - support/resistance
        - key signals (RSI, MACD, moving averages)
        - a concise summary
        """

        if self.llm is None:
            return "LLM not connected yet."
        return self.llm(prompt)
