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

"""This package contains a scaffold of a behaviour."""
from typing import cast, Any

from aea.skills.behaviours import TickerBehaviour

from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.tac_control.dialogues import (
    OefSearchDialogues,
)

from gdp.agent_aea.skills.Action_Each_Turn.strategy import BasicStrategy
from gdp.env_aea.skills.Action_Each_Turn.environment import Environment, Phase

DEFAULT_REGISTER_AND_SEARCH_INTERVAL = 5.0


class AgentSearchBehaviour(TickerBehaviour):
    """This class scaffolds a behaviour."""

    def setup(self) -> None:
        """
        Implement the setup.
        :return: None
        """

    def act(self) -> None:
        """
        Implement the act.
        :return: None
        """
        environment = cast(Environment, self.context.environment)##do we need to add the environment model in the agent_aea skill package ?
        if environment.phase.value == Phase.PRE_GAME.value:
            self._search_for_environment()

    def teardown(self) -> None:
        """
        Implement the task teardown.
        :return: None
        """

    def _search_for_environment(self) -> None:
        """
        Search for active environment (simulation controller).
        We assume that the environment is registered as a service with the 'env' data model
        and with an attribute version = expected_version_id.
        :return: None
        """
        environment = cast(Environment, self.context.environment)
        query = environment.get_environment_query()##
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.SEARCH_SERVICES,
            query=query,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info(
            "searching for environment, search_id={}".format(oef_search_msg.dialogue_reference)
        )

class AgentRegisterAndSearchBehaviour(TickerBehaviour):
    """This class implements the agent register and search behaviour."""

    def __init__(self, **kwargs: Any):
        """Initialize the search behaviour."""
        search_interval = cast(
            float, kwargs.pop("search_interval", DEFAULT_REGISTER_AND_SEARCH_INTERVAL)
        )
        super().__init__(tick_interval=search_interval, **kwargs)
        self.is_registered = False

    def setup(self) -> None:
        """
        Implement the setup.
        :return: None
        """

    def act(self) -> None:
        """
        Implement the act.
        :return: None
        """
        # the flag "is_game_finished" is set by the 'tac_participation'
        # the flag "is_simulation_finished" is set by the '????'
        # skill to notify the other skill that the simulation is finished.
        if self.context.shared_state.get("is_simulation_finished", False):## shared state 
            self.context.is_active = False## is active
            return

        if not self.is_registered:##
            self._register_agent()
            self._register_service()
            self.is_registered = True
        self._search_services()

    def teardown(self) -> None:
        """
        Implement the task teardown.
        :return: None
        """
        if self.is_registered:
            self._unregister_service()
            self._unregister_agent()
            self.is_registered = False

    def _register_agent(self) -> None:
        """
        Register the agent's location.
        :return: None
        """
        strategy = cast(Strategy, self.context.strategy)## is our strat class equilavent to theirs ?
        description = strategy.get_location_description()## add fct to strat class
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,## where was it saved ?
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("registering agent on SOEF.")

    def _register_service(self) -> None:
        """
        Register to the OEF Service Directory.
        In particular, register
            - as buyer and seller.
        :return: None
        """
        strategy = cast(Strategy, self.context.strategy)
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        self.context.logger.debug(
            "updating service directory as {}.".format("buyer and seller")##registering as ???
        )
        description = strategy.get_register_service_description()## implement fct in strategy
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)

    def _unregister_service(self) -> None:
        """
        Unregister service from OEF Service Directory.
        :return: None
        """
        strategy = cast(Strategy, self.context.strategy)
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        self.context.logger.debug(
            "unregistering from service directory as {}.".format(
                "buyer and seller"
            )
        )
        description = strategy.get_unregister_service_description()## implement fct in strategy
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)

    def _unregister_agent(self) -> None:
        """
        Unregister agent from the SOEF.
        :return: None
        """
        strategy = cast(Strategy, self.context.strategy)
        description = strategy.get_location_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering agent from SOEF.")

    def _search_services(self) -> None:
        """
        Search on OEF Service Directory.
        In particular, search
            - for sellers and their supply, or
            - for buyers and their demand, or
            - for both.
        :return: None
        """
        strategy = cast(Strategy, self.context.strategy)
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        query = strategy.get_location_and_service_query()## implement fct in strat.
        for (is_seller_search, searching_for) in strategy.searching_for_types:######### check what that corresponds to and adapt it to the list of neighbours
            oef_search_msg, oef_search_dialogue = oef_search_dialogues.create(
                counterparty=self.context.search_service_address,
                performative=OefSearchMessage.Performative.SEARCH_SERVICES,
                query=query,
            )
            oef_search_dialogue = cast(OefSearchDialogue, oef_search_dialogue)
            oef_search_dialogue.is_seller_search = is_seller_search
            self.context.outbox.put_message(message=oef_search_msg)
            self.context.logger.info(
                "searching for {}, search_id={}.".format(
                    searching_for, oef_search_msg.dialogue_reference
                )
            )

class AgentLogicBehaviour(TickerBehaviour):
    """Behaviour looks at if actions required in each tick:
       is there agent asking for water info? if so, tell them
       is the round done (on my end)? if so, stop
       is there enough info for making a decision? if so, do so,
       if not, might have to send message to ask for info"""

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        pass

    def act(self) -> None:

        strategy = cast(BasicStrategy, self.context.strategy)

        there_is_agent_asking_for_water_info = True
        while there_is_agent_asking_for_water_info:
            there_is_agent_asking_for_water_info = strategy.deal_with_an_agent_asking_for_water_info

        if not strategy.is_round_done:
            info_is_enough = strategy.enough_info_to_make_decision
            if info_is_enough:
                strategy.make_decision_send_to_env()
            else:
                asking_for_info = True
                while asking_for_info:
                    asking_for_info = strategy.potentially_ask_for_info

    def teardown(self) -> None:
        """
        Implement the task teardown.

        :return: None
        """
        pass
