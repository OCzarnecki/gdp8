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

"""This module contains the support resources for the agent_environment protocol."""

from gdp.agent_aea.protocols.agent_environment.message import AgentEnvironmentMessage
from gdp.agent_aea.protocols.agent_environment.serialization import (
    AgentEnvironmentSerializer,
)


AgentEnvironmentMessage.serializer = AgentEnvironmentSerializer
