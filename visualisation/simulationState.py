import json
import numpy as np

WIDTH = 900
HEIGHT = 600

def computePos(x, y, tw, th, twc, thc):
    return np.array([(x * tw) + twc, (y * th) + thc])

class Cell():

    def __init__(self, pos, water):
        self.pos = pos
        self.water = water

class Agent():

    def __init__(self, id, pos, desired_pos, inventory):
        self.pos = pos
        self.desired_pos = desired_pos
        self.vel = np.array([0, 0])
        self.desired_dir = np.array([0, 0])
        self.inventory = inventory
        self.id = id


class State():

    def __init__(self, file, readable=True):
        # readable is if we need to preprocess the json file since it is in a human readable format
        # the correct format is exactly one line per json object
        self.file = file # read only
        self.readable = readable

        self.data = self.read_file() # read only
        self.x_size = self.data[0]['x_size']
        self.y_size = self.data[0]['y_size']
        self.max_water_capacity = self.data[0]['max_water_capacity_cell']
        self.max_inventory = self.data[0]['max_water_capacity_agent']

        self.time = 0 # read only

        # assuming there is one line for each [0, self.max_time]
        self.max_time = len(self.data)-2
        assert(self.data[-1]['tick_number'] == self.max_time)
        self.agents = []
        self.max_agent = 10

        self.tile_width = WIDTH / self.x_size
        self.tile_height = HEIGHT / self.y_size
        self.pit_max_radius = min(self.tile_width/2, self.tile_height/2)

        self.load()

    def load(self):
        #reinitialize agents and cells
        self.cells = []
        #temporary array as we want to keep track of the velocity
        newAgents = []

        twcenter = self.tile_width / 2
        thcenter = self.tile_height / 2

        d = self.data[self.time+1]
        assert(d['tick_number'] == self.time)
        #agents on the next iteration, we want to know their position
        nextTime = self.time+2
        if self.time == self.max_time:
            nextTime = 1

        desired_pos_agents = self.data[nextTime]['agents']

        j = 0 
        for agent in d['agents']:
            desired_pos_x = -1
            desired_pos_y = -1
            if j<len(desired_pos_agents) and desired_pos_agents[j]['id']==agent['id']:
                desired_pos_x = desired_pos_agents[j]['x']
                desired_pos_y = desired_pos_agents[j]['y']
                j += 1
            pos = computePos(agent['x'], agent['y'], self.tile_width, self.tile_height, twcenter, thcenter)
            if desired_pos_x == -1:
                newAgents.append(Agent(agent['id'],
                    pos,
                    pos,
                    agent['inventory']))
            else:
                newAgents.append(Agent(agent['id'],
                    pos,
                    computePos(desired_pos_x, desired_pos_y, self.tile_width, self.tile_height, twcenter, thcenter),
                    agent['inventory']))
        for cell in d['cells']:
            self.cells.append(Cell(computePos(cell['x'], cell['y'], self.tile_width, self.tile_height, twcenter, thcenter), cell['water']))
        
        if self.agents != []:
            i = 0
            for newAgent in newAgents:
                while newAgent.id != self.agents[i].id:
                    i += 1
                newAgent.vel = self.agents[i].vel
                newAgent.pos = self.agents[i].pos
                newAgent.desired_dir = self.agents[i].desired_dir
        self.agents = newAgents

        if self.time == self.max_time:
            self.time = 0
        else:
            self.time += 1
    
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
