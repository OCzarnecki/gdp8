# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: acn_message.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="acn_message.proto",
    package="dhtnode",
    syntax="proto3",
    serialized_pb=_b(
        '\n\x11\x61\x63n_message.proto\x12\x07\x64htnode"\xac\x01\n\x0b\x41gentRecord\x12\x12\n\nservice_id\x18\x01 \x01(\t\x12\x11\n\tledger_id\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\x12\x12\n\npublic_key\x18\x04 \x01(\t\x12\x17\n\x0fpeer_public_key\x18\x05 \x01(\t\x12\x11\n\tsignature\x18\x06 \x01(\t\x12\x12\n\nnot_before\x18\x07 \x01(\t\x12\x11\n\tnot_after\x18\x08 \x01(\t"0\n\x08Register\x12$\n\x06record\x18\x01 \x01(\x0b\x32\x14.dhtnode.AgentRecord"&\n\rLookupRequest\x12\x15\n\ragent_address\x18\x01 \x01(\t"<\n\x0eLookupResponse\x12*\n\x0c\x61gent_record\x18\x01 \x01(\x0b\x32\x14.dhtnode.AgentRecord"B\n\x0b\x41\x65\x61\x45nvelope\x12\r\n\x05\x65nvel\x18\x01 \x01(\x0c\x12$\n\x06record\x18\x02 \x01(\x0b\x32\x14.dhtnode.AgentRecord"\xed\x02\n\x06Status\x12%\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x17.dhtnode.Status.ErrCode\x12\x0c\n\x04msgs\x18\x02 \x03(\t"\xad\x02\n\x07\x45rrCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x1d\n\x19\x45RROR_UNSUPPORTED_VERSION\x10\x01\x12\x1c\n\x18\x45RROR_UNEXPECTED_PAYLOAD\x10\x02\x12\x11\n\rERROR_GENERIC\x10\x03\x12\x17\n\x13\x45RROR_SERIALIZATION\x10\x04\x12\x1d\n\x19\x45RROR_WRONG_AGENT_ADDRESS\x10\n\x12\x1a\n\x16\x45RROR_WRONG_PUBLIC_KEY\x10\x0b\x12\x17\n\x13\x45RROR_INVALID_PROOF\x10\x0c\x12\x1c\n\x18\x45RROR_UNSUPPORTED_LEGDER\x10\r\x12\x1f\n\x1b\x45RROR_UNKNOWN_AGENT_ADDRESS\x10\x14\x12\x19\n\x15\x45RROR_AGENT_NOT_READY\x10\x15"\x86\x02\n\nAcnMessage\x12\x0f\n\x07version\x18\x01 \x01(\t\x12!\n\x06status\x18\x02 \x01(\x0b\x32\x0f.dhtnode.StatusH\x00\x12%\n\x08register\x18\x03 \x01(\x0b\x32\x11.dhtnode.RegisterH\x00\x12\x30\n\x0elookup_request\x18\x04 \x01(\x0b\x32\x16.dhtnode.LookupRequestH\x00\x12\x32\n\x0flookup_response\x18\x05 \x01(\x0b\x32\x17.dhtnode.LookupResponseH\x00\x12,\n\x0c\x61\x65\x61_envelope\x18\x06 \x01(\x0b\x32\x14.dhtnode.AeaEnvelopeH\x00\x42\t\n\x07payloadb\x06proto3'
    ),
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


_STATUS_ERRCODE = _descriptor.EnumDescriptor(
    name="ErrCode",
    full_name="dhtnode.Status.ErrCode",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="SUCCESS", index=0, number=0, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_UNSUPPORTED_VERSION", index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_UNEXPECTED_PAYLOAD", index=2, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_GENERIC", index=3, number=3, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_SERIALIZATION", index=4, number=4, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_WRONG_AGENT_ADDRESS",
            index=5,
            number=10,
            options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_WRONG_PUBLIC_KEY", index=6, number=11, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_INVALID_PROOF", index=7, number=12, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_UNSUPPORTED_LEGDER", index=8, number=13, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_UNKNOWN_AGENT_ADDRESS",
            index=9,
            number=20,
            options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_AGENT_NOT_READY", index=10, number=21, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=490,
    serialized_end=791,
)
_sym_db.RegisterEnumDescriptor(_STATUS_ERRCODE)


