# Visualisation

Visualisation files are under `visualisation`.

## Main Visualisation (play-replay)

![Main Visualisation Diagram](/docs/mainVis_diagram.png?raw=true)

The visualisation module takes a simulation log, and displays a dynamic view of the agents behaviours and the real time state of the simulation.

It shows the following features:
1. Map filled with water pits whose size matches their quantity of water
2. Agents moving inside that map
3. Time of simulation and number of survivors
4. Speed of the simulation (x1, x2 or x10)
5. Play / Pause the simulation to look for precise agent stats

Keys that can be used to manipulate the visualisation:
1. RIGHT and LEFT keys increase / decrease the speed of the simulation
2. UP and DOWN keys bounce forward / back in the simulation (+/- 100 iterations)
3. SPACE bar pauses and resumes the simulation
4. While on pause, moving the mouse above an agent will display its remaining water and its ID

Two python files are used for main visualisation : `simulationState.py` and `main.py`. The first one is used to retrieve the data from the given json log file. It implements a `State` class which represents the state of the simulation at any given time. A state has a set of agents and their characteristics, a set of cells and their characteristics and other useful values (time, speed etc).

The `main.py` file is used to display the visualisation. It uses `pygame` library and works as follows :
1. At a frame of 60 FPS, runs a main loop
2. Depending on the given simulation speed, loads the new state in `simulationState.py`
3. Updates agents position
4. Draws the new positions on the screen

To implement agent movement, we retrieve the agent actual position as well as the position the agent will be in the next iteration (`desired_pos`). Using these two positions we can compute the direction in which the agent wants to move and compute a velocity and acceleration accordingly. This is all done with simple arithmetic and basic `math` and `numpy` methods.

## Statistics (show-stats)

![Statistics Diagram](/docs/stats_diagram.png?raw=true)

The statistics module takes a simulation log, and shows a series of graphs summarising the simulation. It includes statistics interesting for measuring individual survival, collective survival, and disparities between agents. It is intended to be used side by side with the main visualisation.

It currently shows the following 6 statistics:
1. Proportion of agents surviving / time
2. Distribution of agent inventory / time
3. Average water gathered per agent in a single time step / time (water gathered from time `t` to `t+1`)
4. Distribution of time since last drink
5. Distribution of distance to nearest agent
6. Cumulative water gathered by all agents / time

The module includes time-dependent graphs, which is controlled through the time slider.

On the technical side, the module shares the use of the `State` class with the main visualiser to read the simulation logs in an accessible format. It uses `simStatePure.py`, which is less specialised for live simulation compared to `simulationState.py`.

The module plots its graphs using `matplotlib`, and is organised so each statistic is abstracted into a single `plot_i` function. Each `plot_i` function takes an `Axes` object and plots onto it without knowing the location of the axes in the overall figure, so plots can be implemented in a modular way. All plot axes come from a single `pyplot.subplots` command, laying out the axes in a table.

The time dependent graphs are updated through an observer pattern implemented with the `TimeKeeper` object. When `plot_i` is called, a time dependent update function may be sent to `TimeKeeper` as an observer. When the time slider is updated, `TimeKeeper` calls all of its observers, updating all time dependent graphs.
