# backend/agentlogger.py

from datetime import datetime


class AgentLogger:

    logs = []

    @classmethod
    def log(
        cls,
        agent,
        tool_used,
        status,
        execution_time_ms,
        metadata=None
    ):

        cls.logs.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "agent": agent,
                "tool_used": tool_used,
                "status": status,
                "execution_time_ms": execution_time_ms,
                "metadata": metadata or {}
            }
        )

    @classmethod
    def get_logs(cls):

        return cls.logs