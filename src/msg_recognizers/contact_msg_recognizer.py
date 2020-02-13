from typing import Dict, List

from msg_recognizers import MessageIntent, BaseMsgRecognizer

_COMMANDS = {
    'get': ['contact',
            'contacts',
            'about',
            'связь',
            'контакт',
            'контакты',
            'կապ',
            'կոնտակտ',
            'կոնտակտներ',
            'մասին',
            ],
}


class ContactMsgRecognizer(BaseMsgRecognizer):
    """Recognizes contact messages."""

    @property
    def _commands(self) -> Dict[str, List[str]]:
        return _COMMANDS

    @property
    def _intent(self) -> MessageIntent:
        return MessageIntent.contact
