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

from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage
from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue


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
    # neighbour_water_amount are list of twos of agent_id and their info which = "Unknown" initially,
    # = "Asking" if a message has been sent to ask
    current_env_message = None
    current_env_dialogue = None
    round_no = -1
    is_round_done = True
    agent_messages_returned_waiting_for_response = []  # Storing any messages of future round
    agent_message_asking_for_my_water = []  # Storing any messages of future round

    def receive_agent_env_info(self, agent_environment_message: AgentEnvironmentMessage,
                               agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        # ENV messages should only be allowed to arrive when last round is done and should forever be
        # coming in the right sequence (1 then 2 then 3...)
        # Assert correct round and ready to accept
        # Assert last round done
        assert agent_environment_message.turn_number == self.round_no + 1
        assert self.is_round_done
        self.round_no += 1
        self.current_env_message = agent_environment_message
        self.current_env_dialogue = agent_environment_dialogue
        self.tile_water = agent_environment_message.tile_water
        self.agent_water = agent_environment_message.agent_water
        self.neighbour_id = list(agent_environment_message.neighbour_ids)
        self.neighbour_water_amount = [[i, "Unknown"] for i in self.neighbour_id]
        self.is_round_done = False

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:
        # If round number is of prev round. discard
        # If round number is of future round. something is wrong cuz you should not be able to
        # request anything
        assert self.round_no >= agent_agent_message.turn_number
        if self.round_no == agent_agent_message.turn_number:
            if not self.is_round_done:
                # Use info
                index = self.neighbour_water_amount.index([agent_agent_message.target, "Asking"])
                self.neighbour_water_amount[index] = [agent_agent_message.target, agent_agent_message.water]

    def deal_with_an_agent_asking_for_water_info(self) -> bool:
        # Return true if a request was dealt with, return false if there were no request dealt with
        if not self.agent_message_asking_for_my_water:
            # no request
            return False
        else:
            # there is request, test round no, deal with it if correct
            request, *self.agent_message_asking_for_my_water = self.agent_message_asking_for_my_water
            [message_, dialogue_] = request
            message = cast(AgentAgentMessage, message_)
            dialogue = cast(AgentAgentDialogue, dialogue_)
            if message.turn_number == self.round_no:
                return_message = dialogue.reply(
                    performative=AgentAgentMessage.Performative.WATER_STATUS,
                    target_message=message,
                    water_status=self.agent_water,
                )
                self.context.outbox.put_message(message=return_message)
                return True
            else:
                self.agent_message_asking_for_my_water.append(request)
                return False

    def enough_info_to_make_decision(self) -> bool:
        # currently, ALL neighbour info asked before making decision
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown" or i[1] == "Asking":
                return False
        return True

    def potentially_ask_for_info(self) -> bool:
        # currently, ALL info has to be asked for
        # return true if a message asking for water is sent
        # false otherwise
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown":
                i[1] = "Asking"
                agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)
                # message sent to another agent
                # agent_agent_message, _ = agent_agent_dialogues.create(
                #     counterparty=?????,
                #     performative=AgentAgentMessage.Performative.??????,
                #     ledger_id=strategy.ledger_id,
                #     address=cast(str, self.context.agent_addresses.get(strategy.ledger_id)),
                # )
                # self.outbox.
                send_agent_agent_message, _ = agent_agent_dialogues.create(
                    counterparty=i[0],
                    performative=AgentAgentMessage.Performative.REQUEST_INFO,
                    turn_number=self.round_no,
                )
                self.context.outbox.put_message(message=send_agent_agent_message)
                return True
        return False

    def make_decision_send_to_env(self) -> None:
        # pre: info enough to make decision
        # ******************************************************************************************
        # Current decision method:
        # Get all neighbour water info, calculate average with self and offer/request the difference
        # ******************************************************************************************
        sum_of_all_agents = self.agent_water
        for i in self.neighbour_water_amount:
            sum_of_all_agents += i[1]
        average = (sum_of_all_agents + self.agent_water) / (len(self.neighbour_water_amount) + 1)
        difference = int(self.agent_water - average)
        # difference > 0 => offer water, vice versa, difference ALWAYS underestimated if not accurate
        if difference > 0:
            decision: str = "send_water" + "." + str(difference)
        elif difference == 0:
            decision: str = "NULL"
        else:  # difference > 0
            decision: str = "receive_water" + "." + str(-difference)
        return_agent_env_message = self.current_env_dialogue.reply(
            performative=AgentEnvironmentMessage.Performative.ACTION,
            target_message=self.current_env_message,
            command=decision,
            turn_number=self.round_no
        )
        self.context.outbox.put_message(message=return_agent_env_message)
        self.is_round_done = True

    '''
    def return_self_water_info(self):
        raise NotImplementedError

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
    '''