_AGENTRECORD = _descriptor.Descriptor(
    name="AgentRecord",
    full_name="dhtnode.AgentRecord",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="service_id",
            full_name="dhtnode.AgentRecord.service_id",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="ledger_id",
            full_name="dhtnode.AgentRecord.ledger_id",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="dhtnode.AgentRecord.address",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="public_key",
            full_name="dhtnode.AgentRecord.public_key",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="peer_public_key",
            full_name="dhtnode.AgentRecord.peer_public_key",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="signature",
            full_name="dhtnode.AgentRecord.signature",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="not_before",
            full_name="dhtnode.AgentRecord.not_before",
            index=6,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="not_after",
            full_name="dhtnode.AgentRecord.not_after",
            index=7,
            number=8,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=31,
    serialized_end=203,
)


_REGISTER = _descriptor.Descriptor(
    name="Register",
    full_name="dhtnode.Register",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="record",
            full_name="dhtnode.Register.record",
            index=0,
            number=1,
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
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=205,
    serialized_end=253,
)


_LOOKUPREQUEST = _descriptor.Descriptor(
    name="LookupRequest",
    full_name="dhtnode.LookupRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="agent_address",
            full_name="dhtnode.LookupRequest.agent_address",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=255,
    serialized_end=293,
)


_LOOKUPRESPONSE = _descriptor.Descriptor(
    name="LookupResponse",
    full_name="dhtnode.LookupResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="agent_record",
            full_name="dhtnode.LookupResponse.agent_record",
            index=0,
            number=1,
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
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=295,
    serialized_end=355,
)


_AEAENVELOPE = _descriptor.Descriptor(
    name="AeaEnvelope",
    full_name="dhtnode.AeaEnvelope",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="envel",
            full_name="dhtnode.AeaEnvelope.envel",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="record",
            full_name="dhtnode.AeaEnvelope.record",
            index=1,
            number=2,
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
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=357,
    serialized_end=423,
)


_STATUS = _descriptor.Descriptor(
    name="Status",
    full_name="dhtnode.Status",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="code",
            full_name="dhtnode.Status.code",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="msgs",
            full_name="dhtnode.Status.msgs",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_STATUS_ERRCODE,],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=426,
    serialized_end=791,
)


_ACNMESSAGE = _descriptor.Descriptor(
    name="AcnMessage",
    full_name="dhtnode.AcnMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="version",
            full_name="dhtnode.AcnMessage.version",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="status",
            full_name="dhtnode.AcnMessage.status",
            index=1,
            number=2,
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
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="register",
            full_name="dhtnode.AcnMessage.register",
            index=2,
            number=3,
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
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="lookup_request",
            full_name="dhtnode.AcnMessage.lookup_request",
            index=3,
            number=4,
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
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="lookup_response",
            full_name="dhtnode.AcnMessage.lookup_response",
            index=4,
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
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="aea_envelope",
            full_name="dhtnode.AcnMessage.aea_envelope",
            index=5,
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
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="payload",
            full_name="dhtnode.AcnMessage.payload",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=794,
    serialized_end=1056,
)

