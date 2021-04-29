from typing import Any, Type

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue
from aea.protocols.dialogue.base import DialogueLabel as BaseDialogueLabel

from packages.gdp8.protocols.agent_agent.message import AgentAgentMessage
from packages.gdp8.protocols.agent_environment.message import AgentEnvironmentMessage
from packages.gdp8.protocols.default.dialogues import (
    DefaultDialogues as BaseDefaultDialogues,
    DefaultDialogue as BaseDefaultDialogue
)##not correct

from packages.gdp8.protocols.agent_agent.dialogues import (
    AgentAgentDialogues as BaseAgentAgentDialogues,
    AgentAgentDialogue as BaseAgentAgentDialogue
)

from packages.gdp8.protocols.agent_environment.dialogues import (
    AgentEnvironmentDialogues as BaseAgentEnvironmentDialogues,
    AgentEnvironmentDialogue as BaseAgentEnvironmentDialogue
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

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
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


class AgentAgentDialogue(BaseAgentAgentDialogue):
    """The dialogue class maintains state of a dialogue and manages it."""

    __slots__ = ("?????", "?????")

    def __init__(
            self,
            dialogue_label: BaseDialogueLabel,
            self_address: Address,
            role: BaseDialogue.Role,
            message_class: Type[AgentAgentMessage] = AgentAgentMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for

        :return: None
        """
        BaseAgentAgentDialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            self_address=self_address,
            role=role,
            message_class=message_class,
        )
        # self.??? = None  # type: Optional[Dict[str, str]]
        # self.??? = None  # type: Optional[Terms]


class AgentAgentDialogues(Model, BaseAgentAgentDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return BaseAgentAgentDialogue.Role.AGENT

        BaseAgentAgentDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
            dialogue_class=AgentAgentDialogue,
        )


class AgentEnvironmentDialogue(BaseAgentEnvironmentDialogue):
    """The dialogue class maintains state of a dialogue and manages it."""

    __slots__ = ("?????", "?????")

    def __init__(
            self,
            dialogue_label: BaseDialogueLabel,
            self_address: Address,
            role: BaseDialogue.Role,
            message_class: Type[AgentEnvironmentMessage] = AgentEnvironmentMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for

        :return: None
        """
        BaseAgentEnvironmentDialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            self_address=self_address,
            role=role,
            message_class=message_class,
        )
        # self.????? = None  # type: Optional[Dict[str, str]]
        # self.????? = None  # type: Optional[Terms]


class AgentEnvDialogues(Model, BaseAgentEnvironmentDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return BaseAgentEnvironmentDialogue.Role.AGENT

        BaseAgentEnvironmentDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
            dialogue_class=AgentEnvironmentDialogue,
        )
