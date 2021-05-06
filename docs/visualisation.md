# Visualisation

Visualisation files are under `visualisation`.

## Main Visualisation (play-replay)

![Main Visualisation Diagram](https://github.com/OCzarnecki/gdp8/tree/master/docs/mainVis_diagram.png)

## Statistics (show-stats)

![Statistics Diagram](https://github.com/OCzarnecki/gdp8/tree/master/docs/stats_diagram.png)

The statistics module takes a simulation log, and shows a series of graphs summarising the simulation. It includes statistics interesting for measuring individual survival, collective survival, and disparities between agents. It is intended to be used side by side with the main visualisation.

It currently shows the following 6 statistics:
1. Proportion of agents surviving / time
2. Distribution of agent inventory / time
3. Average water gathered per agent in a single time step / time (water gathered from time `t` to `t+1`)
4. Distribution of time since last drink
5. Distribution of distance to nearest agent
6. Total water gathered by all agents / time

The module includes time-dependent graphs, which is controlled through the time slider.

On the technical side, the module shares the use of the `State` class with the main visualiser to read the simulation logs in an accessible format. It uses `simStatePure.py`, which is less specialised for live simulation compared to `simulationState.py`.

The module plots its graphs using `matplotlib`, and is organised so each statistic is abstracted into a single `plot_i` function. Each `plot_i` function takes an `Axes` object and plots onto it without knowing the location of the axes in the overall figure, so plots can be implemented in a modular way. All plot axes come from a single `pyplot.subplots` command, laying out the axes in a table.

The time dependent graphs are updated through an observer pattern implemented with the `TimeKeeper` object. When `plot_i` is called, a time dependent update function may be sent to `TimeKeeper` as an observer. When the time slider is updated, `TimeKeeper` calls all of its observers, updating all time dependent graphs.
