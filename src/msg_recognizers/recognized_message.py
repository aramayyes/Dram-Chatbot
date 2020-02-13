from typing import List, Union, Dict

from msg_recognizers.message_intent import MessageIntent


class RecognizedMessage:
    """Represents a recognized message."""

    def __init__(self, intent: MessageIntent, action: str = None, params: Union[List[str], Dict] = None):
        self.intent = intent
        self.action = action
        self.params = params
