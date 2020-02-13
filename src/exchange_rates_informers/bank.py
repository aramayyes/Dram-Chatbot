from typing import List

from .exchange_rate import ExchangeRate


class Bank:
    """Represents a bank, which has an id, name and rates."""

    def __init__(self, id_: str, name: str, update_time: str = None, ex_rates: List[ExchangeRate] = None):
        self.id_ = id_
        self.name = name
        self.update_time = update_time

        self.rates = ex_rates if ex_rates else []
