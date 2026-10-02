class LLMRiskInterpreter:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def interpret(self, data):
        prompt = f"""
        You are a risk analyst. Interpret the following risk metrics:

        {data}

        Provide:
        - volatility assessment
        - drawdown concerns
        - beta exposure
        - debt/liquidity risk
        - a concise summary
        """

        if self.llm is None:
            return "LLM not connected yet."
        return self.llm(prompt)
