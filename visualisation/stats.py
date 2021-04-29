"""
Next steps:
subplots setup
implement slider
add slider dependent plot
add labels for initial plots
implement statistical functions, plot one by one
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from simStatePure import State

# Parameter
FILE = "./example_logs/test.json"

# interface with logs
def get_data():
    # returns [State], in validated time order. validation from simStatePure
    s0 = State(FILE)
    max_time = s0.max_time
    states = []
    for i in range(0, max_time+1):
        s = State(FILE)
        s.load(i)
        states.append(s)
    return states

# Global variables
STATES = get_data()
T = [state.time for state in STATES]
MAX_TIME = T[-1]

# statistical functions
def num_survivors(state):
    # it seems only agents in logs are surivors, which makes the conditional useless?
    return sum(1 for agent in state.agents if agent.inventory > 0)

# plotting utilities
class TimeKeeper:
    time = 0
    observers = [] # observer pattern for updating everything when time changes

    def update(time):
        TimeKeeper.time = round(time) # may get float time (e.g. from slider)
        for o in TimeKeeper.observers:
            o(TimeKeeper.time)

"""def add_time_slider(ax, slider_y=0.1):
    # shifts ax to accomodate bottom time slider, returns slider
    slider_ax = pass
    slider = Slider(slider_ax, 'Time', 0, MAX_TIME, valinit=0, valstep=)
    return slider"""

# individual plots
def plot_1(ax):
    # Proportion of surviving agents / time
    initial_population = num_survivors(STATES[0])
    prop = [num_survivors(s) / initial_population for s in STATES]
    ax.plot(T, prop)

# commands that get run
if __name__ == "__main__":
    fig = plt.figure()
    ax = plt.axes()
    plot_1(ax)
    plt.show()
