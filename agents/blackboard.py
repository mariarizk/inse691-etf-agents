class Blackboard:
    def __init__(self):
        self.data = {}

    def write(self, agent_name, result):
        self.data[agent_name] = result

    def read(self, agent_name):
        return self.data.get(agent_name)

    def all(self):
        return self.data

    def missing(self, required):
        return [r for r in required if r not in self.data]
