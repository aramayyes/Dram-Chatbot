from typing import Dict, List

from bot_data import banks
from msg_recognizers import MessageIntent, BaseMsgRecognizer

_COMMANDS = {
    'all': ['all',
            'al',
            'все',
            'всё',
            'բոլոր',
            'բոլորը', ],
    'banks': [
        'banks',
        'банки',
        'բանկեր',
    ],
    'mybank': [
        'my',
        'mine',
        'mybanks',
        'mybank',
        'my banks',
        'my bank',
        'мой',
        'мои',
        'моибанки',
        'мойбанки',
        'мойбанк',
        'моибанк',
        'мои банки',
        'мой банки',
        'мой банк',
        'мои банк',
        'իմ',
        'իմ բանկերը',
        'իմ բանկեր',
        'իմ բանկը',
        'իմ բանկ',
        'իմբանկերը',
        'իմբանկեր',
        'իմբանկը',
        'իմբանկ',
    ]
}

# Add all available banks as commands
for bank in banks.BANKS:
    _COMMANDS[bank.id_.value] = [bank.en_name.lower(), bank.hy_name.lower(), bank.ru_name.lower()]


class ExchangeRateMsgRecognizer(BaseMsgRecognizer):
    """Recognizes messages which are for are intended for founding out exchange rates."""

    @property
    def _commands(self) -> Dict[str, List[str]]:
        return _COMMANDS

    @property
    def _intent(self) -> MessageIntent:
        return MessageIntent.exchange_rate
