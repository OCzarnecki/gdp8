# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 gdp8
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
This module contains the classes required for agent_environment dialogue management.

- AgentEnvironmentDialogue: The dialogue class maintains state of a dialogue and manages it.
- AgentEnvironmentDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, FrozenSet, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues

from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage


class AgentEnvironmentDialogue(Dialogue):
    """The agent_environment dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES = frozenset({AgentEnvironmentMessage.Performative.TICK})
    TERMINAL_PERFORMATIVES = frozenset({AgentEnvironmentMessage.Performative.ACTION})
    VALID_REPLIES = {
        AgentEnvironmentMessage.Performative.ACTION: frozenset(),
        AgentEnvironmentMessage.Performative.TICK: frozenset(
            {AgentEnvironmentMessage.Performative.ACTION}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a agent_environment dialogue."""

        AGENT = "agent"
        ENVIRONMENT = "environment"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a agent_environment dialogue."""

        SUCCESS = 0

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[AgentEnvironmentMessage] = AgentEnvironmentMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :return: None
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class AgentEnvironmentDialogues(Dialogues, ABC):
    """This class keeps track of all agent_environment dialogues."""

    END_STATES = frozenset({AgentEnvironmentDialogue.EndState.SUCCESS})

    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[AgentEnvironmentDialogue] = AgentEnvironmentDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :return: None
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=AgentEnvironmentMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
