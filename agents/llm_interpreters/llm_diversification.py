class LLMDiversificationInterpreter:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def interpret(self, data):
        prompt = f"""
        You are a portfolio analyst. Interpret the following diversification metrics:

        {data}

        Provide:
        - sector exposure
        - concentration risk
        - correlation risk
        - a concise summary
        """

        if self.llm is None:
            return "LLM not connected yet."
        return self.llm(prompt)
