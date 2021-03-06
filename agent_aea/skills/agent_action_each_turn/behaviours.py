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

from packages.gdp8.skills.agent_action_each_turn.strategy import \
    DogStrategy, AltruisticGoldfishStrategy, LoneGoldfishStrategy


class AgentLogicBehaviour(TickerBehaviour):
    """Behaviour first looks at the strategy passed in, chooses the correct strategy, then
       looks at if actions required in each tick:
       is there agent asking for info? if so, tell them
       is the round done (on my end)? if so, end behaviour
       have I asked for information (if needed)? if not, ask
       otherwise, have I received enough information to make a decision? if so, do so"""

    def __init__(self, **kwargs: Any) -> None:
        self.strategyName = kwargs['strategy_used']
        super().__init__(**kwargs)

    def setup(self, **kwargs: Any) -> None:
        """
        Implement the setup.

        :return: None
        """

    def act(self) -> None:

        if self.strategyName == "Explorer Dogs":
            strategy = cast(DogStrategy, self.context.dog_strategy)
        elif self.strategyName == "Altruistic Goldfish":
            strategy = cast(AltruisticGoldfishStrategy, self.context.altruistic_goldfish_strategy)
        else:
            assert self.strategyName == "Lone Goldfish"
            strategy = cast(LoneGoldfishStrategy, self.context.lone_goldfish_strategy)

        there_is_agent_asking_for_info = True
        while there_is_agent_asking_for_info:
            there_is_agent_asking_for_info = strategy.deal_with_an_agent_asking_for_info()
        if not strategy.is_round_done:
            if not strategy.asked_for_info_already:
                self.context.logger.info("ask for info/make decision")
                strategy.ask_for_info_and_maybe_make_decision()
            elif strategy.enough_info_to_make_decision():
                self.context.logger.info("made decision")
                strategy.make_decision_send_to_env()

    def teardown(self) -> None:
        """
        Implement the task teardown.

        :return: None
        """
        pass
