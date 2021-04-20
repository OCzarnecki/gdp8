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
https://github.com/fetchai/agents-aea/blob/main/packages/fetchai/skills/tac_control/game.py

TODO @blanche: find solution for the register and unregister function: _remove_service_data and set_service_data


"""

from aea.skills.base import Model
from aea.common import Address
from aea.helpers.search.generic import (
    AGENT_LOCATION_MODEL,
    AGENT_REMOVE_SERVICE_MODEL,
    AGENT_SET_SERVICE_MODEL,
)
from aea.helpers.search.models import 


from typing import Any, Dict, List, Optional, cast
from enum import Enum

import agent_aea

class Phase(Enum):
    """This class defines the phases of the simulation."""

    PRE_SIMULATION = "pre_simulation"
    SIMULATION_REGISTRATION = "simulation_registration"
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
        ## The handler can also pass the whole message if you prefer
        raise NotImplementedError

    def start_next_simulation_turn(self) -> None:
        """Starts the next simulation turn."""
        # turn_number +=1
        # implement logic for the actions taken by the agents 
        raise NotImplementedError

    def end_simulation(self) -> None:
        """Is there anything particular to be done at the end of the simulation? save state of environment?..."""
        raise NotImplementedError


    ##########################FUNCTIONS NEEDED JSUT FOR THE AGENTS######### 
    ## they are stored in the participant/game.py for instance


    """def __init__(self, **kwargs: Any):
        """Instantiate the game class."""
        self._expected_controller_addr = kwargs.pop(
            "expected_controller_addr", None
        )  # type: Optional[str]

        self._search_query = kwargs.pop("search_query", DEFAULT_SEARCH_QUERY)
        if "search_value" not in self._search_query:  # pragma: nocover
            raise ValueError("search_value not found in search_query")
        self._expected_version_id = self._search_query["search_value"]
        location = kwargs.pop("location", DEFAULT_LOCATION)
        self._agent_location = Location(
            latitude=location["latitude"], longitude=location["longitude"]
        )
        self._radius = kwargs.pop("search_radius", DEFAULT_SEARCH_RADIUS)
        self._phase = Phase.PRE_GAME
"""

    def update_expected_controller_addr(self, controller_addr: Address) -> None:
        """
        Overwrite the expected controller address.
        :param controller_addr: the address of the controller
        :return: None
        """
        self.context.logger.warning(
            "TAKE CARE! Circumventing controller identity check! For added security provide the expected controller key as an argument to the Game instance and check against it."
        )
        self._expected_controller_addr = controller_addr

    
    def get_env_query(self) -> Query:
        """
        Get the query for the environment.
        :return: the query
        """
        close_to_my_service = Constraint(
            "location", ConstraintType("distance", (self._agent_location, self._radius))
        )
        service_key_filter = Constraint(
            self._search_query["search_key"],
            ConstraintType(
                self._search_query["constraint_type"],
                self._search_query["search_value"],
            ),
        )
        query = Query([close_to_my_service, service_key_filter],)
        return query

    def update_environment_phase(self, phase: Phase) -> None:
        raise NotImplementedError

    def update_expected_environment_addr(self, environment_addr: Address) -> None:
        raise NotImplementedError

    def get_environment_query(self) -> query:
        raise NotImplementedError
    
    def get_register_env_description(self) -> Description:
        """Get the env description for registering."""
        description = Description(
            self.context.parameters.set_service_data,## we don't have a Param class yet, need to figure out what this description is for and if we actually need it
            data_model=AGENT_SET_SERVICE_MODEL,
        )
        return description
    
    def get_unregister_env_description(self) -> Description:
        """Get the env description for unregistering."""
        description = Description(
            self.context.parameters.remove_service_data,##same issue as the register_env_description() above
            data_model=AGENT_REMOVE_SERVICE_MODEL,
        )
        return description
        ##############################################
