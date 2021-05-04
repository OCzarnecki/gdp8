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
import random
from typing import cast

from aea.skills.base import Model

from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage
from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue


# Next round env message SHOULD NEVER be able to come when is_round_done = false.
# ALL messages sent has to be replied before making a decision (for now)


class LoneGoldfishStrategy(Model):
    """
    The lone goldfish, like lone wolves but don't remember anything. 
    they ignore all communication, drink when they find water.
    Perform a uniform random walk to find water.
    """
    round_no = -1
    is_round_done = True
    current_env_dialogue = None
    current_env_message = None
    tile_water = None
    agent_water = None

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
        self.is_round_done = False

    def deal_with_an_agent_asking_for_water_info(self) -> bool:
        # the lone goldfish doesn't communicate with its neighbours
        return False

    def enough_info_to_make_decision(self) -> bool:
        # the lone goldfish only needs the water quantity of his cell to take a decision
        return True

    def make_decision_send_to_env(self) -> None:
        # *******************************************************
        # decision making:
        # if cell contains water: drink maximum amount
        # else move randomly (up, down, left or right)
        # ********************************************************
        if self.tile_water > 0:
            decision = "NULL"
        else:
            direction = self._rdm_direction()
            decision: str = "move" + "." + str(direction)

        self.context.logger.info(
            "sending command={} to env={}".format(
                decision, self.current_env_message.sender
            )
        )
        return_agent_env_message = self.current_env_dialogue.reply(
            performative=AgentEnvironmentMessage.Performative.ACTION,
            target_message=self.current_env_message,
            command=decision,
        )
        self.context.outbox.put_message(message=return_agent_env_message)
        self.is_round_done = True

    def _rdm_direction(self) -> str:
        rdm = random.randint(0,3)
        directions = ["north", "east", "south", "west"]
        return directions[rdm]


class AltruisticGoldfishStrategy(Model):
    """
    The altruistic goldfish. 
    They don't remember anything, but at least they're friendly. 
    They ask for water when they're thirsty and find a hydrated neighbor, 
    they offer water to thirsty neighbors when they find water. 
    Otherwise they perform a uniform random walk to find water.
    """

    thirst_level = 75  #### this should be a arg of the model !
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
    a_neighbour_is_thirsty = None
    a_neighbour_has_water_to_offer = None

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
        self.context.logger.info(self.neighbour_water_amount)
        self.is_round_done = False

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:
        # If round number is of prev round. discard
        # If round number is of future round. something is wrong because you should not be able to
        # request anything
        # assert self.round_no >= agent_agent_message.turn_number
        # if self.round_no == agent_agent_message.turn_number:
        if not self.is_round_done:
            # Use info
            index = self.neighbour_water_amount.index([agent_agent_message.sender, "Asking"])
            self.neighbour_water_amount[index] = [agent_agent_message.sender, agent_agent_message.water]
            if self.neighbour_water_amount[index] <= self.thirst_level:
                self.a_neighbour_is_thirsty = True
            else:
                self.a_neighbour_has_water_to_offer = True

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
                    water=self.agent_water,
                )
                self.context.outbox.put_message(message=return_message)
                return True
            else:
                self.agent_message_asking_for_my_water.append(request)
                return False

    def potentially_ask_for_info(self) -> bool:
        # currently, ALL info has to be asked for
        # return true if a message asking for water is sent
        # false otherwise
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown":
                i[1] = "Asking"
                agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)
                # message sent to another agent
                send_agent_agent_message, _ = agent_agent_dialogues.create(
                    counterparty=i[0],
                    performative=AgentAgentMessage.Performative.REQUEST_INFO,
                    turn_number=self.round_no,
                )
                self.context.outbox.put_message(message=send_agent_agent_message)
                self.context.logger.info(i[0])
                return True
        return False

    def enough_info_to_make_decision(self) -> bool:
        # If the agent is thirsty it needs to wait until its neighbours told him their water status
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown" or i[1] == "Asking":
                return False
        return True

    def make_decision_send_to_env(self) -> None:
        # *******************************************************
        # decision making:
        # if thirsty : drink (either from cell or from neighbours)
        # if water in current cell and neighbours thirsty : send water
        # else move randomly (up, down, left or right)
        # ********************************************************

        if self.tile_water > 0:
            if not (self.a_neighbour_is_thirsty):
                decision = "NULL"  # neighbours are not thirsty and the cell has water
            else:
                # a neighbour is thirsty, offering the extra water from the cell
                if self.agent_water <= self.thirst_level:
                    water = min(0, self.tile_water - (self.thirst_level - self.agent_water))
                else:
                    water = self.tile_water
                decision: str = "offer_water" + "." + str(water)
        else:
            # the cell has no water
            if self.agent_water > self.thirst_level and self.a_neighbour_is_thirsty:
                # a neighbour is thirsty so it offers the extra water that he has
                water = self.agent_water - self.thirst_level
                decision: str = "offer_water" + "." + str(water)
            elif self.agent_water <= self.thirst_level and self.a_neighbour_has_water_to_offer:
                # agent is thirsty and another has water to offer
                water = self.thirst_level - self.agent_water
                decision: str = "receive_water" + "." + str(water)
            else:
                # cell has no water and neigbours are not thirsty or if they are agent doesn't have any to offer
                direction = _rdm_direction()
                decision: str = "move" + "." + str(direction)

        self.context.logger.info(
            "sending command={} to env={}".format(
                decision, self.current_env_message.sender
            )
        )
        return_agent_env_message = self.current_env_dialogue.reply(
            performative=AgentEnvironmentMessage.Performative.ACTION,
            target_message=self.current_env_message,
            command=decision,
        )
        self.context.outbox.put_message(message=return_agent_env_message)
        self.is_round_done = True

    def _rdm_direction(self) -> str:
        rdm = np.random.random_integers(0, high=4)
        directions = ["up", "down", "right", "left"]
        return directions[rdm]
