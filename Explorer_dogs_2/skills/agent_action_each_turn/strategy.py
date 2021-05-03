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


Desperate_for_water_when_below = 75
agent_max_capacity = 150
agent_max_dig_rate = 20
least_water_amount_in_tile_for_agent_to_remember_it = agent_max_dig_rate


class BasicStrategy(Model):
    """
    This class defines the strategy for the agent
    Generic Strategy is to gather agent water amount before making a decision
    """

    tile_water = None
    agent_water = None
    north_neighbour_id = None
    east_neighbour_id = None
    south_neighbour_id = None
    west_neighbour_id = None
    neighbour_water_amount = None
    # neighbour_water_amount are list of twos of agent_id and their info which = "Unknown" initially,
    # = "Asking" if a message has been sent to ask
    current_env_message = None
    current_env_dialogue = None
    round_no = -1
    is_round_done = True
    agent_messages_returned_waiting_for_response = []  # Storing any messages of future round
    agent_message_asking_for_my_water = []  # Storing any messages of future round
    asked_for_info_already = True
    water_location = []
    move_direction_last_turn = "None"

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
        self.north_neighbour_id = agent_environment_message.north_neighbour_id
        self.east_neighbour_id = agent_environment_message.east_neighbour_id
        self.south_neighbour_id = agent_environment_message.south_neighbour_id
        self.west_neighbour_id = agent_environment_message.west_neighbour_id
        self.neighbour_water_amount = [[i, "Water info unknown", "Direction to nearest water unknown"] for i in
                                       [self.north_neighbour_id, self.east_neighbour_id,
                                        self.south_neighbour_id, self.west_neighbour_id] if i != "None"]
        self.context.logger.info(self.neighbour_water_amount)
        self.move_direction_last_turn = agent_environment_message.movement_last_turn
        self.update_water_location_according_to_last_round_movement()
        self.is_round_done = False
        self.asked_for_info_already = False

    def update_water_location_according_to_last_round_movement(self) -> None:
        if self.move_direction_last_turn == "None":
            pass
        else:
            if self.move_direction_last_turn == "north":
                new_list = [[x, y - 1] for [x, y] in self.water_location]
            elif self.move_direction_last_turn == "east":
                new_list = [[x - 1, y] for [x, y] in self.water_location]
            elif self.move_direction_last_turn == "south":
                new_list = [[x, y + 1] for [x, y] in self.water_location]
            else:
                # assert(self.move_direction_last_turn == "west")
                if not self.move_direction_last_turn == "west":
                    self.context.logger.info("invalid move direction last turn = " + self.move_direction_last_turn)
                new_list = [[x + 1, y] for [x, y] in self.water_location]
            self.water_location = new_list

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:
        # If round number is of prev round. discard
        # If round number is of future round. something is wrong cuz you should not be able to
        # request anything
        # assert self.round_no >= agent_agent_message.turn_number
        # if self.round_no == agent_agent_message.turn_number:

        if not self.is_round_done:
            # Use info
            sender = agent_agent_message.sender
            reply = agent_agent_message.reply
            try:
                water_info = int(reply)
                index = -1
                index_not_found = True
                while index_not_found:
                    index += 1
                    if self.neighbour_water_amount[index][0] == sender \
                            & self.neighbour_water_amount[index][1] == "Asking":
                        index_not_found = False
                self.neighbour_water_amount[index][1] = water_info
            except ValueError:
                [x, y] = reply.split(".")
                x = int(x)
                y = int(y)
                # x.y should be returned denoting x steps North and y steps East
                # tokens = [x,y]
                # Add the direction of this agent to cuz xy is the relative distance from that agent to water not
                # distance of me to water
                if self.north_neighbour_id == sender:
                    y += 1
                elif self.east_neighbour_id == sender:
                    y += 1
                elif self.south_neighbour_id == sender:
                    y -= 1
                elif self.west_neighbour_id == sender:
                    y -= 1
                self.add_to_water_location([x, y])
                index_not_found = True
                index = -1
                while index_not_found:
                    index += 1
                    if self.neighbour_water_amount[index][0] == sender \
                            & self.neighbour_water_amount[index][2] == "Asking":
                        index_not_found = False
                self.neighbour_water_amount[index][2] = "Result Received"

    def add_to_water_location(self, xy_coordinates: list[int]) -> None:
        try:
            self.water_location.index(xy_coordinates)
            # if doesn't fail, we already know there is water there, nothing to be done
        except ValueError:
            self.water_location.append(xy_coordinates)

    def deal_with_an_agent_asking_for_info(self) -> bool:
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
                if message.request == "water_info":
                    return_message = dialogue.reply(
                        performative=AgentAgentMessage.Performative.RECIEVER_REPLY,
                        target_message=message,
                        reply=str(self.agent_water),
                    )
                    self.context.outbox.put_message(message=return_message)
                elif message.request == "closest_water":
                    path = self.find_path_to_closest_water
                    return_message = dialogue.reply(
                        performative=AgentAgentMessage.Performative.RECIEVER_REPLY,
                        target_message=message,
                        reply=path,
                    )
                    self.context.outbox.put_message(message=return_message)
                else:
                    self.context.logger.info("Agent_Agent_Message of unknown request = {}".format(message.request))
                return True
            else:
                self.agent_message_asking_for_my_water.append(request)
                return False

    def enough_info_to_make_decision(self) -> bool:
        # Wait till all info that were asked are returned
        for i in self.neighbour_water_amount:
            if i[1] == "Asking" or i[2] == "Asking":
                return False
        return True

    def ask_for_info_and_maybe_make_decision(self) -> None:
        # state, am i exploring? or am i in desperation need for water
        # If exploring:
        # If tile water > 100, mark and rmb
        # Replenish water supply if on water
        if self.agent_water <= Desperate_for_water_when_below:
            state = "returning"
        else:
            state = "exploring"
        # no matter what, update memory about this tile
        try:
            self.water_location.remove([0, 0])
        except ValueError:
            pass
        if self.tile_water > least_water_amount_in_tile_for_agent_to_remember_it:
            self.water_location.append([0, 0])
        if state == "exploring":
            if self.agent_water < agent_max_capacity - agent_max_dig_rate & self.tile_water > 0:
                # Replenish water supply, no need for asking for info
                self.asked_for_info_already = True
                return_agent_env_message = self.current_env_dialogue.reply(
                    performative=AgentEnvironmentMessage.Performative.ACTION,
                    target_message=self.current_env_message,
                    command="NULL",
                )
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
            else:
                # No need to ask for info, exploring
                self.asked_for_info_already = True
                # Explore, follow path from last round with high probability, can return to env immediately
                if self.move_direction_last_turn == "None":
                    randomizer = random.randint(1, 4)
                    if randomizer == 1:
                        direction = "move.north"
                    elif randomizer == 2:
                        direction = "move.east"
                    elif randomizer == 3:
                        direction = "move.south"
                    else:
                        assert randomizer == 4
                        direction = "move.west"
                else:
                    randomizer = random.randint(1, 5)
                    if self.move_direction_last_turn == "North":
                        if randomizer == 1:
                            direction = "move.west"
                        elif randomizer == 5:
                            direction = "move.east"
                        else:
                            direction = "move.north"
                    elif self.move_direction_last_turn == "East":
                        if randomizer == 1:
                            direction = "move.north"
                        elif randomizer == 5:
                            direction = "move.south"
                        else:
                            direction = "move.east"
                    elif self.move_direction_last_turn == "South":
                        if randomizer == 1:
                            direction = "move.east"
                        elif randomizer == 5:
                            direction = "move.west"
                        else:
                            direction = "move.south"
                    else:
                        assert self.move_direction_last_turn == "West"
                        if randomizer == 1:
                            direction = "move.south"
                        elif randomizer == 5:
                            direction = "move.north"
                        else:
                            direction = "move.west"
                return_agent_env_message = self.current_env_dialogue.reply(
                    performative=AgentEnvironmentMessage.Performative.ACTION,
                    target_message=self.current_env_message,
                    command=direction,
                )
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
        if state == "returning":
            if self.tile_water > 1:
                # Replenish water supply, no need for asking for info
                self.asked_for_info_already = True
                return_agent_env_message = self.current_env_dialogue.reply(
                    performative=AgentEnvironmentMessage.Performative.ACTION,
                    target_message=self.current_env_message,
                    command="NULL",
                )
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
            else:
                # Ask all other agent about closest water location, make_decision later
                self.ask_all_neighbour_water_location()
                self.asked_for_info_already = True

    def ask_all_neighbour_water_location(self) -> None:
        for neighbour_info in self.neighbour_water_amount:
            id_of_agent_to_ask = neighbour_info[0]
            neighbour_info[2] = "Asking"
            agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)
            send_agent_agent_message, _ = agent_agent_dialogues.create(
                counterparty=id_of_agent_to_ask,
                performative=AgentAgentMessage.Performative.SENDER_REQUEST,
                turn_number=self.round_no,
                requests="closest_water",
            )

    def find_path_to_closest_water(self) -> str:
        # Look at info in water location, find closest
        if len(self.water_location) == 0:
            return "None"
        else:
            [x_, y_] = self.water_location[0]
            closest_distance = abs(x_) + abs(y_)
            corresponding_location = [x_, y_]
            for [x, y] in self.water_location:
                if abs(x) + abs(y) < closest_distance:
                    closest_distance = abs(x) + abs(y)
                    corresponding_location = [x, y]
            return str(corresponding_location[0]) + "." + str(corresponding_location[1])

    def make_decision_send_to_env(self) -> None:
        path = self.find_path_to_closest_water()
        if path == "None":
            x = random.randint(1, 4)
            if x == 1:
                decision = "move.north"
            elif x == 2:
                decision = "move.south"
            elif x == 3:
                decision = "move.east"
            else:
                decision = "move.west"
        else:
            [x, y] = path.split(".")
            x = int(x)
            y = int(y)
            if x > 0:
                decision = "move.north"
            elif x < 0:
                decision = "move.south"
            elif y > 0:
                decision = "move.east"
            else:
                if y == 0:
                    self.context.logger.info("agent_decision_making_algorithm_error")
                decision = "move.west"
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
