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

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message


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

    class Performative(Message.Performative):
        """Performatives for the agent_environment protocol."""

        ACTION = "action"
        TICK = "tick"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"action", "tick"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "agent_water",
            "command",
            "dialogue_reference",
            "east_neighbour_id",
            "message_id",
            "movement_last_turn",
            "north_neighbour_id",
            "performative",
            "south_neighbour_id",
            "target",
            "tile_water",
            "turn_number",
            "west_neighbour_id",
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
    def command(self) -> str:
        """Get the 'command' content from the message."""
        enforce(self.is_set("command"), "'command' content is not set.")
        return cast(str, self.get("command"))

    @property
    def east_neighbour_id(self) -> str:
        """Get the 'east_neighbour_id' content from the message."""
        enforce(
            self.is_set("east_neighbour_id"), "'east_neighbour_id' content is not set."
        )
        return cast(str, self.get("east_neighbour_id"))

    @property
    def movement_last_turn(self) -> str:
        """Get the 'movement_last_turn' content from the message."""
        enforce(
            self.is_set("movement_last_turn"),
            "'movement_last_turn' content is not set.",
        )
        return cast(str, self.get("movement_last_turn"))

    @property
    def north_neighbour_id(self) -> str:
        """Get the 'north_neighbour_id' content from the message."""
        enforce(
            self.is_set("north_neighbour_id"),
            "'north_neighbour_id' content is not set.",
        )
        return cast(str, self.get("north_neighbour_id"))

    @property
    def south_neighbour_id(self) -> str:
        """Get the 'south_neighbour_id' content from the message."""
        enforce(
            self.is_set("south_neighbour_id"),
            "'south_neighbour_id' content is not set.",
        )
        return cast(str, self.get("south_neighbour_id"))

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
    def west_neighbour_id(self) -> str:
        """Get the 'west_neighbour_id' content from the message."""
        enforce(
            self.is_set("west_neighbour_id"), "'west_neighbour_id' content is not set."
        )
        return cast(str, self.get("west_neighbour_id"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the agent_environment protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, AgentEnvironmentMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == AgentEnvironmentMessage.Performative.TICK:
                expected_nb_of_contents = 8
                enforce(
                    type(self.tile_water) is int,
                    "Invalid type for content 'tile_water'. Expected 'int'. Found '{}'.".format(
                        type(self.tile_water)
                    ),
                )
                enforce(
                    type(self.turn_number) is int,
                    "Invalid type for content 'turn_number'. Expected 'int'. Found '{}'.".format(
                        type(self.turn_number)
                    ),
                )
                enforce(
                    type(self.agent_water) is int,
                    "Invalid type for content 'agent_water'. Expected 'int'. Found '{}'.".format(
                        type(self.agent_water)
                    ),
                )
                enforce(
                    isinstance(self.north_neighbour_id, str),
                    "Invalid type for content 'north_neighbour_id'. Expected 'str'. Found '{}'.".format(
                        type(self.north_neighbour_id)
                    ),
                )
                enforce(
                    isinstance(self.east_neighbour_id, str),
                    "Invalid type for content 'east_neighbour_id'. Expected 'str'. Found '{}'.".format(
                        type(self.east_neighbour_id)
                    ),
                )
                enforce(
                    isinstance(self.south_neighbour_id, str),
                    "Invalid type for content 'south_neighbour_id'. Expected 'str'. Found '{}'.".format(
                        type(self.south_neighbour_id)
                    ),
                )
                enforce(
                    isinstance(self.west_neighbour_id, str),
                    "Invalid type for content 'west_neighbour_id'. Expected 'str'. Found '{}'.".format(
                        type(self.west_neighbour_id)
                    ),
                )
                enforce(
                    isinstance(self.movement_last_turn, str),
                    "Invalid type for content 'movement_last_turn'. Expected 'str'. Found '{}'.".format(
                        type(self.movement_last_turn)
                    ),
                )
            elif self.performative == AgentEnvironmentMessage.Performative.ACTION:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.command, str),
                    "Invalid type for content 'command'. Expected 'str'. Found '{}'.".format(
                        type(self.command)
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
