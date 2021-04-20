# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
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

from typing import Optional, Tuple, cast

from aea.common import Address
from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler
from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.tac_participation.dialogues import (
    OefSearchDialogue,
    OefSearchDialogues,
)
from gdp.agent_aea.protocols.default.message import DefaultMessage
from gdp.agent_aea.protocols.default.dialogues import DefaultDialogues
from gdp.agent_aea.protocols.agent_agent.message import AgentAgentMessage
from gdp.agent_aea.protocols.agent_agent.dialogues import AgentAgentDialogue, AgentAgentDialogues
from gdp.agent_aea.protocols.agent_environment.message import AgentEnvironmentMessage
from gdp.agent_aea.protocols.agent_environment.dialogues import AgentEnvironmentDialogue, AgentEnvironmentDialogues

from gdp.agent_aea.skills.Action_Each_Turn.strategy import BasicStrategy
from gdp.env_aea.skills.Action_Each_Turn.environment import Environment, Phase



# Handler will Update my model (strategy class) depending on what it has received
# Unimplemented: self.context.agent_environment_dialogues, self.context.default_dialogues

class OefSearchHandler(Handler):
    """This class handles oef messages."""

    SUPPORTED_PROTOCOL = OefSearchMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the handler setup.
        :return: None
        """

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.
        :param message: the message
        :return: None
        """
        oef_search_msg = cast(OefSearchMessage, message)

        # recover dialogue
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_dialogue = cast(
            Optional[OefSearchDialogue], oef_search_dialogues.update(oef_search_msg)
        )
        if oef_search_dialogue is None:
            self._handle_unidentified_dialogue(oef_search_msg)
            return

        # handle message
        if oef_search_msg.performative == OefSearchMessage.Performative.SEARCH_RESULT:
            self._on_search_result(oef_search_msg, oef_search_dialogue)
        elif oef_search_msg.performative == OefSearchMessage.Performative.OEF_ERROR:
            self._on_oef_error(oef_search_msg, oef_search_dialogue)
        else:
            self._handle_invalid(oef_search_msg, oef_search_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.
        :return: None
        """

    def _handle_unidentified_dialogue(self, oef_search_msg: OefSearchMessage) -> None:
        """
        Handle an unidentified dialogue.
        :param msg: the message
        """
        self.context.logger.warning(
            "received invalid oef_search message={}, unidentified dialogue.".format(
                oef_search_msg
            )
        )

    def _on_oef_error(
        self, oef_search_msg: OefSearchMessage, oef_search_dialogue: OefSearchDialogue
    ) -> None:
        """
        Handle an OEF error message.
        :param oef_search_msg: the oef search msg
        :param oef_search_dialogue: the dialogue
        :return: None
        """
        self.context.logger.warning(
            "received OEF Search error: dialogue_reference={}, oef_error_operation={}".format(
                oef_search_dialogue.dialogue_label.dialogue_reference,
                oef_search_msg.oef_error_operation,
            )
        )

    def _on_search_result(
        self, oef_search_msg: OefSearchMessage, oef_search_dialogue: OefSearchDialogue
    ) -> None:
        """
        Split the search results from the OEF search node.
        :param oef_search_msg: the search result
        :param oef_search_dialogue: the dialogue
        :return: None
        """
        self.context.logger.debug(
            "on search result: dialogue_reference={} agents={}".format(
                oef_search_dialogue.dialogue_label.dialogue_reference,
                oef_search_msg.agents,
            )
        )
        self._on_controller_search_result(oef_search_msg.agents)

    def _handle_invalid(
        self, oef_search_msg: OefSearchMessage, oef_search_dialogue: OefSearchDialogue
    ) -> None:
        """
        Handle an oef search message.
        :param oef_search_msg: the oef search message
        :param oef_search_dialogue: the dialogue
        :return: None
        """
        self.context.logger.warning(
            "cannot handle oef_search message of performative={} in dialogue={}.".format(
                oef_search_msg.performative, oef_search_dialogue,
            )
        )

    def _on_controller_search_result(
        self, agent_addresses: Tuple[Address, ...]
    ) -> None:
        """
        Process the search result for a controller.
        :param agent_addresses: list of agent addresses
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        if environment.phase.value != Phase.PRE_SIMULATION.value:
            self.context.logger.debug(
                "ignoring controller search result, the simulation as already started."
            )
            return

        if len(agent_addresses) == 0:
            self.context.logger.info("couldn't find the environment. Retrying...")
        elif len(agent_addresses) > 1:
            self.context.logger.warning(
                "found more than one environment. Retrying..."
            )
        else:
            self.context.logger.info("found the environment. Registering...")
            environment_addr = agent_addresses[0]
            self._register_to_env(environment_addr)

    def _register_to_env(self, environment_addr: Address) -> None:
        """
        Register to active environment.
        :param environment_addr: the address of the environment.
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        environment.update_expected_environment_addr(environment_addr)##
        environment.update_environment_phase(Phase.SIMULATION_REGISTRATION)##
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        agent_env_msg, agent_environment_dialogue = agent_environment_dialogues.create(
            counterparty=environment_addr,
            performative=AgentEnvironmentMessage.Performative.REGISTER,
            agent_name=self.context.agent_name,## do we have a variable for the agent name? what is its use?
        )
        agent_environment_dialogue = cast(AgentEnvironmentDialogue, agent_environment_dialogue)
        environment.agent_environment_dialogue = agent_environment_dialogue
        self.context.outbox.put_message(message=agent_env_msg)
        self.context.behaviours.env_search.is_active = False## Do we need to do something particular to add behaviour to the context?
        
class EnvironmentMessageHandler(Handler):
    """This class handles oef messages, from the environment."""

    SUPPORTED_PROTOCOL = AgentEnvironmentMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        agent_env_msg = cast(AgentEnvironmentMessage, message)

        #recover dialogue
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        agent_environment_dialogue = cast(AgentEnvironmentDialogue, agent_environment_dialogues.update(agent_env_msg))
        if agent_environment_dialogue is None:
            self._handle_unidentified_dialogue(agent_env_msg)
            return

        #handle message
        environment = cast(Environment, self.context.environment)
        self.context.logger.debug(
            "handling environment response. performative={}".format(agent_env_msg.performative)
        )
        if agent_env_msg.sender != environment.expected_controller_addr:
            raise ValueError(
                "The sender of the message is not the environment agent we registered with."
            )

        if agent_env_msg.performative == AgentEnvironmentMessage.Performative.TICK:
            self._on_tick(agent_env_msg, agent_environment_dialogue)
        else:
            self._handle_invalid(agent_env_msg, agent_environment_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """

    def _handle_unidentified_dialogue(self, agent_env_msg: AgentEnvironmentMessage) -> None:
        """
        Handle an unidentified dialogue.
        :param agent_env_msg: the message
        """
        self.context.logger.warning(
            "received invalid environment message={}, unidentified dialogue.".format(agent_env_msg)
        )

    def _on_tick(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue):
        """ 
        Handle a tick message from the environment from an identified dialogue.
        
        :param agent_env_msg: the agent environment message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        # Update my_model to get ready for next round
        self.context.logger.info(
            "received a tick message from the environment."
            )

        strategy = cast(BasicStrategy, self.context.strategy)
        strategy.receive_agent_env_info(agent_env_msg, agent_environment_dialogue)

    def _handle_invalid(self, agent_env_msg: AgentEnvironmentMessage, agent_environment_dialogue) -> None:
        """
        Handle an oef search message.

        :param agent_env_msg: the agent environmet message
        :param agent_environment_dialogue: the agent environment dialogue
        :return: None
        """
        self.context.logger.warning(
            "cannot handle environment message of performative={} in dialogue={}.".format(
                agent_env_msg.performative, agent_environment_dialogue
            )
        )

class AgentMessageHandler(Handler):
    SUPPORTED_PROTOCOL = AgentAgentMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        :return: None
        """
        agent_agent_message = cast(AgentAgentMessage, message)

        agent_agent_dialogues = cast(AgentAgentDialogues, self.context.agent_agent_dialogues)  # ??????????
        agent_agent_dialogue = cast(AgentAgentDialogue,
                                    agent_agent_dialogues.update(agent_agent_message))
        if agent_agent_dialogue is None:
            self._handle_unidentified_dialogue(agent_agent_message)
            return

        if agent_agent_message.performative == AgentAgentMessage.Performative.WATER_STATUS:
            # water status returned
            self._handle_returned_water_info(agent_agent_message, agent_agent_dialogue)
        elif agent_agent_message.performative == AgentAgentMessage.Performative.REQUEST_INFO:
            # water status asked
            self._handle_water_query(agent_agent_message, agent_agent_dialogue)
        else:
            self._handle_invalid(agent_agent_message, agent_agent_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_unidentified_dialogue(self, agent_agent_message: AgentAgentMessage) -> None:
        """

        """
        # self.context.logger.info(
        #     "received invalid agent_agent message={}, unidentified dialogue.".format(agent_agent_message)
        # )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=agent_agent_message.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"Agent Environment Message": agent_agent_message.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_returned_water_info(self, agent_agent_message: AgentAgentMessage, agent_agent_dialogue):
        # Actual function where agent messages are used.
        strategy = cast(BasicStrategy, self.context.strategy)
        # Info received. returns whether we can go to make_decision (may be on waiting list since last round not over)
        # True = Go on, False = stop
        strategy.receive_agent_agent_info(agent_agent_message)

    def _handle_water_query(self, agent_agent_message: AgentAgentMessage, agent_agent_dialogue):
        strategy = cast(BasicStrategy, self.context.strategy)
        strategy.agent_message_asking_for_my_water.append(
            [agent_agent_message, agent_agent_dialogue]
        )

    def _handle_invalid(self, agent_agent_message: AgentAgentMessage, agent_agent_dialogue) -> None:
        pass
        # self.context.logger.warning(
        #     "cannot handle agent agent message of performative={} in dialogue={}.".format(
        #         agent_agent_message.performative, agent_agent_dialogue,
        #     )
        # )
