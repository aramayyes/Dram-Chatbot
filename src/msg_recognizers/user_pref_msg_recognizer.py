from typing import Dict, List

from msg_recognizers import MessageIntent, BaseMsgRecognizer

_COMMANDS = {
    'edit': [
        'preference',
        'pref',
        'setting',
        'option',
        'preferences',
        'prefs',
        'settings',
        'options',
        'language',
        'lang'

        'настройка',
        'настройки',
        'опции',
        'язык',

        'կարգավորում',
        'կարգավորումներ',
        'լեզու',
        'լեզուն',
    ],

}


class UserPrefMsgRecognizer(BaseMsgRecognizer):
    """Recognizes messages concerning user preferences."""

    @property
    def _commands(self) -> Dict[str, List[str]]:
        return _COMMANDS

    @property
    def _intent(self) -> MessageIntent:
        return MessageIntent.preferences
