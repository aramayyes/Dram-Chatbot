import asyncio
from typing import Union, List, Tuple

from botbuilder.core import ConversationState, UserState, CardFactory, MessageFactory
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity, HeroCard, CardAction, ActionTypes

from bot_data import banks, Currency, Language
from data_models import UserPreferences
from exchange_rates_informers import ExchangeRatesInformer
from msg_responders import BaseMsgResponder
from msg_recognizers import RecognizedMessage, MessageIntent
from resources import ResponseMsgs


class ExchangeRateMsgResponder(BaseMsgResponder):
    """Represents a message responder which creates responses for messages concerning exchange rates."""

    __RUR = ['₽', 'ru', 'rur', 'rub*', 'rus*', 'ру', 'руб*', 'рус*', 'рос*', 'ռուս*', 'ռուբ*']

    def __init__(self, conversation_state: ConversationState, user_state: UserState,
                 informer: ExchangeRatesInformer):
        super(ExchangeRateMsgResponder, self).__init__(conversation_state, user_state)
        self.informer = informer

        self.actions = {
            'all': self._get_all,
            'banks': self._get_banks,
            'mybank': self._get_user_bank_rates
        }

        for bank in banks.BANKS:
            self.actions[bank.id_.value] = self._get_bank_rates

    async def can_respond(self, recognized_message: RecognizedMessage, channel: str, **kwargs) -> bool:
        return recognized_message.intent is MessageIntent.exchange_rate and recognized_message.action in self.actions

    async def create_response(self, recognized_message: RecognizedMessage, channel: str,
                              original_msg: str,
                              user_preferences: UserPreferences, **kwargs) \
            -> Union[str, Activity, Tuple, List[str], Dialog]:
        action = self.actions.get(recognized_message.action)

        # Raise an exception if the action is not supported.
        # This situation is typical for cases when this method is called without first calling :py:meth:`can_respond`.
        if action is None:
            raise Exception(f"{ExchangeRateMsgResponder.__name__}: unsupported action {recognized_message.action}.")

        # Execute the action and return the result
        return await action(recognized_message=recognized_message, original_msg=original_msg,
                            user_preferences=user_preferences, channel=channel)

    async def _get_all(self, recognized_message: RecognizedMessage, user_preferences: UserPreferences, channel: str,
                       **kwargs) -> (str, str):
        """Gets buy and sell exchange rates for given currency at all banks.

        :param RecognizedMessage recognized_message: recognized message which contains params
        :param UserPreferences user_preferences: user preferences
        :param str channel: channel id from which the message came
        :return tuple: the first element is a table-like message for non-cash rates and the second for cash rates
        """
        # Get user bank's rate_am_id to highlight bank's name in the response message.
        user_bank_id = banks.get_by_id(user_preferences.bank).rate_am_id
        lang = user_preferences.lang

        # Message formatting: bold and italic
        b = '**'
        i = '*'
        if channel == 'facebook':
            b = "'"
            i = "'"

        cur = Currency.usd

        # Get the currency from message params
        params = recognized_message.params
        if isinstance(params, dict):
            params = params.values()

        def is_in_params(clue):
            return any(
                param.startswith(clue[:-1]) if clue.endswith('*') else clue == param for param in params)

        if any(is_in_params(rur) for rur in ExchangeRateMsgResponder.__RUR):
            cur = Currency.rur

        # Get the best rates values and all banks rates for both non-cash and cash types
        ((best_non_cash, banks_non_cash), (best_cash, banks_cash)) = await asyncio.gather(
            self.informer.get_all(lang, cur), self.informer.get_all(lang, cur, non_cash=False))

        # Sort banks by name
        banks_non_cash.sort(key=lambda x: x.name)
        banks_cash.sort(key=lambda x: x.name)

        # Bring the user bank to the front of the list
        for b_nc in banks_non_cash:
            if b_nc.id_ == user_bank_id:
                break
        else:
            b_nc = None
        if b_nc:
            banks_non_cash.remove(b_nc)
            banks_non_cash.insert(0, b_nc)

        for b_c in banks_cash:
            if b_c.id_ == user_bank_id:
                break
        else:
            b_c = None
        if b_c:
            banks_cash.remove(b_c)
            banks_cash.insert(0, b_c)

        # Create a table-like text for both cash and non-cash types. Bank name is in the end of row, because otherwise
        #   the message doesn't look like a table, since bank names have different lengths.
        # Highlight best rates and user bank.
        non_cash_table = ExchangeRateMsgResponder.__create_banks_table(banks_non_cash, best_non_cash[0],
                                                                       best_non_cash[1], b, i, channel, user_bank_id)

        cash_table = ExchangeRateMsgResponder.__create_banks_table(banks_cash, best_cash[0],
                                                                   best_cash[1], b, i, channel, user_bank_id)

        # Construct the result message
        currency_msg = ResponseMsgs.get('n_rur' if cur is Currency.rur else 'n_usd', n=1)
        non_cash_msg = ResponseMsgs.get('non_cash', lang)
        cash_msg = ResponseMsgs.get('cash', lang)
        table_header_msg = (f"{ResponseMsgs.get('buy', lang)} | "
                            f"{ResponseMsgs.get('sell', lang)} | "
                            f"{ResponseMsgs.get('bank_name', lang)}")

        # Don't highlight headers for fb
        if b == "'":
            b = ''
        res_msg_non_cash = (
            f"{b}{currency_msg}, {non_cash_msg}{b}\n\n\n\n"
            f"{table_header_msg}\n\n"
            "-----\n\n"
            f"{non_cash_table}"
        )

        res_msg_cash = (
            f"{b}{currency_msg}, {cash_msg}{b}\n\n\n\n"
            f"{table_header_msg}\n\n"
            "-----\n\n"
            f"{cash_table}\n\n"
        )

        return res_msg_non_cash, res_msg_cash

    async def _get_user_bank_rates(self, user_preferences: UserPreferences, channel: str, **kwargs) -> str:
        """Gets buy and sell exchange rates for all supported currencies at user bank.

        :param UserPreferences user_preferences: user preferences
        :param str channel: channel id from which the message came
        :return str: message which contains both non-cash and cash rates for all supported currencies
        """
        lang = user_preferences.lang
        bank_id = banks.get_by_id(user_preferences.bank).rate_am_id

        return await self.__get_rates_by_bank_id(bank_id, lang, channel)

    async def _get_bank_rates(self, recognized_message: RecognizedMessage, user_preferences: UserPreferences,
                              channel: str, **kwargs):
        """Gets buy and sell exchange rates for all supported currencies at the given bank.

        :param RecognizedMessage recognized_message: recognized message which contains bank name as the action attr
        :param UserPreferences user_preferences: user preferences
        :param str channel: channel id from which the message came
        :return str: message which contains both non-cash and cash rates for all supported currencies
        """
        lang = user_preferences.lang
        bank_real_id = recognized_message.action
        bank_id = banks.get_by_id(bank_real_id).rate_am_id

        return await self.__get_rates_by_bank_id(bank_id, lang, channel)

    async def __get_rates_by_bank_id(self, bank_id: str, lang: Language, channel: str):
        """Returns exchange rates at the given bank."""
        b_non_cash, b_cash = await asyncio.gather(
            self.informer.get_bank_rates(bank_id, lang),
            self.informer.get_bank_rates(bank_id, lang, non_cash=False))

        # Message formatting: bold
        b = '**' if not channel == 'facebook' else ''

        header = f"{b}{b_non_cash.name} ({b_non_cash.update_time}){b}\n\n"
        non_cash = f"<br/>{ResponseMsgs.get('non_cash', lang)}\n\n---\n\n"
        cash = f"<br/>{ResponseMsgs.get('cash', lang)}\n\n---\n\n"

        rate_msgs = []
        for data in (b_non_cash, b_cash):
            rate_msgs.append(
                f"{ResponseMsgs.get('n_usd', n=1)} ({ResponseMsgs.get('buy', lang)}) - {data.rates[0].buy}\n\n"
                f"{ResponseMsgs.get('n_usd', n=1)} ({ResponseMsgs.get('sell', lang)}) - {data.rates[0].sell}\n\n"
                f"{ResponseMsgs.get('n_rur', n=1)} ({ResponseMsgs.get('buy', lang)}) - {data.rates[1].buy}\n\n"
                f"{ResponseMsgs.get('n_rur', n=1)} ({ResponseMsgs.get('sell', lang)}) - {data.rates[1].sell}\n\n")

        return header + non_cash + rate_msgs[0] + cash + rate_msgs[1]

    @staticmethod
    async def _get_banks(user_preferences: UserPreferences, **kwargs):
        """Returns all banks names."""
        lang = user_preferences.lang

        choose_bank_text = ResponseMsgs.get('choose_bank_for_rates', lang)
        card = HeroCard(
            text=choose_bank_text,
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title=getattr(bank, f'{lang.value}_name'),
                    value=getattr(bank, f'{lang.value}_name')
                ) for bank in banks.BANKS
            ],
        )

        card_attachment = CardFactory.hero_card(card)

        reply = MessageFactory.list([card_attachment])
        return reply

    @staticmethod
    def __create_banks_table(banks_, best_buy, best_sell, b, i, channel, user_bank):
        """Creates a table-like message for given banks and rates."""
        return '\n\n'.join(
            f"{f'{b}{bank.rates[0].buy}{b}' if bank.rates[0].buy == best_buy else bank.rates[0].buy} | " +
            f"{f'{b}{bank.rates[0].sell}{b}' if bank.rates[0].sell == best_sell else bank.rates[0].sell} | " +
            (f'{i}{ExchangeRateMsgResponder.__truncate_bank_name(bank.name, channel)}{i}' if bank.id_ == user_bank
             else ExchangeRateMsgResponder.__truncate_bank_name(bank.name, channel))
            for bank in banks_)

    @staticmethod
    def __truncate_bank_name(name, channel):
        """Truncates the given name, so it can fit in banks table message."""
        if channel == 'telegram':
            if len(name) > 13:
                name = name[:12]
        elif channel == 'facebook':
            if len(name) > 8:
                name = name[:6] + '...'

        return name
