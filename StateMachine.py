class StateMachine:
    def __init__(self):
        self.states = ("startPage", "projectPage", "loadPage", "deletePage")
        self.state = self.states[0]

    def setState(self, index):
        self.state = self.states[index]

    def getState(self):
        return self.state
    
    def getStateIndex(self):
        return self.states.index(self.state)

    