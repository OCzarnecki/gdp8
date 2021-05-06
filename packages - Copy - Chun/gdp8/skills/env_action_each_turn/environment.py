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

"""

from aea.skills.base import Model
# from aea.common import Address
# from aea.helpers.search.generic import (
#    AGENT_LOCATION_MODEL,
#    AGENT_REMOVE_SERVICE_MODEL,
#    AGENT_SET_SERVICE_MODEL,
# )
# Causes syntax error
# from aea.helpers.search.models import

from packages.gdp8.skills.env_action_each_turn.address_mapping import AddressMapping

from enum import Enum, auto
from itertools import product
from typing import Any
# from typing import List, Optional, cast, Dict

import random


class Phase(Enum):
    """This class defines the phases of the simulation."""

    PRE_SIMULATION = "pre_simulation"
    START_SIMULATION = "start_simulation"
    START_NEXT_SIMULATION_TURN = "start_next_simulation_turn"
    COLLECTING_AGENTS_REPLY = "collecting_agents_reply"
    AGENTS_REPLY_RECEIVED = "agents_reply_received"
    SIMULATION_CANCELLED = "simulation_cancelled"


class CommandType(Enum):
    """ Enum of possible types of command """
    OFFER_WATER = auto()
    REQUEST_WATER = auto()
    MOVE = auto()
    IDLE = auto()


class Command:
    """ Abstract superclass of all command objects"""

    def __init__(self, command_type):
        self.command_type = command_type


class OfferWaterCommand(Command):
    def __init__(self, quantity):
        super().__init__(CommandType.OFFER_WATER)
        self.quantity = quantity


class ReceiveWaterCommand(Command):
    def __init__(self, quantity):
        super().__init__(CommandType.REQUEST_WATER)
        self.quantity = quantity


class MoveCommand(Command):
    def __init__(self, direction):
        super().__init__(CommandType.MOVE)
        self.direction = direction


class IdleCommand(Command):
    def __init__(self):
        super().__init__(CommandType.IDLE)


class Agent:
    """ Representation of the properties an agent has in the
        environment. Does not include framework properties like
        addresses etc. """

    def __init__(self, agent_id, initial_water, pos_x, pos_y):
        self.agent_id = agent_id
        self.water = initial_water
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.movement_last_turn = None
        self.queue_command(None)

    def queue_command(self, command):
        """ Set the command that the agent wants to execute this
            turn. Overwrites previous commands. Must be one of
            the command objects defined above, deriving Command. 
        """
        if command is None:
            command = IdleCommand()
        self.next_command = command


class SimulationState:
    """ Captures the entire state of the simulation at a given
        time, and implements methods for querying and modifying
        it. """

    def __init__(self,
                 size_x,
                 size_y,
                 initial_oasis_water,
                 oasis_count,
                 agent_count,
                 initial_agent_water,
                 agent_mining_speed,
                 agent_max_capacity):
        self.size_x = size_x  # Width of cell grid
        self.size_y = size_y  # Height of cell grid
        self._initial_oasis_water = initial_oasis_water
        self._agent_mining_speed = agent_mining_speed
        self._agent_max_capacity = agent_max_capacity
        self._generate_water(initial_oasis_water, oasis_count)
        self._init_agents(agent_count, initial_agent_water)
        self.turn_number = 0
        # Allocate datastructures used in update_simulation once
        self._needs = [[0] * size_y for _ in range(size_x)]
        self._transfers = [[0] * size_y for _ in range(size_x)]

    def get_agent_by_id(self, agent_id):
        """ Retrieve agent by agent id. Crash and burn if
            invalid. """
        return self._agents_by_id[agent_id]

    def get_agent_by_pos(self, x, y):
        """ Returns the agent at grid position (x, y) or None if
            the grid cell is empty. Coords must be within range.
            """
        return self._agent_grid[x][y]

    def get_cell_water(self, x, y):
        """ Return the current water contents of a grid cell. """
        return self._water[x][y]

    def get_agents_alive(self):
        """ Return a list of all agents that are currently alive.
            """
        return [agent for agent in self._agents_by_id if agent.water > 0]

    def update_simulation(self):
        """ Advance the simulation by one turn, and prepare data
            for the next one. """
        self.turn_number += 1
        self._transfer_water()
        self._move_agents()
        for agent in self._agents_by_id:
            # Charge water cost
            agent.water = max(agent.water - 1, 0)  # an agent could already have given all water away :(
            # Clear command
            agent.queue_command(None)
            if (agent.water <= 0
                    and self.get_agent_by_pos(agent.pos_x, agent.pos_y) == agent):
                self._agent_grid[agent.pos_x][agent.pos_y] = None

    def get_header_object(self):
        """ Returns an object with the simulation configuration, for
            creating the log for visualisation. """
        return {
            "x_size": self.size_x,
            "y_size": self.size_y,
            "max_water_capacity_cell": self._initial_oasis_water,
            "max_water_capacity_agent": self._agent_max_capacity
        }

    def serialize_current(self):
        """ Returns the entire current simulation state, in the
            format for visualisation. """
        return {
            "tick_number": self.turn_number,
            "agents": [
                {
                    "x": agent.pos_x,
                    "y": agent.pos_y,
                    "inventory": agent.water,
                    "id": agent.agent_id
                } for agent in self.get_agents_alive()],
            "cells": [
                {
                    "x": x,
                    "y": y,
                    "water": self.get_cell_water(x, y)
                } for x in range(self.size_x)
                for y in range(self.size_y)]
        }

    def _move_agents(self):
        """
        Update position of all agents that wanted to move. 
        If the position is already taken, the action will be discarded.
        The world is "round", if you reach the top and move up you go back to the bottom.

        """
        for agent in self.get_agents_alive():
            if agent.next_command.command_type == CommandType.MOVE:
                direction = agent.next_command.direction
                if direction == "north":
                    self._try_moving(agent, direction, agent.pos_x, agent.pos_y - 1, agent.pos_x, agent.pos_y)
                elif direction == "south":
                    self._try_moving(agent, direction, agent.pos_x, agent.pos_y + 1, agent.pos_x, agent.pos_y)
                elif direction == "west":
                    self._try_moving(agent, direction, agent.pos_x - 1, agent.pos_y, agent.pos_x, agent.pos_y)
                elif direction == "east":
                    self._try_moving(agent, direction, agent.pos_x + 1, agent.pos_y, agent.pos_x, agent.pos_y)
                else:
                    raise ValueError(
                        "Agent tried to move in a direction not recognised: '{}'".format(agent.next_command))
            else:
                agent.movement_last_turn = None

    def _try_moving(self, agent, direction, try_pos_x, try_pos_y, prev_pos_x, prev_pos_y):
        try_pos_x = try_pos_x % self.size_x
        try_pos_y = try_pos_y % self.size_y
        if self._agent_grid[try_pos_x][try_pos_y] is None:
            agent.pos_x = try_pos_x
            agent.pos_y = try_pos_y
            agent.movement_last_turn = direction
            self._agent_grid[try_pos_x][try_pos_y] = agent
            self._agent_grid[prev_pos_x][prev_pos_y] = None
        else:
            agent.movement_last_turn = None
        return

    def _transfer_water(self):
        """ Update the agents' water inventory by one turn. This
            includes both mining, and the resolution of transfers
            the agents make among themselves. If requests or
            offers for water are not consistent with each other,
            arbitrary tie-breaking will be applied. The details
            are not specified. In particular, there is no
            guarantee for optimality. """
        # Algorithm description:
        # Maintain needs for all cells. Needs are positive if the
        # agent at the cell requested water, negative if it
        # offered water, and 0 otherwise or if the cell does not
        # contain an agent. The needs are modified towards 0
        # while the algorithm is running.
        #
        # Also maintain transfers, indicating how much water
        # should be transferred to or from an agent after water
        # has been mined. The transfers are the output of the
        # algorithm.
        #
        # Iterate over all agents. If their needs are negative,
        # greedily try to meet negative needs of neighbours.
        # Adjust needs accordingly, and keep track of transfers
        # made. Make sure that the transfer satisfies all the
        # constraints (amounts offered, amounts requested, max
        # capacity, capacity that can be transferred).

        # Init data structures
        for x in range(self.size_x):
            for y in range(self.size_y):
                self._transfers[x][y] = 0
                agent = self.get_agent_by_pos(x, y)
                self._needs[x][y] = 0
                if agent is not None and agent.next_command is not None:
                    if agent.next_command.command_type == CommandType.REQUEST_WATER:
                        self._needs[x][y] = agent.next_command.quantity
                    elif agent.next_command.command_type == CommandType.OFFER_WATER:
                        self._needs[x][y] = -1 * min(agent.next_command.quantity,
                                                     agent.water + self._minable_at(x, y))
                    elif agent.next_command.command_type == CommandType.IDLE:
                        pass
        # Compute transfers
        agent_positions = [(agent.pos_x, agent.pos_y) for agent in self.get_agents_alive()]
        for agent in self.get_agents_alive():
            if agent is None:
                raise ValueError("agent is None")
            # else:
            #     print(str(agent.water) + "." + str(agent.pos_x) + "." + str(agent.pos_y) + "." + str(agent.agent_id))
        for (x, y) in agent_positions:
            # agent_test = self.get_agent_by_pos(x, y)
            # if agent_test is None:
            #     raise ValueError(
            #             str(x) + "." + str(y)
            #    )
            # Action is only needed for agents who send water
            if self._needs[x][y] < 0:
                agent = self.get_agent_by_pos(x, y)
                neighbour_coords = [((x + dx + self.size_x) % self.size_x, (y + dy + self.size_y) % self.size_y)
                                    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                for (dst_x, dst_y) in set(neighbour_coords):
                    dst_agent = self.get_agent_by_pos(dst_x, dst_y)
                    if dst_agent is not None and self._needs[dst_x][dst_y] > 0:
                        transfer_amount = min(self._agent_max_capacity
                                              - dst_agent.water
                                              - self._minable_at(dst_x, dst_y)
                                              + self._transfers[dst_x][dst_y],
                                              self._needs[dst_x][dst_y],
                                              -1 * self._needs[x][y],
                                              agent.water + self._minable_at(x, y) + self._transfers[x][y])
                        transfer_amount = max(transfer_amount, 0)
                        self._needs[x][y] += transfer_amount
                        self._needs[dst_x][dst_y] -= transfer_amount
                        self._transfers[x][y] -= transfer_amount
                        self._transfers[dst_x][dst_y] += transfer_amount

        # Apply transfers and mine water
        for (x, y) in agent_positions:
            agent = self.get_agent_by_pos(x, y)
            assert(agent is not None)
            # Mine water
            minable = self._minable_at(x, y)
            if minable > 0:
                to_mine = min(self._agent_max_capacity - agent.water, minable)
                self._water[x][y] -= to_mine
                agent.water += to_mine
            # Transfer water
            agent.water += self._transfers[x][y]

    def _minable_at(self, x, y):
        """ Determine how much an agent with enough spare
            capacity could mine at position (x, y). """
        return min(self._water[x][y], self._agent_mining_speed)

    def _generate_water(self, initial_oasis_water, oasis_count):
        """ Terrain generation. Populate the grid with water. """
        # Currently just uniformly distribute 1x1 oases.
        # Might do a Gaussian blur later for coolness and interest.
        self._water = [[0] * self.size_y for _ in range(self.size_x)]
        for (x, y) in self._unique_random_coords(oasis_count):
            self._water[x][y] = initial_oasis_water

    def _init_agents(self, agent_count, initial_agent_water):
        """ Initiate IDs and locations for agents. """
        # Distribute agents uniformly.
        current_id = 0
        self.agent_count = agent_count
        self._agents_by_id = []
        self._agent_grid: list[list[Agent]] = [[None] * self.size_y for _ in range(self.size_x)]

        for (x, y) in self._unique_random_coords(agent_count):
            agent = Agent(current_id, initial_agent_water, x, y)
            self._agents_by_id.append(agent)
            self._agent_grid[x][y] = agent
            current_id += 1

    def _unique_random_coords(self, count):
        """ Returns a list of `count` unique, uniformly distributed, random,
            integer coordinates, that lie within this simulations grid """
        possible_coords = list(product(range(self.size_x), range(self.size_y)))
        return random.sample(possible_coords, count)


class Environment(Model):
    """Model of the environment."""

    def __init__(self, **kwargs: Any) -> None:
        self._phase = Phase.START_SIMULATION
        self.state = SimulationState(
            kwargs['size_x'],
            kwargs['size_y'],
            kwargs['initial_oasis_water'],
            kwargs['oasis_count'],
            kwargs['agent_count'],
            kwargs['initial_agent_water'],
            kwargs['agent_mining_speed'],
            kwargs['agent_max_capacity']
        )
        self._agents_replied = set()
        super().__init__(**kwargs)

    def set_mapping(self, mapping: AddressMapping) -> None:
        """Set the mapping by which id<->address resolution
           will be done."""
        self._mapping = mapping

    @property
    def nb_agents(self) -> int:
        """Get the number of agents in the simulation."""
        return self.state.agent_count

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
        return self.state.turn_number

    def water_content(self, agent_address) -> int:
        """Get the water_content of the cell of the agent."""
        agent_id = self.address_to_id(agent_address)
        agent = self.state.get_agent_by_id(agent_id)
        return self.state.get_cell_water(agent.pos_x, agent.pos_y)

    def agent_water(self, agent_address) -> int:
        """Get the amount of water the agent has in its inventory."""
        agent_id = self.address_to_id(agent_address)
        return self.state.get_agent_by_id(agent_id).water

    def agent_movement(self, agent_address) -> str:
        """Get the direction in which the agent was moved last turn.
           one of "north", "east", "south", "west", or None if the
           agent didn't move."""
        agent_id = self.address_to_id(agent_address)
        return self.state.get_agent_by_id(agent_id).movement_last_turn

    def neighbours_nesw(self, agent_address):
        """Get the list of addresses of the agents neighbours.
           :return 4-tuple, where each element is either the
                   neighbouring agent address, or None if there
                   is no agent. The addresses are laid out like
                   this: (N, W, S, E), where N corresponds to the
                   address in the north etc."""
        agent = self.state.get_agent_by_id(self.address_to_id(agent_address))
        x, y = agent.pos_x, agent.pos_y
        size_x, size_y = self.state.size_x, self.state.size_y
        n, e, s, w = None, None, None, None
        north_agent = self.state.get_agent_by_pos(x, (y - 1 + size_y) % size_y)
        if north_agent:
            n = self.id_to_address(north_agent.agent_id)
        east_agent = self.state.get_agent_by_pos((x + 1) % size_x, y)
        if east_agent:
            e = self.id_to_address(east_agent.agent_id)
        south_agent = self.state.get_agent_by_pos(x, (y + 1) % size_y)
        if south_agent:
            s = self.id_to_address(south_agent.agent_id)
        west_agent = self.state.get_agent_by_pos((x - 1 + size_x) % size_x, y)
        if west_agent:
            w = self.id_to_address(west_agent.agent_id)
        return n, e, s, w

    @property
    def agents_alive(self) -> list[Agent]:
        """Get a list of agents still alive in the simulation."""
        return [self.id_to_address(agent.agent_id) for agent in self.state.get_agents_alive()]
        # -> I actually prefer if we could return a similar dict as agent_addr_to_id

    @property
    def agents_reply_received(self) -> bool:
        """Get true if the env received a reply from all agents still alive this turn"""
        return len(self._agents_replied) == self.agents_alive.__len__()

    def remove_dead_agents(self) -> None:
        """Removes all agents who haven't replied this turn from the list of agents alive."""
        # Nothing to do, currently.
        pass

    def save_action(self, agent_address, action) -> None:
        """Saves the agent's action for this turn."""
        agent_id = self.address_to_id(agent_address)
        agent = self.state.get_agent_by_id(agent_id)
        self._agents_replied.add(agent_id)
        command = None
        if action == "NULL":
            command = IdleCommand()
        else:
            tokens = action.split(".")
            if len(tokens) == 0:
                self.context.logger.warning("got empty action string")

            elif tokens[0] == "offer_water":
                if len(tokens) != 2:
                    self.context.logger.warning("could not parse action string {}".format(action))
                else:
                    try:
                        command = OfferWaterCommand(int(tokens[1]))
                    except ValueError:
                        self.context.logger.warning("could not parse action string {}".format(action))

            elif tokens[0] == "receive_water":
                if len(tokens) != 2:
                    self.context.logger.warning("could not parse action string {}".format(action))
                else:
                    try:
                        command = ReceiveWaterCommand(int(tokens[1]))
                    except ValueError:
                        self.context.logger.warning("could not parse action string {}".format(action))

            elif tokens[0] == "move":
                if len(tokens) != 2:
                    self.context.logger.warning("could not parse action string {}".format(action))
                else:
                    try:
                        command = MoveCommand(tokens[1])
                    except ValueError:
                        self.context.logger.warning("could not parse action string {}".format(action))
            else:
                self.context.logger.warning("could not parse action string {}".format(action))
        agent.queue_command(command)

    def update_simulation(self) -> None:
        """Starts the next simulation turn."""
        self.state.update_simulation()
        self._agents_replied.clear()

    def end_simulation(self) -> None:
        """Cleanup."""
        # Nothing to do, currently.
        pass

    def address_to_id(self, agent_address):
        return self._mapping.get_id_from_address(agent_address)

    def id_to_address(self, agent_id):
        return self._mapping.get_address_from_id(agent_id)
