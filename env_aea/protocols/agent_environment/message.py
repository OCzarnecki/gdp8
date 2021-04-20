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

"""This module contains agent_environment's message definition."""

import logging
from typing import Any, FrozenSet, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message

from packages.gdp8.protocols.agent_environment.custom_types import (
    Command as CustomCommand,
)


_default_logger = logging.getLogger(
    "aea.packages.gdp8.protocols.agent_environment.message"
)

DEFAULT_BODY_SIZE = 4


class AgentEnvironmentMessage(Message):
    """Agent-environment messages"""

    protocol_id = PublicId.from_str("gdp8/agent_environment:0.1.0")
    protocol_specification_id = PublicId.from_str(
        "gdp8/agent_environment_communication:0.1.0"
    )

    Command = CustomCommand

    class Performative(Message.Performative):
        """Performatives for the agent_environment protocol."""

        ACTION = "action"
        TICK = "tick"
        CANCELLED ="cancelled"
        REGISTER = "register"
        UNREGISTER = "unregister"
        AGENT_ENV_ERROR ="agent_env_error"



        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "action", 
        "tick", 
        "cancelled", 
        "register", 
        "unregister",
        "agent_env_error",
        }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "agent_water",
            "command",
            "dialogue_reference",
            "message_id",
            "neighbour_ids",
            "performative",
            "target",
            "tile_water",
            "turn_number",
            "water_quantity",
            "error_description",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of AgentEnvironmentMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=AgentEnvironmentMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(AgentEnvironmentMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def agent_water(self) -> int:
        """Get the 'agent_water' content from the message."""
        enforce(self.is_set("agent_water"), "'agent_water' content is not set.")
        return cast(int, self.get("agent_water"))

    @property
    def command(self) -> CustomCommand:
        """Get the 'command' content from the message."""
        enforce(self.is_set("command"), "'command' content is not set.")
        return cast(CustomCommand, self.get("command"))

    @property
    def neighbour_ids(self) -> FrozenSet[int]:
        """Get the 'neighbour_ids' content from the message."""
        enforce(self.is_set("neighbour_ids"), "'neighbour_ids' content is not set.")
        return cast(FrozenSet[int], self.get("neighbour_ids"))

    @property
    def tile_water(self) -> int:
        """Get the 'tile_water' content from the message."""
        enforce(self.is_set("tile_water"), "'tile_water' content is not set.")
        return cast(int, self.get("tile_water"))

    @property
    def turn_number(self) -> int:
        """Get the 'turn_number' content from the message."""
        enforce(self.is_set("turn_number"), "'turn_number' content is not set.")
        return cast(int, self.get("turn_number"))

    @property
    def water_quantity(self) -> int:
        """Get the 'water_quantity' content from the message."""
        enforce(self.is_set("water_quantity"), "'water_quantity' content is not set.")
        return cast(int, self.get("water_quantity"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the agent_environment protocol."""
        try:
            enforce(
                type(self.dialogue_reference) == tuple,
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                type(self.dialogue_reference[0]) == str,
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                type(self.dialogue_reference[1]) == str,
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) == int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) == int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                type(self.performative) == AgentEnvironmentMessage.Performative,
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == AgentEnvironmentMessage.Performative.TICK:
                expected_nb_of_contents = 4
                enforce(
                    type(self.tile_water) == int,
                    "Invalid type for content 'tile_water'. Expected 'int'. Found '{}'.".format(
                        type(self.tile_water)
                    ),
                )
                enforce(
                    type(self.turn_number) == int,
                    "Invalid type for content 'turn_number'. Expected 'int'. Found '{}'.".format(
                        type(self.turn_number)
                    ),
                )
                enforce(
                    type(self.agent_water) == int,
                    "Invalid type for content 'agent_water'. Expected 'int'. Found '{}'.".format(
                        type(self.agent_water)
                    ),
                )
                enforce(
                    type(self.neighbour_ids) == frozenset,
                    "Invalid type for content 'neighbour_ids'. Expected 'frozenset'. Found '{}'.".format(
                        type(self.neighbour_ids)
                    ),
                )
                enforce(
                    all(type(element) == int for element in self.neighbour_ids),
                    "Invalid type for frozenset elements in content 'neighbour_ids'. Expected 'int'.",
                )
            elif self.performative == AgentEnvironmentMessage.Performative.ACTION:
                expected_nb_of_contents = 2
                enforce(
                    type(self.command) == CustomCommand,
                    "Invalid type for content 'command'. Expected 'Command'. Found '{}'.".format(
                        type(self.command)
                    ),
                )
                enforce(
                    type(self.water_quantity) == int,
                    "Invalid type for content 'water_quantity'. Expected 'int'. Found '{}'.".format(
                        type(self.water_quantity)
                    ),
                )

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                        self.target
                    ),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