_REGISTER.fields_by_name["record"].message_type = _AGENTRECORD
_LOOKUPRESPONSE.fields_by_name["agent_record"].message_type = _AGENTRECORD
_AEAENVELOPE.fields_by_name["record"].message_type = _AGENTRECORD
_STATUS.fields_by_name["code"].enum_type = _STATUS_ERRCODE
_STATUS_ERRCODE.containing_type = _STATUS
_ACNMESSAGE.fields_by_name["status"].message_type = _STATUS
_ACNMESSAGE.fields_by_name["register"].message_type = _REGISTER
_ACNMESSAGE.fields_by_name["lookup_request"].message_type = _LOOKUPREQUEST
_ACNMESSAGE.fields_by_name["lookup_response"].message_type = _LOOKUPRESPONSE
_ACNMESSAGE.fields_by_name["aea_envelope"].message_type = _AEAENVELOPE
_ACNMESSAGE.oneofs_by_name["payload"].fields.append(
    _ACNMESSAGE.fields_by_name["status"]
)
_ACNMESSAGE.fields_by_name["status"].containing_oneof = _ACNMESSAGE.oneofs_by_name[
    "payload"
]
_ACNMESSAGE.oneofs_by_name["payload"].fields.append(
    _ACNMESSAGE.fields_by_name["register"]
)
_ACNMESSAGE.fields_by_name["register"].containing_oneof = _ACNMESSAGE.oneofs_by_name[
    "payload"
]
_ACNMESSAGE.oneofs_by_name["payload"].fields.append(
    _ACNMESSAGE.fields_by_name["lookup_request"]
)
_ACNMESSAGE.fields_by_name[
    "lookup_request"
].containing_oneof = _ACNMESSAGE.oneofs_by_name["payload"]
_ACNMESSAGE.oneofs_by_name["payload"].fields.append(
    _ACNMESSAGE.fields_by_name["lookup_response"]
)
_ACNMESSAGE.fields_by_name[
    "lookup_response"
].containing_oneof = _ACNMESSAGE.oneofs_by_name["payload"]
_ACNMESSAGE.oneofs_by_name["payload"].fields.append(
    _ACNMESSAGE.fields_by_name["aea_envelope"]
)
_ACNMESSAGE.fields_by_name[
    "aea_envelope"
].containing_oneof = _ACNMESSAGE.oneofs_by_name["payload"]
DESCRIPTOR.message_types_by_name["AgentRecord"] = _AGENTRECORD
DESCRIPTOR.message_types_by_name["Register"] = _REGISTER
DESCRIPTOR.message_types_by_name["LookupRequest"] = _LOOKUPREQUEST
DESCRIPTOR.message_types_by_name["LookupResponse"] = _LOOKUPRESPONSE
DESCRIPTOR.message_types_by_name["AeaEnvelope"] = _AEAENVELOPE
DESCRIPTOR.message_types_by_name["Status"] = _STATUS
DESCRIPTOR.message_types_by_name["AcnMessage"] = _ACNMESSAGE

AgentRecord = _reflection.GeneratedProtocolMessageType(
    "AgentRecord",
    (_message.Message,),
    dict(
        DESCRIPTOR=_AGENTRECORD,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.AgentRecord)
    ),
)
_sym_db.RegisterMessage(AgentRecord)

Register = _reflection.GeneratedProtocolMessageType(
    "Register",
    (_message.Message,),
    dict(
        DESCRIPTOR=_REGISTER,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.Register)
    ),
)
_sym_db.RegisterMessage(Register)

LookupRequest = _reflection.GeneratedProtocolMessageType(
    "LookupRequest",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LOOKUPREQUEST,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.LookupRequest)
    ),
)
_sym_db.RegisterMessage(LookupRequest)

LookupResponse = _reflection.GeneratedProtocolMessageType(
    "LookupResponse",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LOOKUPRESPONSE,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.LookupResponse)
    ),
)
_sym_db.RegisterMessage(LookupResponse)

AeaEnvelope = _reflection.GeneratedProtocolMessageType(
    "AeaEnvelope",
    (_message.Message,),
    dict(
        DESCRIPTOR=_AEAENVELOPE,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.AeaEnvelope)
    ),
)
_sym_db.RegisterMessage(AeaEnvelope)

Status = _reflection.GeneratedProtocolMessageType(
    "Status",
    (_message.Message,),
    dict(
        DESCRIPTOR=_STATUS,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.Status)
    ),
)
_sym_db.RegisterMessage(Status)

AcnMessage = _reflection.GeneratedProtocolMessageType(
    "AcnMessage",
    (_message.Message,),
    dict(
        DESCRIPTOR=_ACNMESSAGE,
        __module__="acn_message_pb2"
        # @@protoc_insertion_point(class_scope:dhtnode.AcnMessage)
    ),
)
_sym_db.RegisterMessage(AcnMessage)


# @@protoc_insertion_point(module_scope)
