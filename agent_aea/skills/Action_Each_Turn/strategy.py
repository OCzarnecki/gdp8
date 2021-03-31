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

"""This model is a "intermediate" for the handler to place stuff and behaviour to read and make decisions"""
from typing import cast

from aea.skills.base import Model

from gdp.agent_aea.protocols.agent_agent import AgentAgentMessage
from gdp.agent_aea.protocols.agent_environment.custom_types import Command


# Next round env message SHOULD NEVER be able to come when is_round_done = false.
# ALL messages sent has to be replied before making a decision (for now)


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
    current_env_message = None
    current_env_dialogue = None
    round_no = 0
    is_round_done = False
    agent_messages_returned_waiting_for_response = []  # Storing any messages of future round
    agent_message_asking_for_my_water = []  # Storing any messages of future round

    def receive_agent_env_info(self, agent_environment_message, agent_environment_dialogue) -> None:
        # ENV messages should only be allowed to arrive when last round is done and should forever be
        # coming in the right sequence (1 then 2 then 3...)
        # Assert correct round and ready to accept
        assert (agent_environment_message.round_no == self.round_no + 1)
        self.round_no += 1
        self.current_env_message = agent_environment_message
        self.current_env_dialogue = agent_environment_dialogue
        self.tile_water = agent_environment_message.tile_water
        self.agent_water = agent_environment_message.agent_water
        self.neighbour_id = list(agent_environment_message.neighbour_ids)
        self.neighbour_water_amount = [[i, None] for i in self.neighbour_id]

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:
        assert self.round_no == agent_agent_message.round_no
        message = cast(AgentAgentMessage, agent_agent_message)
        if not self.round_done:
            # Use info
            index = self.neighbour_water_amount.index([agent_agent_message.target, None])
            self.neighbour_water_amount[index] = [agent_agent_message.target, agent_agent_message.water]









# ------------------------------------------------------------------------------------------------
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
        average = sum(self.neighbour_water_amount) / len(self.neighbour_id)
        difference_with_self = self.agent_water - int(average)  # average is over_estimated if not whole number
        if difference_with_self > 0:
            # Offer water
            return [None, "Offer", difference_with_self, self.round_no]
        elif difference_with_self == 0:
            # Idle
            return [None, "Idle", difference_with_self, self.round_no]
        else:
            # Request water
            return [None, "Request", difference_with_self, self.round_no]

    def decide_what_info_to_search_for(self) -> [int, Command, int, int]:
        # find a None in the list
        return [self.neighbour_id[self.neighbour_water_amount.index(None)], None, None, self.round_no]

    def save_other_agent_water_info(self, water_info, sender_id, round_no) -> None:
        assert self.round_no == round_no
        self.neighbour_water_amount[self.neighbour_id.index(sender_id)] = water_info

    def round_done(self) -> None:
        assert (not self.round_done)
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
