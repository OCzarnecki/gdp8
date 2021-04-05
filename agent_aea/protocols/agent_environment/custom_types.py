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

"""This module contains class representations corresponding to every custom type in the protocol specification."""


class Command:
    """This class represents an instance of Command."""

    def __init__(self, command_: str):
        """Initialise an instance of Command."""
        self.command = command_
        raise NotImplementedError

    @staticmethod
    def encode(command_protobuf_object, command_object: "Command") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the command_protobuf_object argument is matched with the instance of this class in the 'command_object' argument.

        :param command_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param command_object: an instance of this class to be encoded in the protocol buffer object.
        :return: None
        """
        raise NotImplementedError

    @classmethod
    def decode(cls, command_protobuf_object) -> "Command":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'command_protobuf_object' argument.

        :param command_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'command_protobuf_object' argument.
        """
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError
