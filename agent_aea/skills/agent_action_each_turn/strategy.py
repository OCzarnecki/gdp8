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
import math
import random
from typing import cast, Any

from aea.skills.base import Model

from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage
from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue


# Next round env message SHOULD NEVER be able to come when is_round_done = false.
# ALL messages sent has to be replied before making a decision (for now)


class DogStrategy(Model):
    """
    This class defines the strategy Explorer Dogs for the agent
    The explorer dogs:
    They're loyal, stubborn, and just a little smart. They actively go out and seek water when they're hydrated, when
    they are not hydrated, they will ask agents encountered about water directions and return to where they think the
    closest water is at (could be from info of another agent, could be from previous exploration)
    """

    tile_water = None
    agent_water = None
    north_neighbour_id = None
    east_neighbour_id = None
    south_neighbour_id = None
    west_neighbour_id = None
    neighbour_water_amount = None
    current_env_message = None
    current_env_dialogue = None
    round_no = -1
    is_round_done = True
    agent_messages_returned_waiting_for_response = []
    agent_message_asking_for_my_water = []
    asked_for_info_already = True
    water_location: list[list[int]] = []
    move_direction_last_turn = "None"

    def __init__(self, **kwargs: Any) -> None:
        self.agent_max_capacity = kwargs['agent_max_capacity']
        self.desperate_for_water_when_below = math.floor(
            self.agent_max_capacity * kwargs['thirsty_below_that_percentage_of_water'] / 100)
        self.agent_max_dig_rate = kwargs['agent_max_dig_rate']
        self.least_water_amount_in_tile_for_agent_to_remember_it = self.agent_max_dig_rate
        super().__init__(**kwargs)

    def receive_agent_env_info(self, agent_environment_message: AgentEnvironmentMessage,
                               agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        assert agent_environment_message.turn_number == self.round_no + 1, \
            agent_environment_message.turn_number + "." + str(self.round_no)
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
                assert(self.move_direction_last_turn == "west")
                new_list = [[x + 1, y] for [x, y] in self.water_location]
            self.water_location = new_list

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:

        if not self.is_round_done:
            sender = agent_agent_message.sender
            reply = agent_agent_message.reply
            if reply.find(".") == -1 and reply != "None":
                water_info = int(reply)
                index = -1
                index_not_found = True
                while index_not_found:
                    index += 1
                    if self.neighbour_water_amount[index][0] == sender and self.neighbour_water_amount[index][
                        1] == "Asking":
                        index_not_found = False
                self.neighbour_water_amount[index][1] = water_info
            else:
                if reply == "None":
                    index_not_found = True
                    index = -1
                    while index_not_found:
                        index += 1
                        if self.neighbour_water_amount[index][0] == sender \
                                and self.neighbour_water_amount[index][2] == "Asking":
                            index_not_found = False
                    self.neighbour_water_amount[index][2] = "Result Received"
                else:
                    [x, y] = reply.split(".")
                    x = int(x)
                    y = int(y)
                    if self.north_neighbour_id == sender:
                        y += 1
                    elif self.east_neighbour_id == sender:
                        x += 1
                    elif self.south_neighbour_id == sender:
                        y -= 1
                    elif self.west_neighbour_id == sender:
                        x -= 1
                    self.add_to_water_location([x, y])
                    index_not_found = True
                    index = -1
                    while index_not_found:
                        index += 1
                        if self.neighbour_water_amount[index][0] == sender \
                                and self.neighbour_water_amount[index][2] == "Asking":
                            index_not_found = False
                    self.neighbour_water_amount[index][2] = "Result Received"

    def add_to_water_location(self, xy_coordinates) -> None:
        try:
            self.water_location.index(xy_coordinates)
        except ValueError:
            self.water_location.append(xy_coordinates)

    def deal_with_an_agent_asking_for_info(self) -> bool:
        if len(self.agent_message_asking_for_my_water) == 0:
            return False
        else:
            request, *self.agent_message_asking_for_my_water = self.agent_message_asking_for_my_water
            [message_, dialogue_] = request
            message = cast(AgentAgentMessage, message_)
            dialogue = cast(AgentAgentDialogue, dialogue_)
            if message.turn_number == self.round_no:
                if message.request == "water_info":
                    reply = str(self.agent_water)
                    return_message = dialogue.reply(
                        performative=AgentAgentMessage.Performative.RECEIVER_REPLY,
                        target_message=message,
                        reply=reply,
                    )
                    self.context.logger.info("sending agent message for info back")
                    self.context.outbox.put_message(message=return_message)
                elif message.request == "closest_water":
                    path = str(self.find_path_to_closest_water())
                    return_message = dialogue.reply(
                        performative=AgentAgentMessage.Performative.RECEIVER_REPLY,
                        target_message=message,
                        reply=path,
                    )
                    self.context.logger.info("sending agent message for info back")
                    self.context.outbox.put_message(message=return_message)
                else:
                    self.context.logger.info("Agent_Agent_Message of unknown request = {}".format(message.request))
                return True
            else:
                self.agent_message_asking_for_my_water.append(request)
                return False

    def enough_info_to_make_decision(self) -> bool:
        for i in self.neighbour_water_amount:
            if i[1] == "Asking" or i[2] == "Asking":
                return False
        return True

    def ask_for_info_and_maybe_make_decision(self) -> None:
        if self.agent_water <= self.desperate_for_water_when_below:
            state = "returning"
        else:
            state = "exploring"
        self.context.logger.info("agent in state = " + state)
        try:
            self.water_location.remove([0, 0])
        except ValueError:
            pass
        if self.tile_water > self.least_water_amount_in_tile_for_agent_to_remember_it:
            self.water_location.append([0, 0])
        if state == "exploring":
            if self.agent_water < self.agent_max_capacity - self.agent_max_dig_rate and self.tile_water > 0:
                self.asked_for_info_already = True
                return_agent_env_message = self.current_env_dialogue.reply(
                    performative=AgentEnvironmentMessage.Performative.ACTION,
                    target_message=self.current_env_message,
                    command="NULL",
                )
                self.context.logger.info("sending env message back with command = " + "NULL")
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
            else:
                self.asked_for_info_already = True
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
                    if self.move_direction_last_turn == "north":
                        if randomizer == 1:
                            direction = "move.west"
                        elif randomizer == 5:
                            direction = "move.east"
                        else:
                            direction = "move.north"
                    elif self.move_direction_last_turn == "east":
                        if randomizer == 1:
                            direction = "move.north"
                        elif randomizer == 5:
                            direction = "move.south"
                        else:
                            direction = "move.east"
                    elif self.move_direction_last_turn == "south":
                        if randomizer == 1:
                            direction = "move.east"
                        elif randomizer == 5:
                            direction = "move.west"
                        else:
                            direction = "move.south"
                    else:
                        assert self.move_direction_last_turn == "west"
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
                self.context.logger.info("sending env message back with command = " + direction)
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
        if state == "returning":
            if self.tile_water > 1:
                self.asked_for_info_already = True
                return_agent_env_message = self.current_env_dialogue.reply(
                    performative=AgentEnvironmentMessage.Performative.ACTION,
                    target_message=self.current_env_message,
                    command="NULL",
                )
                self.context.logger.info("sending env message back with command = " + "NULL")
                self.context.outbox.put_message(message=return_agent_env_message)
                self.is_round_done = True
            else:
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
                request="closest_water",
            )
            self.context.outbox.put_message(message=send_agent_agent_message)
            self.context.logger.info("sending agent message to " + id_of_agent_to_ask)

    def find_path_to_closest_water(self) -> str:
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
                decision = "move.east"
            elif x < 0:
                decision = "move.west"
            elif y > 0:
                decision = "move.north"
            else:
                if y == 0:
                    self.context.logger.info("agent_decision_making_algorithm_error")
                decision = "move.south"
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


