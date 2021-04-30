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

from aea.common import Address
from aea.skills.behaviours import TickerBehaviour
from aea.helpers.search.models import Constraint, ConstraintType, Query

from packages.gdp8.skills.agent_action_each_turn.strategy import BasicStrategy

DEFAULT_SEARCH_QUERY = {
    "search_key": "env",## is that the key of the environment ?
    "search_value": "v1", 
    "constraint_type": "==",
}
registeredToEnv = False

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

    def act(self) -> None:

        if not registeredToEnv :
            self._register_to_env(self.context.environment_addr)##where is the env address stored?
       
        else:
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

    def _register_to_env(self, environment_addr: Address) -> None:  
        """
        Register to active environment.
        :param environment_addr: the address of the environment.
        :return: None
        """
        agent_environment_dialogues = cast(AgentEnvironmentDialogues, self.context.agent_environment_dialogues)
        agent_env_msg, agent_environment_dialogue = agent_environment_dialogues.create(
            counterparty=environment_addr,
            performative=AgentEnvironmentMessage.Performative.REGISTER,
            agent_name=self.context.agent_name,## do we have a variable for the agent name? what is its use?
        )
        agent_environment_dialogue = cast(AgentEnvironmentDialogue, agent_environment_dialogue)
        self.context.outbox.put_message(message=agent_env_msg)
        registeredToEnv = True##