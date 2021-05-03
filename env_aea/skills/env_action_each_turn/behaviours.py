# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a behaviour for the environment. 
"""

from aea.skills.behaviours import TickerBehaviour
from typing import Any, Optional, cast

from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage

from packages.gdp8.skills.env_action_each_turn.environment import Environment, Phase
from packages.gdp8.skills.env_action_each_turn.address_mapping import AddressMapping
from packages.gdp8.skills.env_action_each_turn.replay_logger import ReplayLogger


class EnvironmentLogicBehaviour(TickerBehaviour):
    """Each turn of the simulation, this behaviour:
        - collects data from the environment for tick messages
        - sends tick messages to all agents with correct info
        - notifies the environment when it's ok to move to next turn of the simulation
   """

    def __init__(self, **kwargs: Any):
        """Instantiate the behaviour."""
        super().__init__(**kwargs) 
        self._mapping_path = kwargs['mapping_path']

    def setup(self) -> None:
        """
        Implement the setup.
        :return: None
        """
        self._replay_logger = ReplayLogger()

        environment = self.context.environment
        mapping = AddressMapping(
            self._mapping_path,
            environment.nb_agents
        )
        mapping.load()
        environment.set_mapping(mapping)

    def act(self) -> None:
        """
        Implement the act. Actions depending on the phase of the simulation
        (can add a time constraint).

        :return: None
        """
        environment = cast(Environment, self.context.environment)

        if (environment.phase.value == Phase.PRE_SIMULATION.value):
            # should have a list of all agents and their address at the end of this phase
            ##if nothing has to be done before the simulation this phase can be removed
            self.context.logger.info("Starting simulation")
            environment.phase = Phase.START_SIMULATION

        elif (environment.phase.value == Phase.START_SIMULATION.value):
            # Set up simulation logging
            self._replay_logger.initialize(environment.state)
            # Log initial state
            self._replay_logger.log_state(environment.state)
            environment.phase = Phase.START_NEXT_SIMULATION_TURN

        elif (environment.phase.value == Phase.START_NEXT_SIMULATION_TURN.value):
            environment.phase = Phase.COLLECTING_AGENTS_REPLY
            self._send_tick_messages(environment)
            self.context.logger.info("tick messages sent, waiting for replies")

        elif (environment.phase.value == Phase.COLLECTING_AGENTS_REPLY.value):
            if environment.agents_reply_received:
                environment.phase = Phase.AGENTS_REPLY_RECEIVED
                # elif after_some_time_contraint:
                #   environment.remove_dead_agents() # agents are considered dead if they haven't replied after a delay
                #   environment.phase = Phase.AGENTS_REPLY_RECEIVED

                environment.phase = Phase.START_NEXT_SIMULATION_TURN
                environment.update_simulation()
                self._replay_logger.log_state(environment.state)

        elif (environment.phase.value == Phase.SIMULATION_CANCELLED.value):
            ## the simulation has been canceled
            environment.end_simulation()
            self._cancel_simulation()
            ## save the env state
            ## kill all agents
            ## end simulation
            # -> Who does the above ? 
            return None
        else:
            ##there has been an issue, the env should be in one of those phases
            ## return phase of env
            return None

    def teardown(self) -> None:
        """
        Implement the task teardown.

        :return: None
        """

    def _cancel_simulation(self, environment: Environment) -> None:
        """Notify agents that the simulation is cancelled."""
        self.context.logger.info("notifying agents that the simulation is cancelled.")

        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        for agent_address in environment.registration.agent_addr_to_name.keys():  ##
            _agent_environment_dialogues = agent_environment_dialogues.get_dialogues_with_counterparty(
                agent_address
            )
            if len(_agent_environment_dialogues) != 1:
                raise ValueError("Error when retrieving dialogue.")
            agent_environment_dialogue = _agent_environment_dialogues[0]
            last_msg = agent_environment_dialogue.last_message
            if last_msg is None:  # pragma: nocover
                raise ValueError("Error when retrieving last message.")
            env_msg = agent_environment_dialogue.reply(
                performative=AgentEnvironmentMessage.Performative.CANCELLED,
            )
            self.context.outbox.put_message(message=env_msg)

        if (environment.phase == Phase.START_NEXT_SIMULATION_TURN
                or environment.phase == Phase.COLLECTING_AGENTS_REPLY
                or environment.phase == Phase.AGENTS_REPLY_RECEIVED):  ##indentation error possible
            self.context.is_active = False  ## when was it set to true ?

    def _send_tick_messages(self, environment: Environment) -> None:
        """Collects data from the env and sends tick messages to all agents alive for current turn of simulation."""
        if environment.agents_alive != [None]:
            self._send_to_all_agents(environment)
        else:
            self.context.logger.info(
                "Tick messages not sent, list of agents alive is: '{}'".format(environment.agents_alive))

    def _send_to_all_agents(self, environment):
        turn_number = environment.turn_number
        self.context.logger.info("Sending tick messages for turn number: '{}'".format(turn_number))
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)

        for agent_address in environment.agents_alive:
            tile_water = environment.water_content(agent_address)
            agent_water = environment.agent_water(agent_address)
            n, e, s, w = environment.neighbours_nesw(agent_address)
            agent_movement = environment.agent_movement(agent_address)

            tick_msg, _agent_environment_dialogue = agent_environment_dialogues.create(
                counterparty=agent_address,
                performative=AgentEnvironmentMessage.Performative.TICK,
                tile_water=tile_water,
                turn_number=turn_number,
                agent_water=agent_water,
                north_neighbour_id=n if n else "None",
                east_neighbour_id=e if e else "None",
                south_neighbour_id=s if s else "None",
                west_neighbour_id=w if w else "None",
                movement_last_turn=agent_movement if agent_movement else "None"
            )
            self.context.outbox.put_message(message=tick_msg)
