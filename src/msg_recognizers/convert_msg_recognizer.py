import re
from typing import Dict, List, Optional

from msg_recognizers import BaseMsgRecognizer, MessageIntent, RecognizedMessage


class ConvertMsgRecognizer(BaseMsgRecognizer):
    @property
    def _commands(self) -> Dict[str, List[str]]:
        return {}

    @property
    def _intent(self) -> MessageIntent:
        return MessageIntent.currency_converter

    def recognize(self, message: str) -> Optional[RecognizedMessage]:
        """
        Tries to recognize the given message, by searching a number in it.

        :param message: Message which should be recognized
        :return RecognizedMessage:
        """
        # Convert the message to lowercase letters,
        #   remove the very first '/' sign and replace all '_' signs with spaces (' '),
        #   which are used for commands in telegram
        message = message.lower()
        message = message.strip()
        message = message.replace('_', ' ')
        if message.startswith('/'):
            message = message[1:]

        # Try to find the first number in the message. Return None if there is no one, because this message is not
        #   recognizable.
        result = RecognizedMessage(self._intent)
        n_re = re.search(r"\d+(\.\d+)?", message.replace(',', '.'))
        if n_re is None:
            return None

        number = n_re.group()
        message = message.replace(number, '', 1)

        result.action = 'convert'
        result.params = [number] + message.strip().split(' ')
        return result
