from typing import Dict, List

from msg_recognizers import MessageIntent, BaseMsgRecognizer

_COMMANDS = {
    'help': ['help',
             'помощь',
             'помощ',
             'помошь',
             'помош',
             'օգնություն',
             'օգնել',
             ],
}


class HelpMsgRecognizer(BaseMsgRecognizer):
    """Recognizes help messages."""

    @property
    def _commands(self) -> Dict[str, List[str]]:
        return _COMMANDS

    @property
    def _intent(self) -> MessageIntent:
        return MessageIntent.help
