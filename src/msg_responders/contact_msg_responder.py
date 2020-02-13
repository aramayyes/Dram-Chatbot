from typing import Union, List, Tuple

from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity

from data_models import UserPreferences
from msg_responders import BaseMsgResponder
from msg_recognizers import RecognizedMessage, MessageIntent
from resources import ResponseMsgs


class ContactMsgResponder(BaseMsgResponder):
    """Represents a message responder which creates responses for contact messages."""

    async def can_respond(self, recognized_message: RecognizedMessage, channel: str, **kwargs) -> bool:
        return recognized_message.intent is MessageIntent.contact

    async def create_response(self, recognized_message: RecognizedMessage, channel: str,
                              original_msg: str,
                              user_preferences: UserPreferences, **kwargs) \
            -> Union[str, Activity, Tuple, List[str], Dialog]:
        msg = ResponseMsgs.get('contact', user_preferences.lang)
        return msg
