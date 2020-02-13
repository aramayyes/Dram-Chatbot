from enum import Enum


class MessageIntent(Enum):
    """Contains all available intents for the input messages."""
    help = 1
    contact = 10
    preferences = 20
    exchange_rate = 30
    currency_converter = 40
    unknown_intent = 100
