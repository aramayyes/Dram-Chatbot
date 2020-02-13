from typing import Union, List, Tuple

from botbuilder.core import UserState, ConversationState
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity

from data_models import UserPreferences
from dialogs import UserPreferencesDialog
from msg_responders import BaseMsgResponder
from msg_recognizers import RecognizedMessage, MessageIntent


class ChangePrefMsgResponder(BaseMsgResponder):
    """Represents a message responder which creates responses for messages concerning user preferences."""

    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        super(ChangePrefMsgResponder, self).__init__(conversation_state, user_state)
        self.user_pref_dialog = UserPreferencesDialog('user_prefs', user_state)
        pass

    async def can_respond(self, recognized_message: RecognizedMessage, channel: str, **kwargs) -> bool:
        return recognized_message.intent is MessageIntent.preferences

    async def create_response(self, recognized_message: RecognizedMessage, channel: str,
                              original_msg: str,
                              user_preferences: UserPreferences, **kwargs) \
            -> Union[str, Activity, Tuple, List[str], Dialog]:
        return self.user_pref_dialog
