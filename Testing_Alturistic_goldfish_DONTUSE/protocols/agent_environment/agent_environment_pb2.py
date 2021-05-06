# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent_environment.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="agent_environment.proto",
    package="aea.gdp8.agent_environment_communication.v0_1_0",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=b'\n\x17\x61gent_environment.proto\x12/aea.gdp8.agent_environment_communication.v0_1_0"\x8b\x04\n\x17\x41gentEnvironmentMessage\x12n\n\x06\x61\x63tion\x18\x05 \x01(\x0b\x32\\.aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Action_PerformativeH\x00\x12j\n\x04tick\x18\x06 \x01(\x0b\x32Z.aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_PerformativeH\x00\x1a\xdb\x01\n\x11Tick_Performative\x12\x12\n\ntile_water\x18\x01 \x01(\x05\x12\x13\n\x0bturn_number\x18\x02 \x01(\x05\x12\x13\n\x0b\x61gent_water\x18\x03 \x01(\x05\x12\x1a\n\x12north_neighbour_id\x18\x04 \x01(\t\x12\x19\n\x11\x65\x61st_neighbour_id\x18\x05 \x01(\t\x12\x1a\n\x12south_neighbour_id\x18\x06 \x01(\t\x12\x19\n\x11west_neighbour_id\x18\x07 \x01(\t\x12\x1a\n\x12movement_last_turn\x18\x08 \x01(\t\x1a&\n\x13\x41\x63tion_Performative\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\tB\x0e\n\x0cperformativeb\x06proto3',
)


_AGENTENVIRONMENTMESSAGE_TICK_PERFORMATIVE = _descriptor.Descriptor(
    name="Tick_Performative",
    full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="tile_water",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.tile_water",
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
        _descriptor.FieldDescriptor(
            name="turn_number",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.turn_number",
            index=1,
            number=2,
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
        _descriptor.FieldDescriptor(
            name="agent_water",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.agent_water",
            index=2,
            number=3,
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
        _descriptor.FieldDescriptor(
            name="north_neighbour_id",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.north_neighbour_id",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="east_neighbour_id",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.east_neighbour_id",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="south_neighbour_id",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.south_neighbour_id",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="west_neighbour_id",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.west_neighbour_id",
            index=6,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="movement_last_turn",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative.movement_last_turn",
            index=7,
            number=8,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
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
    serialized_start=325,
    serialized_end=544,
)

_AGENTENVIRONMENTMESSAGE_ACTION_PERFORMATIVE = _descriptor.Descriptor(
    name="Action_Performative",
    full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Action_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="command",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Action_Performative.command",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
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
    serialized_start=546,
    serialized_end=584,
)

_AGENTENVIRONMENTMESSAGE = _descriptor.Descriptor(
    name="AgentEnvironmentMessage",
    full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="action",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.action",
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
            name="tick",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.tick",
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
        _AGENTENVIRONMENTMESSAGE_TICK_PERFORMATIVE,
        _AGENTENVIRONMENTMESSAGE_ACTION_PERFORMATIVE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="performative",
            full_name="aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.performative",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=77,
    serialized_end=600,
)

_AGENTENVIRONMENTMESSAGE_TICK_PERFORMATIVE.containing_type = _AGENTENVIRONMENTMESSAGE
_AGENTENVIRONMENTMESSAGE_ACTION_PERFORMATIVE.containing_type = _AGENTENVIRONMENTMESSAGE
_AGENTENVIRONMENTMESSAGE.fields_by_name[
    "action"
].message_type = _AGENTENVIRONMENTMESSAGE_ACTION_PERFORMATIVE
_AGENTENVIRONMENTMESSAGE.fields_by_name[
    "tick"
].message_type = _AGENTENVIRONMENTMESSAGE_TICK_PERFORMATIVE
_AGENTENVIRONMENTMESSAGE.oneofs_by_name["performative"].fields.append(
    _AGENTENVIRONMENTMESSAGE.fields_by_name["action"]
)
_AGENTENVIRONMENTMESSAGE.fields_by_name[
    "action"
].containing_oneof = _AGENTENVIRONMENTMESSAGE.oneofs_by_name["performative"]
_AGENTENVIRONMENTMESSAGE.oneofs_by_name["performative"].fields.append(
    _AGENTENVIRONMENTMESSAGE.fields_by_name["tick"]
)
_AGENTENVIRONMENTMESSAGE.fields_by_name[
    "tick"
].containing_oneof = _AGENTENVIRONMENTMESSAGE.oneofs_by_name["performative"]
DESCRIPTOR.message_types_by_name["AgentEnvironmentMessage"] = _AGENTENVIRONMENTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AgentEnvironmentMessage = _reflection.GeneratedProtocolMessageType(
    "AgentEnvironmentMessage",
    (_message.Message,),
    {
        "Tick_Performative": _reflection.GeneratedProtocolMessageType(
            "Tick_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _AGENTENVIRONMENTMESSAGE_TICK_PERFORMATIVE,
                "__module__": "agent_environment_pb2"
                # @@protoc_insertion_point(class_scope:aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Tick_Performative)
            },
        ),
        "Action_Performative": _reflection.GeneratedProtocolMessageType(
            "Action_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _AGENTENVIRONMENTMESSAGE_ACTION_PERFORMATIVE,
                "__module__": "agent_environment_pb2"
                # @@protoc_insertion_point(class_scope:aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage.Action_Performative)
            },
        ),
        "DESCRIPTOR": _AGENTENVIRONMENTMESSAGE,
        "__module__": "agent_environment_pb2"
        # @@protoc_insertion_point(class_scope:aea.gdp8.agent_environment_communication.v0_1_0.AgentEnvironmentMessage)
    },
)
_sym_db.RegisterMessage(AgentEnvironmentMessage)
_sym_db.RegisterMessage(AgentEnvironmentMessage.Tick_Performative)
_sym_db.RegisterMessage(AgentEnvironmentMessage.Action_Performative)


# @@protoc_insertion_point(module_scope)
