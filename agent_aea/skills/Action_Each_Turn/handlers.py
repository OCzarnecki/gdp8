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

from typing import Optional, cast

from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler

from gdp.agent_aea.protocols.agent_agent.message import AgentAgentMessage
from gdp.agent_aea.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from gdp.agent_aea.protocols.agent_environment.message import AgentEnvironmentMessage
from gdp.agent_aea.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues

from gdp.agent_aea.protocols.default.message import DefaultMessage
from gdp.agent_aea.protocols.default.dialogues import DefaultDialogues


class EnvironmentMessageHandler(Handler):
    SUPPORTED_PROTOCOL = AgentEnvironmentMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        :return: None
        """
        agent_environment_message = cast(AgentEnvironmentMessage, message)

        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues) # ??????????
        agent_environment_dialogue = cast(AgentEnvironmentDialogue,
                                          agent_environment_dialogues.update(agent_environment_message))
        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_environment_message)
            return

        if agent_environment_message.performative == AgentEnvironmentMessage.Performative.TICK:
            self._handle_(agent_environment_message, agent_environment_dialogue)
        else:
            self._handle_invalid(agent_environment_message, agent_environment_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_unidentified_dialogue(self, agent_environment_message: AgentEnvironmentMessage) -> None:
        """

        """
        # self.context.logger.info(
        #     "received invalid agent_environment message={}, unidentified dialogue.".format(agent_environment_message)
        # )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=agent_environment_message.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"Agent Environment Message": agent_environment_message.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_(self, agent_environment_message: AgentEnvironmentMessage, agent_environment_dialogue):
        # Actual function where Environment messages are received from.
        pass

    def _handle_invalid(self, agent_environment_message: AgentEnvironmentMessage, agent_environment_dialogue) -> None:
        pass
        # self.context.logger.warning(
        #     "cannot handle agent environment message of performative={} in dialogue={}.".format(
        #         agent_environment_message.performative, agent_environment_dialogue,
        #     )
        # )


class AgentMessageHandler(Handler):
    SUPPORTED_PROTOCOL = AgentAgentMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        :return: None
        """
        agent_agent_message = cast(AgentAgentMessage, message)

        agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues) # ??????????
        agent_agent_dialogue = cast(AgentAgentDialogue,
                                    agent_agent_dialogues.update(agent_agent_message))
        if agent_agent_dialogue is None:
            self._handle_unidentified_dialogue(agent_agent_message)
            return

        if agent_agent_message.performative == AgentAgentMessage.Performative.WATER_STATUS:
            self._handle_(agent_agent_message, agent_agent_dialogue)
        else:
            self._handle_invalid(agent_agent_message, agent_agent_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_unidentified_dialogue(self, agent_agent_message: AgentAgentMessage) -> None:
        """

        """
        # self.context.logger.info(
        #     "received invalid agent_agent message={}, unidentified dialogue.".format(agent_agent_message)
        # )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=agent_agent_message.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"Agent Environment Message": agent_agent_message.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_(self, agent_agent_message: AgentAgentMessage, agent_agent_dialogue):
        # Actual function where agent messages are used.
        pass

    def _handle_invalid(self, agent_agent_message: AgentAgentMessage, agent_agent_dialogue) -> None:
        pass
        # self.context.logger.warning(
        #     "cannot handle agent agent message of performative={} in dialogue={}.".format(
        #         agent_agent_message.performative, agent_agent_dialogue,
        #     )
        # )
