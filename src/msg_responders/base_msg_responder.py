from abc import ABC, abstractmethod
from typing import Union, List, Tuple

from botbuilder.core import ConversationState, UserState
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity

from data_models import UserPreferences
from msg_recognizers import RecognizedMessage


class BaseMsgResponder(ABC):
    """Defines methods which need to be implemented in a message responder class."""

    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        self.conversation_state = conversation_state
        self.user_state = user_state

    @abstractmethod
    async def can_respond(self, recognized_message: RecognizedMessage, channel: str, **kwargs) -> bool:
        """Determines whether this message responder can respond to the messages with given intent and action.

        :param RecognizedMessage recognized_message: recognized message, which contains the intent and action attributes
        :param str channel: channel from which the message came
        """
        pass

    @abstractmethod
    async def create_response(self, recognized_message: RecognizedMessage, channel: str,
                              original_msg: str,
                              user_preferences: UserPreferences, **kwargs) \
            -> Union[str, Activity, Tuple, List[str], Dialog]:
        """Creates a respond for the given message.

        :param RecognizedMessage recognized_message: recognized message, which contains the intent and action attributes
        :param Channel channel: channel from which the message came
        :param str original_msg: original msg
        :param UserPreferences user_preferences: contains user preferences
        :return: str or Activity to send it to user, List[str] to send each of them to user in a single message
                    or Dialog to run it
        """
        pass
