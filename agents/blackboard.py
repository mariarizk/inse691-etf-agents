from datetime import datetime, timezone


class Blackboard:
    def __init__(self):
        self.data = {}
        self.log = []

    def write(self, agent_name, result):
        self.data[agent_name] = result
        self.log.append({
            "step": len(self.log) + 1,
            "sender": agent_name,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "content": result,
        })

    def read(self, agent_name):
        return self.data.get(agent_name)

    def all(self):
        return self.data

    def history(self):
        return list(self.log)

    def missing(self, required):
        return [r for r in required if r not in self.data]
