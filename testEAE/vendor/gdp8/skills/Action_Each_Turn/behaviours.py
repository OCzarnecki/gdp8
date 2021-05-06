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
    TODO: log events throughout the phase of the simulation
    TODO: connection setup with all agents
"""

from aea.skills.base import Behaviour
from typing import Any, Optional, cast

from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.tac_control.dialogues import (
    OefSearchDialogues,
)

from gdp.env_aea.skills.Action_Each_Turn.environment import Environment, Phase
from gdp.agent_aea.protocols.agent_environment.message import AgentEnvironmentMessage
from gdp.agent_aea.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues
from gdp.env_aea.skills.Action_Each_Turn.replay_logger import ReplayLogger


class EnvironmentLogicBehaviour(TickerBehaviour):
    """Each turn of the simulation, this behaviour:
        - collects data from the environment for tick messages
        - sends tick messages to all agents with correct info
        - notifies the environment when it's ok to move to next turn of the simulation
   """

    def __init__(self, **kwargs: Any):
        """Instantiate the behaviour."""
        super().__init__(**kwargs) ## why ??
        self._replay_logger = ReplayLogger()

    def setup(self) -> None:
        """
        Implement the setup.
        :return: None
        """

    def act(self) -> None:
        """
        Implement the act. Actions depending on the phase of the simulation
        (can add a time constraint).

        :return: None
        """
        environment = cast(Environment, self.context.environment)

        if (
            environment.phase.value == Phase.PRE_SIMULATION.value
        ):
            environment.phase = Phase.SIMULATION_REGISTRATION
            self._register_env()
            self.context.logger.info(
                "Environment open for registration" ##until: {}".format(parameters.start_time)
            )
        elif (
            environment.phase.value == Phase.SIMULATION_REGISTRATION.value
        ):
            # should have a list of all agents and their address at the end of this phase
            if environment.registration.nb_agents < environment.nb_agents:######## WHERE IS THE NUMBER OF AGENT THAT WE WANT STORED ?
                #wait
                return
            ##elif registration delay expired : cancel simulation
            else:
                ##environment.create()## do we need to generate a simulation ? 
                self._unregister_env()
                # tell the env that the simulation starts?
                environment.phase = Phase.START_SIMULATION
        elif (
            environment.phase.value == Phase.START_SIMULATION.value
        ):
            # Set up simulation logging
            self._replay_logger.initialize(environment.state)
            # Log initial state
            self._replay_logger.log_state(environment.state)
            environment.phase = Phase.START_NEXT_SIMULATION_TURN

        elif (
            environment.phase.value == Phase.START_NEXT_SIMULATION_TURN.value
        ):
            environment.phase = Phase.COLLECTING_AGENTS_REPLY
            self._send_tick_messages(environment)

        elif (
            environment.phase.value == Phase.COLLECTING_AGENTS_REPLY.value
        ):
            if environment.agents_reply_received:  
                environment.phase = Phase.AGENTS_REPLY_RECEIVED
            #elif after_some_time_contraint:
            #   environment.remove_dead_agents() # agents are considered dead if they haven't replied after a delay
            #   environment.phase = Phase.AGENTS_REPLY_RECEIVED

                environment.phase = Phase.START_NEXT_SIMULATION_TURN
                environment.start_next_simulation_turn()
                self._replay_logger.log_state(environment.state)

        elif (
            environment.phase.value == Phase.SIMULATION_CANCELLED.value
        ):
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
        raise NotImplementedError


    def _register_env(self) -> None:
        """
        Register on the OEF as an Environment agent.
        :return: None.
        """
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("registering Environment model on SOEF.")
        
    def _unregister_env(self) -> None:
        """
        Unregister from the OEF as an environment agent.
        :return: None.
        """
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering Environment model from SOEF.")

    def _cancel_simulation(self, environment: Environment) -> None:
        """Notify agents that the simulation is cancelled."""
        self.context.logger.info("notifying agents that the simulation is cancelled.")

        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        for agent_address in environment.registration.agent_addr_to_name.keys():##
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
            or environment.phase == Phase.AGENTS_REPLY_RECEIVED):##indentation error possible
            self.context.is_active = False ## when was it set to true ?


    def _send_tick_messages(self, environment: Environment) -> None:
        """Collects data from the env and sends tick messages to all agents alive for current turn of simulation."""

        turn_number = environment.turn_number
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        
        for agent_address in environment.agents_alive:

            tile_water = environment.water_content(agent_address)
            agent_water = environment.agent_water(agent_address)
            neighbours_id = environment.neighbour_ids(agent_address)
            """
            _tac_dialogues = tac_dialogues.get_dialogues_with_counterparty(
                agent_address
            )
            if len(_tac_dialogues) != 1:
                raise ValueError("Error when retrieving dialogue.")
            tac_dialogue = _tac_dialogues[0]
            last_msg = tac_dialogue.last_message
            if last_msg is None:
                raise ValueError("Error when retrieving last message.")
            tac_msg = tac_dialogue.reply("""## we can do something similar as this if the dialogue below doesn't work

            tick_msg = agent_environment_dialogues.create(
                #dialogue_reference=???,
                #message_id=???,
                #target_message=???,
                counterparty=agent_address,##
                performative=AgentEnvironmentMessage.Performative.TICK,
                tile_water=tile_water,
                turn_number=turn_number,
                agent_water=agent_water,
                neighbours_id=neighbours_id,
            )
            self.context.outbox.put_message(message=tick_msg)