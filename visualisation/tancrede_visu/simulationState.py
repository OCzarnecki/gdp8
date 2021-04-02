class Cell():

    def __init__(self, x, y, water):
        self.x = x
        self.y = y
        self.water = water

class Agent():

    def __init__(self, x, y, inventory, id):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.id = id
        #For now let's pretend the agents move randomly, so we add a velocity
        self.vx = 2
        self.vy = 2


class State():
    """
    Represents simulation state at a fixed time
    Load json file
    """

    def __init__(self, file):
        self.file = file
        self.x_size = 0
        self.y_size = 0
        self.max_water_capacity = 0
        self.agents = []
        self.cells = []
        self.time = 0
        self.max_time = 0
        self.load(0)

        # test code
        self.x_size = 1
        self.y_size = 2
        self.agents = [Agent(500, 500, 0, 0)]
        self.cells = [Cell(25, 25, 10), Cell(350, 286, 96)]

    def load(self, time):
        # update state to use a new simulation time
        pass
