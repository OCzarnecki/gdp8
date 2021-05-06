# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent_agent.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="agent_agent.proto",
    package="aea.gdp8.agent_agent_communication.v0_1_0",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=b'\n\x11\x61gent_agent.proto\x12)aea.gdp8.agent_agent_communication.v0_1_0"\xe1\x02\n\x11\x41gentAgentMessage\x12n\n\x0crequest_info\x18\x05 \x01(\x0b\x32V.aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Request_Info_PerformativeH\x00\x12n\n\x0cwater_status\x18\x06 \x01(\x0b\x32V.aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Water_Status_PerformativeH\x00\x1a*\n\x19Water_Status_Performative\x12\r\n\x05water\x18\x01 \x01(\x05\x1a\x30\n\x19Request_Info_Performative\x12\x13\n\x0bturn_number\x18\x01 \x01(\x05\x42\x0e\n\x0cperformativeb\x06proto3',
)


_AGENTAGENTMESSAGE_WATER_STATUS_PERFORMATIVE = _descriptor.Descriptor(
    name="Water_Status_Performative",
    full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Water_Status_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="water",
            full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Water_Status_Performative.water",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=310,
    serialized_end=352,
)

_AGENTAGENTMESSAGE_REQUEST_INFO_PERFORMATIVE = _descriptor.Descriptor(
    name="Request_Info_Performative",
    full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Request_Info_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="turn_number",
            full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Request_Info_Performative.turn_number",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=354,
    serialized_end=402,
)

_AGENTAGENTMESSAGE = _descriptor.Descriptor(
    name="AgentAgentMessage",
    full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="request_info",
            full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.request_info",
            index=0,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="water_status",
            full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.water_status",
            index=1,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[
        _AGENTAGENTMESSAGE_WATER_STATUS_PERFORMATIVE,
        _AGENTAGENTMESSAGE_REQUEST_INFO_PERFORMATIVE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="performative",
            full_name="aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.performative",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=65,
    serialized_end=418,
)

_AGENTAGENTMESSAGE_WATER_STATUS_PERFORMATIVE.containing_type = _AGENTAGENTMESSAGE
_AGENTAGENTMESSAGE_REQUEST_INFO_PERFORMATIVE.containing_type = _AGENTAGENTMESSAGE
_AGENTAGENTMESSAGE.fields_by_name[
    "request_info"
].message_type = _AGENTAGENTMESSAGE_REQUEST_INFO_PERFORMATIVE
_AGENTAGENTMESSAGE.fields_by_name[
    "water_status"
].message_type = _AGENTAGENTMESSAGE_WATER_STATUS_PERFORMATIVE
_AGENTAGENTMESSAGE.oneofs_by_name["performative"].fields.append(
    _AGENTAGENTMESSAGE.fields_by_name["request_info"]
)
_AGENTAGENTMESSAGE.fields_by_name[
    "request_info"
].containing_oneof = _AGENTAGENTMESSAGE.oneofs_by_name["performative"]
_AGENTAGENTMESSAGE.oneofs_by_name["performative"].fields.append(
    _AGENTAGENTMESSAGE.fields_by_name["water_status"]
)
_AGENTAGENTMESSAGE.fields_by_name[
    "water_status"
].containing_oneof = _AGENTAGENTMESSAGE.oneofs_by_name["performative"]
DESCRIPTOR.message_types_by_name["AgentAgentMessage"] = _AGENTAGENTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AgentAgentMessage = _reflection.GeneratedProtocolMessageType(
    "AgentAgentMessage",
    (_message.Message,),
    {
        "Water_Status_Performative": _reflection.GeneratedProtocolMessageType(
            "Water_Status_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _AGENTAGENTMESSAGE_WATER_STATUS_PERFORMATIVE,
                "__module__": "agent_agent_pb2"
                # @@protoc_insertion_point(class_scope:aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Water_Status_Performative)
            },
        ),
        "Request_Info_Performative": _reflection.GeneratedProtocolMessageType(
            "Request_Info_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _AGENTAGENTMESSAGE_REQUEST_INFO_PERFORMATIVE,
                "__module__": "agent_agent_pb2"
                # @@protoc_insertion_point(class_scope:aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage.Request_Info_Performative)
            },
        ),
        "DESCRIPTOR": _AGENTAGENTMESSAGE,
        "__module__": "agent_agent_pb2"
        # @@protoc_insertion_point(class_scope:aea.gdp8.agent_agent_communication.v0_1_0.AgentAgentMessage)
    },
)
_sym_db.RegisterMessage(AgentAgentMessage)
_sym_db.RegisterMessage(AgentAgentMessage.Water_Status_Performative)
_sym_db.RegisterMessage(AgentAgentMessage.Request_Info_Performative)


# @@protoc_insertion_point(module_scope)