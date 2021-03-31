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

"""This package contains a scaffold of a model."""

from aea.skills.base import Model

from gdp.agent_aea.protocols.agent_environment.custom_types import Command


class BasicStrategy(Model):
    """
    This class defines the strategy for the agent
    Generic Strategy is to gather agent water amount before making a decision
    """
    tile_water = None
    agent_water = None
    neighbour_id = None
    neighbour_water_amount = None
    # neighbour_id and neighbour_water_amount will be list of the same length.
    # amount of water neighbour_id[n] has = neighbour_water_amount[n]
    # If unknown, = None
    round_no = None
    is_round_done = False
    agent_messages_returned_waiting_for_response = []  # Storing any messages of future round
    agent_message_asking_for_my_water = []  # Storing any messages of future round
    env_messages_waiting_for_response = []  # Storing any messages of future round

    def receive_agent_env_info(self, tile_water, agent_water, neighbours_id, round_no) -> bool:
        # Assert correct round and ready to accept
        if self.round_done and self.round_no == round_no - 1:
            self.tile_water = tile_water
            self.agent_water = agent_water
            self.neighbour_id = list(neighbours_id)
            self.round_no = round_no
            self.neighbour_water_amount = [None for _ in range(len(neighbours_id))]
            return True
        # Not correct round. Save info for later
        # INVARIANT: env_messages_waiting has to be earliest round first.
        else:
            self.env_messages_waiting_for_response.append(
                (tile_water, agent_water, neighbours_id, round_no)
            )
            return False

    def receive_agent_agent_info(self, water_info, sender_id, round_no) -> bool:
        # Assert correct round
        if self.round_no == round_no:
            if self.round_done:
                return False
            else:
                # Use info
                self.save_other_agent_water_info(water_info, sender_id, round_no)
                return True
        elif self.round_no > round_no:
            # PREVIOUS ROUND INTEL, DISCARD
            return False
        elif self.round_no < round_no:
            # FUTURE ROUND INTEL, SAVE
            self.agent_messages_returned_waiting_for_response.append(
                (water_info, sender_id, round_no)
            )
            return False

    def return_self_water_info(self):
        raise NotImplementedError

    def make_decision(self) -> [int, Command, int, int]:
        # either ask for water info or return decision of action for this turn
        # neighbour_id = None if decide to return action to environment agent
        # command, water_quantity = None if decide to ask for water info
        # ******************************************************************************************
        # Current decision method:
        # Get all neighbour water info, calculate average with self and offer/request the difference
        # ******************************************************************************************
        enough_found = self.enough_found
        if enough_found:
            return self.decide_what_to_return_to_env_agent
        else:
            return self.decide_what_info_to_search_for

    def enough_found(self) -> bool:
        # Has enough info been received for decision making?
        return not any(elem is None for elem in self.neighbour_water_amount)

    def decide_what_to_return_to_env_agent(self) -> [int, Command, int, int]:
        average = sum(self.neighbour_water_amount)/len(self.neighbour_id)
        difference_with_self = self.agent_water - int(average)  # average is over_estimated if not whole number
        if difference_with_self > 0:
            # Offer water
            return[None, "Offer", difference_with_self, self.round_no]
        elif difference_with_self == 0:
            # Idle
            return[None, "Idle", difference_with_self, self.round_no]
        else:
            # Request water
            return[None, "Request", difference_with_self, self.round_no]

    def decide_what_info_to_search_for(self) -> [int, Command, int, int]:
        # find a None in the list
        return[self.neighbour_id[self.neighbour_water_amount.index(None)], None, None, self.round_no]

    def save_other_agent_water_info(self, water_info, sender_id, round_no) -> None:
        assert self.round_no == round_no
        self.neighbour_water_amount[self.neighbour_id.index(sender_id)] = water_info

    def round_done(self) -> None:
        assert(not self.round_done)
        self.is_round_done = True

    def next_round_start(self) -> None:
        assert self.round_done
        self.is_round_done = False
        self.round_no += 1

    # not used rn
    def is_there_env_messages_waiting(self) -> bool:
        return len(self.env_messages_waiting_for_response) > 0

    # not used rn
    def find_env_message_to_be_handled(self) -> None:
        head, *tail = self.env_messages_waiting_for_response
        self.env_messages_waiting_for_response = tail
        return head

    def clear_water_query(self) -> (list[int], int):
        # second int = water rn, send to everyone in list[int]
        raise NotImplementedError
