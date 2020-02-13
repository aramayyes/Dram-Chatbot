from bot_data.banks import BankId
from bot_data.language import Language


class UserPreferences:
    """Contains the user preferences data got from storage."""

    def __init__(self, lang: Language = None, bank: BankId = None):
        self.lang = lang
        self.bank = bank
