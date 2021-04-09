from typing import Any

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from gdp.agent_aea.protocols.default.dialogues import (
    DefaultDialogues as BaseDefaultDialogues,
    DefaultDialogue as BaseDefaultDialogue
)

DefaultDialogue = BaseDefaultDialogue


class DefaultDialogues(Model, BaseDefaultDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)

        # pylint: disable=unused-argument
        def role_from_first_message(message: Message, receiver_address: Address) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return DefaultDialogue.Role.AGENT

        BaseDefaultDialogues.__init__(
            self,
            self_address=self.context.agent_address,
            role_from_first_message=role_from_first_message,
        )

    class AgentAgentDialogues(Model, BaseDefaultDialogues):
        raise NotImplementedError

    class AgentEnvDialogues(Model, BaseDefaultDialogues):
        raise NotImplementedError