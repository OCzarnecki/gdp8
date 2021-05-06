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

"""This package contains a scaffold of a handler, that handles the replies of agents every turn."""

from typing import cast

# from aea.configurations.base import PublicId

from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.fetchai.protocols.default.message import DefaultMessage
from packages.fetchai.protocols.default.dialogues import DefaultDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues
from packages.gdp8.skills.env_action_each_turn.environment import Environment, Phase


class EnvironmentHandler(Handler):
    """This class handles oef messages."""

    SUPPORTED_PROTOCOL = AgentEnvironmentMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the handler setup.

        :return: None
        """

    def handle(self, message: Message) -> None:
        """
        Handle a register message.
        If the address is already registered, answer with an error message.

        :param message: the agent_environment message
        :return: None
        """
        agent_env_msg = cast(AgentEnvironmentMessage, message)

        # recover dialogue
        agent_environment_dialogues = cast(AgentEnvironmentDialogues,
                                           self.context.agent_environment_dialogues)
        agent_environment_dialogue = cast(AgentEnvironmentDialogue,
                                          agent_environment_dialogues.update(agent_env_msg))

        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_env_msg)
            return

        self.context.logger.info(
            "handling the agent_environment message. performative={}".format(agent_env_msg.performative)
        )
        # handle message
        if agent_env_msg.performative == AgentEnvironmentMessage.Performative.ACTION:
            self._handle_valid_tick_reply(agent_env_msg)
        else:
            self._handle_invalid(agent_env_msg, agent_environment_dialogue)

            self.context.logger.warning(
                "Agent Message performative not recognized or not permitted."
            )

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """

    def _handle_unidentified_dialogue(self, agent_env_msg: AgentEnvironmentMessage) -> None:
        """
        Handle an unidentified dialogue.

        :param agent_env_msg: the message
        """
        self.context.logger.info(
            "received invalid agent_env message={}, unidentified dialogue.".format(agent_env_msg)
        )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=agent_env_msg.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_description=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"Agent Environment Message": agent_env_msg.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_valid_tick_reply(self, agent_env_msg: AgentEnvironmentMessage):
        """
        Handle a valid tick message reply. (we suppose that all replies are valid, but can add a check if needed)

        That is:
        - update the environment state

        :return: None
        """
        environment = cast(Environment, self.context.environment)
        self.context.logger.info(
            "handling tick message reply: '{}', address = '{}'".format(
                environment.address_to_id(agent_env_msg.sender), agent_env_msg.sender
            )
        )
        # Agents reply should only be handled if they concern the current turn. 
        # FIXME getting rid of this for now, because of weird message shenanigans:
        #     turn_number' content is not set.
        # assert(agent_env_msg.turn_number == self.context.environment.turn_number)

        environment.save_action(agent_env_msg.sender, agent_env_msg.command)

    def _handle_invalid(self, agent_env_msg: AgentEnvironmentMessage,
                        agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        """
        Handle an agent environment message of invalid performative.

        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue (Fipa?)
        :return: None
        """
        self.context.logger.warning(
            "cannot handle agent_environment message of performative={} in dialogue={}.".format(
                agent_env_msg.performative, agent_environment_dialogue
            )
        )
