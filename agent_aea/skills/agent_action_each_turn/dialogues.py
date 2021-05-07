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

"""
This module contains the classes required for dialogue management.
- DefaultDialogue: The dialogue class maintains state of a dialogue of type default and manages it.
- DefaultDialogues: The dialogues class keeps track of all dialogues of type default.
- AgentEnvironmentDialogue: The dialogue class maintains state of a dialogue of type agent_environment and manages it.
- AgentEnvironmentDialogues: The dialogues class keeps track of all dialogues of type agent_environment.
- AgentAgentDialogue: The dialogue class maintains state of a dialogue of type agent_agent and manages it.
- AgentAgentDialogues: The dialogues class keeps track of all dialogues of type agent_agent.
"""
from typing import Any

from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue
from aea.skills.base import Model

from packages.fetchai.protocols.default.dialogues import (
    DefaultDialogue as BaseDefaultDialogue,
)
from packages.fetchai.protocols.default.dialogues import (
    DefaultDialogues as BaseDefaultDialogues,
)
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogue as BaseAgentEnvironmentDialogue
from packages.gdp8.protocols.agent_environment.dialogues import AgentEnvironmentDialogues as BaseAgentEnvironmentDialogues

from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogue as BaseAgentAgentDialogue
from packages.gdp8.protocols.agent_agent.dialogues import AgentAgentDialogues as BaseAgentAgentDialogues

DefaultDialogue = BaseDefaultDialogue


class DefaultDialogues(Model, BaseDefaultDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.
        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message
            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return DefaultDialogue.Role.AGENT

        BaseDefaultDialogues.__init__(
            self,
            self_address=self.context.agent_address,
            role_from_first_message=role_from_first_message,
        )


AgentEnvironmentDialogue = BaseAgentEnvironmentDialogue


class AgentEnvironmentDialogues(Model, BaseAgentEnvironmentDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.
        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message
            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return AgentEnvironmentDialogue.Role.AGENT

        BaseAgentEnvironmentDialogues.__init__(
            self,
            self_address=self.context.agent_address,
            role_from_first_message=role_from_first_message,
        )


AgentAgentDialogue = BaseAgentAgentDialogue


class AgentAgentDialogues(Model, BaseAgentAgentDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.
        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message
            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return AgentAgentDialogue.Role.AGENT  # INFO_REQUESTER?? COULD BE EITHER ONE?

        BaseAgentAgentDialogues.__init__(
            self,
            self_address=self.context.agent_address,
            role_from_first_message=role_from_first_message,
        )
