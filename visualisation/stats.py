"""
Next steps:
subplots setup √
implement slider √
add slider dependent plot √
add labels for initial plots √
implement statistical functions, plot one by one
Add message for when the statistic is no longer defined
Make discrete axes discrete

Proportion of surviving agents over time. √
Distribution of individual inventory over time. Slider √
Average water gathered per agent in single time step over time √ Need dehydration rate
Distribution of time since last drink over time. Slider √
Distribution of proportion of water received vs gathered. (can be calculated indirectly). Slider. Skip, I don't know how to calculate this
Distribution of distance to nearest agent. Slider √
Total water gathered in a single time step over time √ Need dehydration rate



"""
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib.widgets import Slider

from visualisation.simStatePure import State

# Parameter
FILE = "./visualisation/example_logs/test.json"

# interface with logs
def get_data():
    # returns [State], in validated time order. validation from simStatePure
    s0 = State(FILE)
    max_time = s0.max_time
    states = []
    for i in range(0, max_time+1):
        s = State(FILE)
        s.load(i)
        s.agents.sort(key=lambda x: x.id)
        #print([a.id for a in s.agents])
        states.append(s)
    return states

# Global variables (initialized in main)
STATES = None
T = None
MAX_TIME = None

# statistical functions
def num_survivors(state):
    # it seems only agents in logs are surivors, which makes the conditional useless?
    return sum(1 for agent in state.agents if agent.inventory > 0)

# plotting utilities
class TimeKeeper:
    time = 0
    observers = [] # observer pattern for updating everything when time changes

    def update(time):

        TimeKeeper.time = int(round(time)) # may get float time (e.g. from slider)
        #print("new time: {}".format(TimeKeeper.time))
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
    ax.set_title("Proportion of Surviving Agents", fontsize=7)
    ax.set_ylabel("Proportion")
    ax.set_xlabel("Time")
    ax.plot(T, prop)


def plot_2(ax):
    # only ever called once
    # Distribution of individual inventory over time

    def update_plot_2(t):
        ax.cla()
        ax.set_title("Distribution of Agent Inventory", fontsize=7)
        ax.set_xlabel("Inventory")
        ax.set_ylabel("Count")
        state = STATES[t]
        waters = [agent.inventory for agent in state.agents]
        ax.hist(waters, range=(0, state.max_inventory))
    TimeKeeper.observers.append(update_plot_2)
    update_plot_2(0)

def plot_3(ax):
    # Average water gathered per agent in single time step over time
    # time t to t+1
    averages = []
    times = range(0, MAX_TIME)
    for t in times: #TODO: know about dehydration rate
        s0 = STATES[t]
        s1 = STATES[t+1]
        diffs = []
        i = 0
        end = len(s1.agents)
        #print(len(s0.agents), len(s1.agents))
        for a in s0.agents:
            #print(a.id)
            while i != end and a.id != s1.agents[i].id: # agents sorted by id
                #diffs.append(0)
                #print(a.id, s1.agents[i].id)
                i += 1
            #print('\n')
            # does not know about dehydration rate
            if i == end:
                break
            else:
                b = s1.agents[i]
                diffs.append(max(0, b.inventory - a.inventory))
        average = np.mean(diffs)
        averages.append(average)

    ax.set_title("Average water gathered", fontsize=7)
    ax.set_ylabel("Water")
    ax.set_xlabel("Time")
    ax.plot(times, averages)

def plot_4(ax):

    def update_plot_4(t):
        ax.cla()
        ax.set_title("Distribution of Time Since Last Drink", fontsize=7)
        ax.set_xlabel("Time")
        ax.set_ylabel("Count")

        state = STATES[t]
        times = []
        # running time, where n=len(state.agents)
        # O(nnt), may be a bottleneck
        for a in state.agents:
            time = t
            found = False
            while time > 0 and not found:
                # assuming all agents created at time 0
                b = 0
                found_b = False
                for agent in STATES[time].agents:
                    if agent.id == a.id:
                        b = agent
                        found_b = True
                        break
                assert(found_b)

                # basically repeat of above code, a clever swap can do it
                c = 0
                found_c = False
                for agent in STATES[time-1].agents:
                    if agent.id == b.id:
                        c = agent
                        found_c = True
                        break
                assert(found_c)

                if c.inventory <= b.inventory:
                    times.append(t-time)
                    found = True
                time -= 1
            if not found:
                times.append(t)

        ax.hist(times, range=(0, t+1))
    TimeKeeper.observers.append(update_plot_4)
    update_plot_4(0)

def plot_5(ax):

    def update_plot_5(t):
        ax.cla()
        ax.set_title("Distribution of Distance to Nearest Agent", fontsize=7)
        ax.set_xlabel("Distance")
        ax.set_ylabel("Count")
        state = STATES[t]
        agents = state.agents

        distances = []
        def dist(a, b):
            # d_1 metric
            return abs(a.x - b.x) + abs(a.y - b.y)
        if len(agents) > 1:
            for a in agents:
                d = max(dist(a, b) for b in agents)
                for b in agents:
                    if a.id != b.id:
                        d = min(d, dist(a, b))
                distances.append(d)

        ax.hist(distances)
    TimeKeeper.observers.append(update_plot_5)
    update_plot_5(0)

def plot_6(ax):
    # Need dehydration rate
    ax.set_title("Total Water Gathered", fontsize=7)
    ax.set_xlabel("Time")
    ax.set_ylabel("Water")

    totals = []
    times = range(0, MAX_TIME)
    for t in times:
        s0 = STATES[t]
        s1 = STATES[t+1]
        def total_inv(s): return sum(a.inventory for a in s.agents)
        total = total_inv(s1) - total_inv(s0)
        totals.append(total)

    ax.plot(times, totals)

def main(log_path):
    global FILE
    FILE = log_path
    global STATES
    STATES = get_data()
    global T
    T = [state.time for state in STATES]
    global MAX_TIME
    MAX_TIME = T[-1]

    fig, axes = plt.subplots(2, 4, figsize=(8, 6))
    fig.canvas.set_window_title('AEA Simulation Statistics')
    #fig.tight_layout(pad=1,h_pad=1,w_pad=1) # make things overlap less
    fig.tight_layout(pad=3)
    #plt.rcParams['font.size'] = 8 # small font
    plt.subplots_adjust(bottom=0.25)
    slider_ax = plt.axes([0.15, 0.1, 0.7, 0.03])
    slider = Slider(slider_ax, 'Time', 0, MAX_TIME, valinit=0, valstep=1, valfmt='%0.0f') # format is to display integers
    slider.on_changed(TimeKeeper.update)

    axes = [i for j in axes for i in j]
    #print(axes)
    plot_funcs = [plot_1, plot_2, plot_3, plot_4, plot_5, plot_6]
    for ax, f in zip(axes, plot_funcs):
        f(ax)

    plt.show()

def run_cli():
    if len(sys.argv) != 2:
        print(f"No file specified. Using default: {FILE}")
        print("Run with --help to print usage")
        main(FILE)
    elif sys.argv[1] in ["-h", "--help"]:
        print("Usage: python stats.py LOG_FILE_PATH")
        return
    else:
        main(sys.argv[1])

# commands that get run
if __name__ == "__main__":
    run_cli()
