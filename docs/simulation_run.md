# Subsystem design: simulation run

The simulation runs via the AEA framework. Think of the agents as mars rovers, with sensors and actuators. The sensors allow it to perceive the ground underneath it, while its actuators (motors and drills) allow it to interact with the world.

The simulation is done by two classes of AEAs. Agent-AEAs are the mars rovers. They communicate with each other, trying to find a good strategy to survive. The environment AEA emulates the world. It sends messages which represent input to the sensors, and receives messages corresponding to actuators.

## Simulation goals
The goal of the agents is to survive as long as possible. The idea being that they are stranded on a desert, and use up one unit of water per unit of time. Spread around the desert are water sources. Agents can either mine water from underneath them, pass water to adjacent agents, or move around the desert. The goal is to survive as long as possible as a collective, not as an individual. This software provides a tool for exploring this problem, and tests out three different strategies for survival.

For details on the strategies, see the respective document in this directory.

## System design
Since this subsystem is implemented almost entirely in the AEA framework, a lot of the framework's language will be used here. For more information, please refer to the documentation at docs.fetch.ai. The simulation lifecycle proceeds in the following steps:
1. The `./simulation run` script accepts configuration parameters, and uses the Multi Agent Manager to pass those parameters to the environment's and the agents' skill configuration.
2. The Multi Agent Manager instantiates the required number of agent-AEAs and an Environment-AEA.
3. The Environment-AEA reads the agent's cryptographic addresses from `keys

TODO mention testing in passing
TODO remove testing from 
TODO individual contribution sheet
TODO no simulation demo
