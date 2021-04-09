import json

class Cell():

    def __init__(self, x, y, water):
        self.x = x
        self.y = y
        self.water = water

class Agent():

    def __init__(self, id, x, y, inventory):
        self.id = id
        self.x = x
        self.y = y
        self.inventory = inventory


class State():
    """
    Represents simulation state at a fixed time
    Load json file
    """

    def __init__(self, file):
        #opening the json file
        f = open(file)

        #getting the dictionary
        data = json.load(f)

        self.file = file
        self.x_size = data['header']['map_width']
        self.y_size = data['header']['map_height']
        self.max_water_capacity = data['header']['max_water_capacity']

        f.close()

        self.time = 0
        self.max_time = 30
        self.max_agent = 50
        self.load()

    def load(self):
        #reinitialize agents and cells
        self.agents = []
        self.cells = []

        #opening the json file
        f = open(self.file)

        #getting the dictionary
        data = json.load(f)

        for d in data['tick_line']:
            if d['tick_number'] == self.time:
                for agent in d['agents']:
                    self.agents.append(Agent(agent['id'], agent['x'], agent['y'], agent['inventory']))
                for cell in d['cells']:
                    self.cells.append(Cell(cell['x'], cell['y'], cell['water']))

        f.close()
