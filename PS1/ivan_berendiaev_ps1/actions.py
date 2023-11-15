class Up:
    @staticmethod
    def apply(state):
        return (state[0], state[1] + 1, state[2])
    
class Down:
    @staticmethod
    def apply(state):
        return (state[0], state[1] - 1, state[2])
    
class Left:
    @staticmethod
    def apply(state):
        return (state[0] - 1, state[1], state[2])
    
class Right:
    @staticmethod
    def apply(state):
        return (state[0] + 1, state[1], state[2])
    
class TurnClockwise:
    @staticmethod
    def apply(state):
        new_angle = state[2] - 1 if state[2] > 0 else 3
        return (state[0], state[1], new_angle)
    
class TurnCounterClockwise:
    @staticmethod
    def apply(state):
        new_angle = state[2] + 1 if state[2] < 3 else 0
        return (state[0], state[1], new_angle)