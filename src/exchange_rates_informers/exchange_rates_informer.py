from abc import ABC, abstractmethod
from typing import List, Tuple

from bot_data import Language, Currency
from exchange_rates_informers import Bank


class ExchangeRatesInformer(ABC):
    """Defines methods which need to be implemented in exchange rates informer classes to get ADM exchange rates."""

    @abstractmethod
    async def get_banks(self, lang: Language) -> List[str]:
        """Gets all banks.

        :param Language lang: The language in which banks names should be
        """
        pass

    @abstractmethod
    async def get_all(self, lang: Language, curr: Currency, non_cash: bool = True) -> Tuple[Tuple, List[Bank]]:
        """Gets AMD exchange rates against the given currency set by all banks.

        :param Language lang: The language in which banks names should be
        :param Currency curr: currency, against which exchange rates should be got
        :param bool non_cash: get exchange rates for non_cash or cash types
        """
        pass

    @abstractmethod
    async def get_bank_rates(self, bank_id: str, lang: Language, non_cash: bool = True) -> Bank:
        """Gets AMD exchange rates set by the given bank."""
        pass
