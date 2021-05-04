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

from aea.skills.base import Model

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
        rdm = random.randint(0, 3)
        directions = ["north", "east", "south", "west"]
        return directions[rdm]
