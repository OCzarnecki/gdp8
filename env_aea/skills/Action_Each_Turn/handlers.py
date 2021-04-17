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

from gdp.agent_aea.protocols.agent_environment.message import AgentEnvironmentMessage
from gdp.agent_aea.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues

from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler


from gdp.agent_aea.protocols.default.message import DefaultMessage
from gdp.agent_aea.protocols.default.dialogues import DefaultDialogues
from gdp.agent_aea.skills.Action_Each_Turn.strategy import BasicStrategy


class MyScaffoldHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = AgentEnvironmentMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        raise NotImplementedError

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope. Containing the reply of an agent to the tick message. 
        The reply to a tick message is an action: command: ct:**, water_quantity: pt:int
        Where the command will be one of the following: NOP, SEND_WATER, RECEIVE_WATER
        **The type of the command is undefined yet

        :param message: the message
        :return: None
        """
        agent_environment_message = cast(AgentEnvironmentMessage, message)

        agent_environment_dialogues = cast(AgentEnvironmentDialogues,
                                           self.context.agent_environment_dialogues)  # ??????????
        agent_environment_dialogue = cast(AgentEnvironmentDialogue,
                                          agent_environment_dialogues.update(agent_environment_message))
        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_environment_message)
            return

        if agent_environment_message.performative == AgentEnvironmentMessage.Performative.ACTION:
            self._handle_(agent_environment_message, agent_environment_dialogue)
        #else:
        #   self._handle_invalid(agent_environment_message, agent_environment_dialogue)


    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        raise NotImplementedError


    def _handle_unidentified_dialogue(self, agent_environment_message: AgentEnvironmentMessage) -> None:
        """
        Taken from the agent_aea handler, not tested yet.
        """
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
        # update the environment with the action taken by the agent
        # Agents reply should only be handled if they concern the current turn. 
        assert(agent_environment_message.turn_number == self.context.environment.turn_number)
        self.context.environment.save_action(agent_environment_dialogue.sender, agent_environment_message.action, agent_environment_message.water_content)
        
    def _handle_invalid(self, agent_environment_message: AgentEnvironmentMessage, agent_environment_dialogue) -> None:
        pass