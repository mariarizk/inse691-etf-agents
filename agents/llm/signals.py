from agents.decision_agent import ANALYST_AGENTS

NEWS_AGENT = "news_sentiment"
CONTEXT_AGENTS = ANALYST_AGENTS + (NEWS_AGENT,)


def context_signals(board):
    """Agent outputs the LLM agents reason over; news is included only when it was collected."""
    return {name: board[name] for name in CONTEXT_AGENTS if name in board}
