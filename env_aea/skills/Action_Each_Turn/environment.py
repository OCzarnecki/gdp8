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

"""This package contains a scaffold of a class modeling the environment.It is shared  
equally across the Handler, Behaviour and Task classes on the context level.
Some of the code is an adaptation of the model of a TAC game:
https://github.com/fetchai/agents-aea/blob/main/packages/fetchai/skills/tac_control/game.py"""

from aea.skills.base import Model
from aea.common import Address


from typing import Any, Dict, List, Optional, cast
from enum import Enum

import agent_aea

class Phase(Enum):
    """This class defines the phases of the simulation."""

    PRE_SIMULATION = "pre_simulation"
    SIMULATION_SETUP = "simulation_setup"
    START_SIMULATION = "start_simulation"
    START_NEXT_SIMULATION_TURN = "start_next_simulation_turn"
    COLLECTING_AGENTS_REPLY = "collecting_agents_reply"
    AGENTS_REPLY_RECEIVED = "agents_reply_received"
    SIMULATION_CANCELLED = "simulation_cancelled"

class Environment(Model): 
    """This class scaffolds a model of the environment."""

    def __init__(self, **kwargs: Any) -> None:

        self._phase = Phase.PRE_SIMULATION


    @property
    def phase(self) -> Phase:
        """Get the simulation phase."""
        return self._phase

    @phase.setter
    def phase(self, phase: Phase) -> None:
        """Set the simulation phase."""
        self.context.logger.debug("Simulation phase set to: {}".format(phase))
        self._phase = phase
    
    @property
    def turn_number(self) -> int:
        """Get the current turn number of the simulation."""
        raise NotImplementedError

    @property
    def water_content(self, agent_address) -> int:
        """Get the water_content of the cell of the agent."""
        raise NotImplementedError 
    
    @property
    def agent_water(self, agent_address) -> int:
        """Get the amount of water the agent has in its inventory."""
        raise NotImplementedError
    
    @property
    def neighbour_ids(self, agent_address) -> list(agent_address):
        """Get the list of addresses of the agents neighbours."""
        raise NotImplementedError

    @property
    def agents_alive(self) -> list(agent_aea):
        # actually doesn't really matter if it is a list(address) or list... What I need is a list with the 
        # address of all agents alive to send them the tick message
        """Get a list of agents still alive in the simulation."""
        raise NotImplementedError
    
    @property
    def agents_reply_received(self) -> bool:
        """Get true if the env received a reply from all agents still alive this turn"""
        raise NotImplementedError

    def remove_dead_agents(self) -> None:
        """Removes all agents who haven't replied this turn from the list of agents alive."""
        raise NotImplementedError

    def save_action(self, agent_adress, action, water_content) -> None:
        """Saves the agent's action for this turn."""
        raise NotImplementedError

    def start_next_simulation_turn(self) -> None:
        """Starts the next simulation turn."""
        # turn_number +=1
        # implement logic for the actions taken by the agents 
        raise NotImplementedError
