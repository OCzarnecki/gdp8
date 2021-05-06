# README #
This software allows the simulation, visualisation and analysis of emergent behaviour in complex systems. It simulates agents scavenging a desert for water, while using different simple local-knowledge strategies to keep the whole group alive as long as possible.

The project uses and showcases the Autonomous Economic Agent framework, developed by fetch.ai.

The authors are Blanche Duron, Chun Chang, Olaf Czarnecki, Kevin Xin, Tancrede Guillou and Ye Teng as part of the Oxford group design practical. We thank David Minarsch and Ali Hosseini at fetch.ai for their invaluable support during the development process.

Note that this project was developed on a limited time scale, and is not under active development. Note also that the work is entirely our own, and is not officially endorsed by fetch.ai.

# Installation
1. Clone this repository.
2. Install the AEA framework, by following the [AEA Framework Installation Instructions](https://docs.fetch.ai/aea/quickstart/#option-2-automated-install-script).
3. Install the required python dependencies
  * numpy
  * pygame
  * matplotlib

# Running
You can run the software simply by executing the `simulation` python script. It supports three subcommands `run`, `play-replay`, and `show-stats`.

## simulation run
Runs the simulation. For a full list of the configurable parameters, try
`./simulation run --help`
For a quick start, try
`./simulation run 5 "Explorer Dogs"`
which will start the simulation with default parameters, and five agents, each using the "Explorer Dog" strategy.

## simulation play-replay
Visualise the behaviour and status of agents in the simulation over time. This is done by reading in a log file, created in the `logs/` directory by `simulation run`. To visualise the results of the most recent simulation, run
`./simulation play-replay`
You can also specify a different log file using the `--logfile PATH` parameter.

## simulation stats
Prints statistics about a simulation run, using a log file.
`./simulation stats`
will use the most recent log file, but as with `play-replay` you can provide any valid log file using `--logfile PATH`.

# Building
The launcher script does not run the code from `env_aea` and `agent_aea` directly. Instead, it uses the snapshot of the code stored in the `packages` folder (the local registry). To push your current work into the package registry, run the `update_packages` script. For more info, check out docs.fetch.ai.

After the packages have been pushed, your changes should be applied immedietly, when running the `simulation` script.

# Architecture
See docs/ folder.

# Testing
From the root directory run
```
python -m unittest
```
This will autodiscover all tests in the `tests` subdirectory, as long as
* all test classes are importable from the project root
* all files containing test classes start with `test_`
* all test methods start with `test_`

