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

"""Serialization module for agent_agent protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.gdp8.protocols.agent_agent import agent_agent_pb2
from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage


class AgentAgentSerializer(Serializer):
    """Serialization for the 'agent_agent' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'AgentAgent' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(AgentAgentMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        agent_agent_msg = agent_agent_pb2.AgentAgentMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == AgentAgentMessage.Performative.SENDER_REQUEST:
            performative = agent_agent_pb2.AgentAgentMessage.Sender_Request_Performative()  # type: ignore
            request = msg.request
            performative.request = request
            turn_number = msg.turn_number
            performative.turn_number = turn_number
            agent_agent_msg.sender_request.CopyFrom(performative)
        elif performative_id == AgentAgentMessage.Performative.RECEIVER_REPLY:
            performative = agent_agent_pb2.AgentAgentMessage.Receiver_Reply_Performative()  # type: ignore
            reply = msg.reply
            performative.reply = reply
            agent_agent_msg.receiver_reply.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = agent_agent_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'AgentAgent' message.

        :param obj: the bytes object.
        :return: the 'AgentAgent' message.
        """
        message_pb = ProtobufMessage()
        agent_agent_pb = agent_agent_pb2.AgentAgentMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        agent_agent_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = agent_agent_pb.WhichOneof("performative")
        performative_id = AgentAgentMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == AgentAgentMessage.Performative.SENDER_REQUEST:
            request = agent_agent_pb.sender_request.request
            performative_content["request"] = request
            turn_number = agent_agent_pb.sender_request.turn_number
            performative_content["turn_number"] = turn_number
        elif performative_id == AgentAgentMessage.Performative.RECEIVER_REPLY:
            reply = agent_agent_pb.receiver_reply.reply
            performative_content["reply"] = reply
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return AgentAgentMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
