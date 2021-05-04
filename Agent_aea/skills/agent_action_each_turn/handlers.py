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

from typing import cast, Any

from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage
from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues

from packages.gdp8.skills.agent_action_each_turn.strategy import \
    DogStrategy, AltruisticGoldfishStrategy, LoneGoldfishStrategy


# Handler will Update my model (strategy class) depending on what it has received
# Unimplemented: self.context.agent_environment_dialogues, self.context.default_dialogues


class EnvironmentMessageHandler(Handler):
    """This class handles messages from the environment."""

    SUPPORTED_PROTOCOL = AgentEnvironmentMessage.protocol_id

    def __init__(self, **kwargs: Any) -> None:
        self.strategyName = kwargs['strategy_used']
        super().__init__(**kwargs)

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """

    def handle(self, message: Message) -> None:
        self.context.logger.info("start handling env msg")
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        agent_env_msg = cast(AgentEnvironmentMessage, message)

        # recover dialogue
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        agent_environment_dialogue = cast(AgentEnvironmentDialogue, agent_environment_dialogues.update(agent_env_msg))
        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_env_msg)
            return

        # handle message
        # environment = cast(Environment, self.context.environment)##
        self.context.logger.debug(
            "handling environment response. performative={}".format(agent_env_msg.performative)
        )

        if agent_env_msg.performative == AgentEnvironmentMessage.Performative.TICK:
            self._on_tick(agent_env_msg, agent_environment_dialogue)
        else:
            self._handle_invalid(agent_env_msg, agent_environment_dialogue)

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
        self.context.logger.warning(
            "received invalid environment message={}, unidentified dialogue.".format(agent_env_msg)
        )

    def _on_tick(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue: AgentEnvironmentDialogue):
        """ 
        Handle a tick message from the environment from an identified dialogue.
        
        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        # Update my_model to get ready for next round
        self.context.logger.info("received tick message from the environment.")

        if self.strategyName == "Explorer Dogs":
            strategy = cast(DogStrategy, self.context.dog_strategy)
        elif self.strategyName == "Altruistic Goldfish":
            strategy = cast(AltruisticGoldfishStrategy, self.context.altruistic_goldfish_strategy)
        else:
            assert self.strategyName == "Lone Goldfish"
            strategy = cast(LoneGoldfishStrategy, self.context.lone_goldfish_strategy)   

        strategy.receive_agent_env_info(agent_env_msg, agent_environment_dialogue)

    def _handle_invalid(self, agent_env_msg: AgentEnvironmentMessage,
                        agent_environment_dialogue: AgentEnvironmentDialogue) -> None:
        """
        Handle an oef search message.
f
        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        self.context.logger.warning(
            "cannot handle environment message of performative={} in dialogue={}.".format(
                agent_env_msg.performative, agent_environment_dialogue
            )
        )


class AgentMessageHandler(Handler):
    SUPPORTED_PROTOCOL = AgentAgentMessage.protocol_id

    def __init__(self, **kwargs: Any) -> None:
        self.strategyName = kwargs['strategy_used']
        super().__init__(**kwargs)

    def setup(self, **kwargs: Any) -> None:
        """
        Implement the setup.

        :return: None
        """

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        :return: None
        """
        self.context.logger.info("start handling agent msg")
        agent_agent_msg = cast(AgentAgentMessage, message)

        agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)
        agent_agent_dialogue = cast(AgentAgentDialogue,
                                    agent_agent_dialogues.update(agent_agent_msg))
        if agent_agent_dialogue is None:
            self._handle_unidentified_dialogue(agent_agent_msg)
            return

        self.context.logger.info(agent_agent_msg.performative)
        if agent_agent_msg.performative == AgentAgentMessage.Performative.SENDER_REQUEST:
            self._handle_other_agent_request_for_info(agent_agent_msg, agent_agent_dialogue)
        elif agent_agent_msg.performative == AgentAgentMessage.Performative.RECEIVER_REPLY:
            self._handle_info_in_replies_from_other_agent(agent_agent_msg)
        else:
            self._handle_invalid(agent_agent_msg, agent_agent_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """

    def _handle_unidentified_dialogue(self, agent_agent_msg: AgentAgentMessage) -> None:
        """
        Handle an unidentified dialogue.
        :param agent_agent_msg: the message
        """
        self.context.logger.info(
            "received invalid agent_agent message={}, unidentified dialogue.".format(agent_agent_msg)
        )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=agent_agent_msg.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"Agent Environment Message": agent_agent_msg.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_info_in_replies_from_other_agent(self, agent_agent_msg: AgentAgentMessage):
        # Actual function where agent messages are used.
        if self.strategyName == "Explorer Dogs":
            strategy = cast(DogStrategy, self.context.dog_strategy)
        elif self.strategyName == "Altruistic Goldfish":
            strategy = cast(AltruisticGoldfishStrategy, self.context.altruistic_goldfish_strategy)
        else:
            assert self.strategyName == "Lone Goldfish"
            strategy = cast(LoneGoldfishStrategy, self.context.lone_goldfish_strategy)

        # Info received. returns whether we can go to make_decision (may be on waiting list since last round not over)
        # True = Go on, False = stop
        strategy.receive_agent_agent_info(agent_agent_msg)

    def _handle_other_agent_request_for_info(self, agent_agent_msg: AgentAgentMessage, agent_agent_dialogue):
        if self.strategyName == "Explorer Dogs":
            strategy = cast(DogStrategy, self.context.dog_strategy)
        elif self.strategyName == "Altruistic Goldfish":
            strategy = cast(AltruisticGoldfishStrategy, self.context.altruistic_goldfish_strategy)
        else:
            assert self.strategyName == "Lone Goldfish"
            strategy = cast(LoneGoldfishStrategy, self.context.lone_goldfish_strategy)   
                 
        self.context.logger.info("request_appended")
        strategy.agent_message_asking_for_my_water.append(
            [agent_agent_msg, agent_agent_dialogue]
        )

    def _handle_invalid(self, agent_agent_msg: AgentAgentMessage, agent_agent_dialogue) -> None:
        """
        Handle a invalid agent_agent message.

        :param agent_agent_msg: the agent agent message
        :param agent_agent_dialogue: the agent agent dialogue
        :return: None
        """
        self.context.logger.warning(
            "cannot handle environment message of performative={} in dialogue={}.".format(
                agent_agent_msg.performative, agent_agent_dialogue
            )
        )
