class LLMFundamentalInterpreter:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def interpret(self, data):
        prompt = f"""
        You are a financial analyst. Interpret the following fundamental metrics:

        {data}

        Provide:
        - strengths
        - weaknesses
        - valuation concerns
        - growth signals
        - a concise summary
        """

        if self.llm is None:
            return "LLM not connected yet."
        return self.llm(prompt)
