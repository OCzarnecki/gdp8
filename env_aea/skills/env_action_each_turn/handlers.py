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

from typing import Optional, cast

from aea.configurations.base import PublicId

from aea.protocols.base import Message
from aea.skills.base import Handler
from packages.fetchai.protocols.oef_search.message import OefSearchMessage##
from packages.gdp8.skills.env_action_each_turn.dialogues import (
    OefSearchDialogue,
    OefSearchDialogues,
)

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
        If the adress is already registered, answer with an error message.

        :param message: the agent_environment message
        :return: None
        """
        agent_env_msg = cast(AgentEnvironmentMessage, message)

        #recover dialogue
        agent_environment_dialogues = cast(AgentEnvironmentDialogues,
                                           self.context.agent_environment_dialogues)
        agent_environment_dialogue = cast(AgentEnvironmentDialogue,
                                          agent_environment_dialogues.update(agent_env_msg))
        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_env_msg)
            return

        self.context.logger.debug(
            "handling the agent_environment message. performative={}".format(agent_env_msg.performative)
        )
        #handle message
        if agent_env_msg.performative == AgentEnvironmentMessage.Performative.REGISTER:
            self._on_register(agent_env_msg, agent_environment_dialogue)
        elif agent_env_msg.performative == AgentEnvironmentMessage.Performative.UNREGISTER:
            self._on_unregister(agent_env_msg, agent_environment_dialogue)
        elif agent_env_msg.performative == AgentEnvironmentMessage.Performative.ACTION:
            self._on_action(agent_env_msg, agent_environment_dialogue)
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

    def _on_register(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        """
        Handle a register message.
        If the address is not registered, answer with an error message.
        
        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        if not environment.phase == Phase.SIMULATION_REGISTRATION:
            self.context.logger.warning(
                "received registration outside of environment registration phase: '{}'".format(
                    agent_env_msg
                )
            )
            return

        ## we can implement a whitelist if undesired agents try to register
        """parameters = cast(Parameters, self.context.parameters)
        ##agent_name = agent_env_msg.agent_name## do we have a whitelist with the name of the agents ? or an id ? 
        if len(parameters.whitelist) != 0 and agent_name not in parameters.whitelist:
            self.context.logger.warning(
                "agent name not in whitelist: '{}'".format(agent_name)
            )
            error_msg = agent_environment_dialogue.reply(
                performative=AgentEnvironmentMessage.Performative.AGENT_ENV_ERROR,
                target_message=agent_env_msg,## target or target_message ??
                error_description= "agent not in whitelist",
            )
            self.context.outbox.put_message(message=error_msg)
            return"""

        environment = cast(Environment, self.context.environment)##why do it again ?
        if agent_env_msg.sender in environment.registration.agent_addr_to_id:
            self.context.logger.warning(
                "agent already registered: '{}'".format(
                    environment.registration.agent_addr_to_id[agent_env_msg.sender],
                )
            )
            error_msg = agent_environment_dialogue.reply(
                performative=AgentEnvironmentMessage.Performative.AGENT_ENV_ERROR,
                target_message=agent_env_msg,
                error_descrition="agent address already registered",
            )
            self.context.outbox.put_message(message=error_msg)
            return

        environment.registration.register_agent(agent_env_msg.sender)
        self.context.logger.info("agent registered: '{}'".format(agent_env_msg.sender))

    def _on_unregister(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        """
        Handle an unregister message.
        If the address is not registered, answer with an error message.

        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        if not environment.phase == Phase.SIMULATION_REGISTRATION:
            self.context.logger.warning(
                "received unregister outside of environment registration phase: '{}'".format(
                    agent_env_msg
                )
            )
            return

        if agent_env_msg.sender not in environment.registration.agent_addr_to_id:
            self.context.logger.warning(
                "agent not registered: '{}'".format(agent_env_msg.sender)
            )
            error_msg = agent_environment_dialogue.reply(
                performative=AgentEnvironmentMessage.Performative.AGENT_ENV_ERROR,
                target_message=agent_env_msg,
                error_description="agent not registered",
            )
            self.context.outbox.put_message(message=error_msg)
        else:
            self.context.logger.debug(
                "agent unregistered: '{}'".format(
                    environment.registration.agent_addr_to_id[agent_env_msg.sender],
                )
            )
            environment.registration.unregister_agent(agent_env_msg.sender)

    def _handle_valid_tick_reply(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue):
        """
        Handle a valid tick message reply. (we suppose that all replies are valid, but can add a check if needed)

        That is:
        - update the environment state

        :param tick_reply: the tick message reply
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        self.context.logger.info(
            "handling tick message reply: '{}'".format(
                    environment.registration.agent_addr_to_id[agent_env_msg.sender],
                    )
        )
        # Agents reply should only be handled if they concern the current turn. 
        assert(agent_env_msg.turn_number == self.context.environment.turn_number)

        self.context.environment.save_action(agent_environment_dialogue.sender, agent_env_msg.action, agent_env_msg.water_content)
        
    def _handle_invalid(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        """
        Handle an agent environment message of invalid perfomative.

        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue (fipa?)
        :return: None
        """
        self.context.logger.warning(
            "cannot handle agent_environment message of performative={} in dialogue={}.".format(
                agent_env_msg.performative, agent_environment_dialogue
            )
        )


class OefSearchHandler(Handler):
    """Handle the message exchange with the OEF search node, which is not suppose to send messages to the environment."""

    SUPPORTED_PROTOCOL = OefSearchMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the handler setup.
        :return: None
        """

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        oef_search_msg = cast(OefSearchMessage, message)

        # recover dialogue
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_dialogue = cast(
            Optional[OefSearchDialogue], oef_search_dialogues.update(oef_search_msg)
        )
        if oef_search_dialogue is None:
            self._handle_unidentified_dialogue(oef_search_msg)
            return

        # handle message
        if oef_search_msg.performative is OefSearchMessage.Performative.OEF_ERROR:
            self._handle_error(oef_search_msg, oef_search_dialogue)
        else:
            self._handle_invalid(oef_search_msg, oef_search_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.
        :return: None
        """

    def _handle_unidentified_dialogue(self, oef_search_msg: OefSearchMessage) -> None:
        """
        Handle an unidentified dialogue.
        :param msg: the message
        """
        self.context.logger.info(
            "received invalid oef_search message={}, unidentified dialogue.".format(
                oef_search_msg
            )
        )

    def _handle_error(self, oef_search_msg: OefSearchMessage, oef_search_dialogue: OefSearchDialogue) -> None:
        """
        Handle an oef search message.
        :param oef_search_msg: the oef search message
        :param oef_search_dialogue: the dialogue
        :return: None
        """
        self.context.logger.info(
            "received oef_search error message={} in dialogue={}.".format(
                oef_search_msg, oef_search_dialogue
            )
        )

    def _handle_invalid(self, oef_search_msg: OefSearchMessage, oef_search_dialogue: OefSearchDialogue) -> None:
        """
        Handle an oef search message.
        :param oef_search_msg: the oef search message
        :param oef_search_dialogue: the dialogue
        :return: None
        """
        self.context.logger.warning(
            "cannot handle oef_search message of performative={} in dialogue={}.".format(
                oef_search_msg.performative, oef_search_dialogue,
            )
        )
