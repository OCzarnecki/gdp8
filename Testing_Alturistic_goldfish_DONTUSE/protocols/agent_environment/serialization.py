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

"""Serialization module for agent_environment protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.gdp8.protocols.agent_environment import agent_environment_pb2
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage


class AgentEnvironmentSerializer(Serializer):
    """Serialization for the 'agent_environment' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'AgentEnvironment' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(AgentEnvironmentMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        agent_environment_msg = agent_environment_pb2.AgentEnvironmentMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == AgentEnvironmentMessage.Performative.TICK:
            performative = agent_environment_pb2.AgentEnvironmentMessage.Tick_Performative()  # type: ignore
            tile_water = msg.tile_water
            performative.tile_water = tile_water
            turn_number = msg.turn_number
            performative.turn_number = turn_number
            agent_water = msg.agent_water
            performative.agent_water = agent_water
            north_neighbour_id = msg.north_neighbour_id
            performative.north_neighbour_id = north_neighbour_id
            east_neighbour_id = msg.east_neighbour_id
            performative.east_neighbour_id = east_neighbour_id
            south_neighbour_id = msg.south_neighbour_id
            performative.south_neighbour_id = south_neighbour_id
            west_neighbour_id = msg.west_neighbour_id
            performative.west_neighbour_id = west_neighbour_id
            movement_last_turn = msg.movement_last_turn
            performative.movement_last_turn = movement_last_turn
            agent_environment_msg.tick.CopyFrom(performative)
        elif performative_id == AgentEnvironmentMessage.Performative.ACTION:
            performative = agent_environment_pb2.AgentEnvironmentMessage.Action_Performative()  # type: ignore
            command = msg.command
            performative.command = command
            agent_environment_msg.action.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = agent_environment_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'AgentEnvironment' message.

        :param obj: the bytes object.
        :return: the 'AgentEnvironment' message.
        """
        message_pb = ProtobufMessage()
        agent_environment_pb = agent_environment_pb2.AgentEnvironmentMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        agent_environment_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = agent_environment_pb.WhichOneof("performative")
        performative_id = AgentEnvironmentMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == AgentEnvironmentMessage.Performative.TICK:
            tile_water = agent_environment_pb.tick.tile_water
            performative_content["tile_water"] = tile_water
            turn_number = agent_environment_pb.tick.turn_number
            performative_content["turn_number"] = turn_number
            agent_water = agent_environment_pb.tick.agent_water
            performative_content["agent_water"] = agent_water
            north_neighbour_id = agent_environment_pb.tick.north_neighbour_id
            performative_content["north_neighbour_id"] = north_neighbour_id
            east_neighbour_id = agent_environment_pb.tick.east_neighbour_id
            performative_content["east_neighbour_id"] = east_neighbour_id
            south_neighbour_id = agent_environment_pb.tick.south_neighbour_id
            performative_content["south_neighbour_id"] = south_neighbour_id
            west_neighbour_id = agent_environment_pb.tick.west_neighbour_id
            performative_content["west_neighbour_id"] = west_neighbour_id
            movement_last_turn = agent_environment_pb.tick.movement_last_turn
            performative_content["movement_last_turn"] = movement_last_turn
        elif performative_id == AgentEnvironmentMessage.Performative.ACTION:
            command = agent_environment_pb.action.command
            performative_content["command"] = command
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return AgentEnvironmentMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
