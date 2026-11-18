from datetime import datetime


class Blackboard:

    def __init__(self):

        self.data = {}
        self.log = []

    def write(self, agent_name, result):

        print(f"BLACKBOARD WRITE -> {agent_name}")

        self.data[agent_name] = result

        self.log.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "agent": agent_name,
                "result": result
            }
        )

    def read(self, agent_name):

        return self.data.get(agent_name)

    def all(self):
        return self.data

    def missing(self, required):

        return [
            r
            for r in required
            if r not in self.data
        ]

    def get_log(self):

        return self.log