def _rdm_direction() -> str:
    rdm = random.randint(0, 3)
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

    tile_water = None
    agent_water = None
    neighbour_id = None
    neighbour_water_amount = None
    current_env_message = None
    current_env_dialogue = None
    round_no = -1
    is_round_done = True
    asked_for_info_already = True
    agent_messages_returned_waiting_for_response = []
    agent_message_asking_for_my_water = []
    a_neighbour_is_thirsty = None
    a_neighbour_has_water_to_offer = None

    def __init__(self, **kwargs: Any) -> None:
        self.agent_max_water = kwargs['agent_max_capacity']
        self.desperate_for_water_when_below = math.floor(
            self.agent_max_water * kwargs['thirsty_below_that_percentage_of_water'] / 100)
        super().__init__(**kwargs)

    def receive_agent_env_info(self, agent_environment_message: AgentEnvironmentMessage,
                               agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        assert agent_environment_message.turn_number == self.round_no + 1
        assert self.is_round_done
        self.round_no += 1
        self.current_env_message = agent_environment_message
        self.current_env_dialogue = agent_environment_dialogue
        self.tile_water = agent_environment_message.tile_water
        self.agent_water = agent_environment_message.agent_water
        self.neighbour_id = [agent for agent in
                             [agent_environment_message.north_neighbour_id, agent_environment_message.east_neighbour_id,
                              agent_environment_message.south_neighbour_id, agent_environment_message.west_neighbour_id]
                             if agent != "None"]
        self.neighbour_water_amount = [[i, "Unknown"] for i in self.neighbour_id]
        self.context.logger.info(self.neighbour_water_amount)
        self.is_round_done = False
        self.asked_for_info_already = False
        self.a_neighbour_has_water_to_offer = False
        self.a_neighbour_is_thirsty = False

    def receive_agent_agent_info(self, agent_agent_message: AgentAgentMessage) -> None:
        if not self.is_round_done:
            index = self.neighbour_water_amount.index([agent_agent_message.sender, "Asking"])
            self.neighbour_water_amount[index] = [agent_agent_message.sender, int(agent_agent_message.reply)]
            if self.neighbour_water_amount[index][1] <= self.desperate_for_water_when_below:
                self.a_neighbour_is_thirsty = True
            else:
                self.a_neighbour_has_water_to_offer = True

    def deal_with_an_agent_asking_for_info(self) -> bool:
        if not self.agent_message_asking_for_my_water:
            return False
        else:
            request, *self.agent_message_asking_for_my_water = self.agent_message_asking_for_my_water
            [message_, dialogue_] = request
            message = cast(AgentAgentMessage, message_)
            dialogue = cast(AgentAgentDialogue, dialogue_)
            if message.turn_number == self.round_no:
                return_message = dialogue.reply(
                    performative=AgentAgentMessage.Performative.RECEIVER_REPLY,
                    target_message=message,
                    reply=str(self.agent_water),
                )
                self.context.outbox.put_message(message=return_message)
                return True
            else:
                self.agent_message_asking_for_my_water.append(request)
                return False

    def ask_for_info_and_maybe_make_decision(self) -> None:
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown":
                i[1] = "Asking"
                agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)
                send_agent_agent_message, _ = agent_agent_dialogues.create(
                    counterparty=i[0],
                    performative=AgentAgentMessage.Performative.SENDER_REQUEST,
                    turn_number=self.round_no,
                    request="water_info"
                )
                self.context.outbox.put_message(message=send_agent_agent_message)
                self.context.logger.info(i[0])
        self.asked_for_info_already = True

    def enough_info_to_make_decision(self) -> bool:
        for i in self.neighbour_water_amount:
            if i[1] == "Unknown" or i[1] == "Asking":
                return False
        return True

    def make_decision_send_to_env(self) -> None:
        if self.tile_water > 0:
            if not self.a_neighbour_is_thirsty:
                decision = "NULL"
            elif self.agent_water <= 10:
                decision = "NULL"
            else:
                water = min(self.agent_water // 2, self.tile_water - (self.agent_max_water - self.agent_water))
                if water < 5:
                    decision: str = "NULL"
                else:
                    decision: str = "offer_water" + "." + str(water)
        else:
            if self.agent_water > self.desperate_for_water_when_below and self.a_neighbour_is_thirsty:
                water = self.agent_water - self.desperate_for_water_when_below
                decision: str = "offer_water" + "." + str(water)
            elif self.agent_water <= self.desperate_for_water_when_below and self.a_neighbour_has_water_to_offer:
                water = self.desperate_for_water_when_below - self.agent_water + 10
                decision: str = "receive_water" + "." + str(water)
            else:
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
    asked_for_info_already = True

    def deal_with_an_agent_asking_for_info(self) -> bool:
        return False

    def ask_for_info_and_maybe_make_decision(self) -> None:
        pass

    def enough_info_to_make_decision(self) -> bool:
        return True

    def receive_agent_env_info(self, agent_environment_message: AgentEnvironmentMessage,
                               agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        assert agent_environment_message.turn_number == self.round_no + 1
        assert self.is_round_done
        self.round_no += 1
        self.current_env_message = agent_environment_message
        self.current_env_dialogue = agent_environment_dialogue
        self.tile_water = agent_environment_message.tile_water
        self.agent_water = agent_environment_message.agent_water
        self.is_round_done = False

    def make_decision_send_to_env(self) -> None:
        if self.tile_water > 0:
            decision = "NULL"
        else:
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
