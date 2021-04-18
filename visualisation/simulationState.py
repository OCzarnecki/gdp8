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

    def __init__(self, file, readable=True):
        # readable is if we need to preprocess the json file since it is in a human readable format
        # the correct format is exactly one line per json object
        self.file = file # read only
        self.readable = readable

        self.data = self.read_file() # read only
        self.x_size = self.data[0]['map_width']
        self.y_size = self.data[0]['map_height']
        self.max_water_capacity = self.data[0]['max_water_capacity']

        self.time = 0 # read only

        # assuming there is one line for each [0, self.max_time]
        self.max_time = len(self.data)-2
        assert(self.data[-1]['tick_number'] == self.max_time)

        self.max_agent = 10
        self.load(0)

    def load(self, time):
        self.time = time # sync time
        #reinitialize agents and cells
        self.agents = []
        self.cells = []

        d = self.data[time+1]
        assert(d['tick_number'] == time)
        for agent in d['agents']:
            self.agents.append(Agent(agent['id'], agent['x'], agent['y'], agent['inventory']))
        for cell in d['cells']:
            self.cells.append(Cell(cell['x'], cell['y'], cell['water']))

    def read_file(self):
        # takes self.file and returns a list of json objects from the file
        with open(self.file) as f:
            s = f.read()
        if self.readable:
            s = self.reformat_from_readable(s)
        return [json.loads(line) for line in s.splitlines()]


    def reformat_from_readable(self, s):
        # human readable play not have exactly one line per json object
        # This uses the observation that in json }{ cannot occur in a single object
        # Note: so long as no string value containing } whitespace { appears in the json document
        return ''.join(s.split()).replace('}{', '}\n{')

    def count_survivors(self):
        return sum(1 for agent in self.agents if agent.inventory > 0)
