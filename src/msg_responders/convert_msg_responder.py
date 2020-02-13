import asyncio
from typing import Union, Tuple, List, Dict

from botbuilder.core import ConversationState, UserState
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity

from bot_data import banks, Language
from data_models import UserPreferences
from exchange_rates_informers import ExchangeRatesInformer, ExchangeRate, Bank
from msg_responders import BaseMsgResponder
from msg_recognizers import RecognizedMessage, MessageIntent
from resources import ResponseMsgs


class ConvertMsgResponder(BaseMsgResponder):
    """Represents a message responder which creates responses for messages concerning currency conversions."""

    __AMD = ['֏', 'amd', 'dram', 'drams', 'драм', 'драмов', 'драмы', 'драма', 'դրամ']

    def __init__(self, conversation_state: ConversationState, user_state: UserState,
                 informer: ExchangeRatesInformer):
        super(ConvertMsgResponder, self).__init__(conversation_state, user_state)
        self.informer = informer

    async def can_respond(self, recognized_message: RecognizedMessage, channel: str, **kwargs) -> bool:
        return recognized_message.intent is MessageIntent.currency_converter

    async def create_response(self, recognized_message: RecognizedMessage, channel: str, original_msg: str,
                              user_preferences: UserPreferences, **kwargs) \
            -> Union[str, Activity, Tuple, List[str], Dialog]:
        lang = user_preferences.lang
        bank_id = banks.get_by_id(user_preferences.bank).rate_am_id

        b_non_cash, b_cash = await asyncio.gather(
            self.informer.get_bank_rates(bank_id, lang),
            self.informer.get_bank_rates(bank_id, lang, non_cash=False))

        # Try to get the amount from params
        n = ConvertMsgResponder.__get_param(recognized_message.params, 'amount', 0)
        if n is not None:
            try:
                # Validate the input number
                parts = n.split('.')
                int_part = parts[0].lstrip('0')
                # Take only 2 signs after .
                fr_part = parts[1][:2] if len(parts) > 1 else '00'

                if len(int_part) > 9:
                    return ResponseMsgs.get('err_n_big', lang)

                n = float(f"{int_part}.{fr_part}")

                if n == 0:
                    # n == 0
                    if len(parts) == 1 or parts[1].rstrip('0') == '':
                        return ResponseMsgs.get('err_n_0', lang)
                    # n < 0.01
                    return ResponseMsgs.get('err_n_small', lang)
            except ValueError:
                n = None

        if n is None:
            raise Exception(f'[{ConvertMsgResponder.__name__}]: the amount is missing in params for action convert.')

        # Check the params to know the direction of conversion
        to_amd = not any(
            ConvertMsgResponder.__check_param(recognized_message.params, dram) for dram in ConvertMsgResponder.__AMD)

        # Convert currencies
        convert = (lambda x: float(x) * n) if to_amd else (lambda x: n / float(x))
        for data in (b_non_cash, b_cash):
            rates = []
            for rate in data.rates:
                buy = convert(rate.buy) if rate.buy else ''
                sell = convert(rate.sell) if rate.sell else ''
                rates.append(ExchangeRate(rate.cur, buy, sell))
            data.rates = rates

        # Message formatting: bold
        b = '**' if not channel == 'facebook' else ''

        # Construct the result message
        header = f"{b}{b_non_cash.name} ({b_non_cash.update_time}){b}\n\n"
        non_cash = f"<br/>{ResponseMsgs.get('non_cash', lang)}\n\n---\n\n"
        cash = f"<br/>{ResponseMsgs.get('cash', lang)}\n\n---\n\n"

        rate_msgs = []

        for data in (b_non_cash, b_cash):
            rate_msgs.append(ConvertMsgResponder.__create_res_msg(data, n, lang, to_amd))

        return header + non_cash + rate_msgs[0] + cash + rate_msgs[1]

    @staticmethod
    def __get_param(params: Union[Dict, List], name: str, pos: int = None):
        """Gets the param with given name or position from params."""
        if isinstance(params, dict):
            return params.get(name)
        elif pos is not None and len(params) > pos:
            return params[pos]
        else:
            return None

    @staticmethod
    def __check_param(params: Union[Dict, List], value: str) -> bool:
        """Checks whether the value exists in params."""
        if isinstance(params, dict):
            params = params.values()

        return value in params

    @staticmethod
    def __create_res_msg(bank: Bank, n: float, lang: Language, to_amd=True):
        if to_amd:
            return (
                f"{ResponseMsgs.get('n_usd', n=n)} ({ResponseMsgs.get('buy', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=bank.rates[0].buy) if bank.rates[0].buy else ''}\n\n"
                f"{ResponseMsgs.get('n_usd', n=n)} ({ResponseMsgs.get('sell', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=bank.rates[0].sell) if bank.rates[0].sell else ''}\n\n"
                f"{ResponseMsgs.get('n_rur', n=n)} ({ResponseMsgs.get('buy', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=bank.rates[1].buy) if bank.rates[1].buy else ''}\n\n"
                f"{ResponseMsgs.get('n_rur', n=n)} ({ResponseMsgs.get('sell', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=bank.rates[1].sell) if bank.rates[1].sell else ''}\n\n")
        else:
            return (
                f"{ResponseMsgs.get('n_usd', n=bank.rates[0].buy) if bank.rates[0].buy else ''}"
                f" ({ResponseMsgs.get('buy', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=n)}\n\n"
                f"{ResponseMsgs.get('n_usd', n=bank.rates[0].sell) if bank.rates[0].sell else ''}"
                f" ({ResponseMsgs.get('sell', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=n)}\n\n"
                f"{ResponseMsgs.get('n_rur', n=bank.rates[1].buy) if bank.rates[1].buy else ''}"
                f" ({ResponseMsgs.get('buy', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=n)}\n\n"
                f"{ResponseMsgs.get('n_rur', n=bank.rates[1].sell) if bank.rates[1].sell else ''}"
                f" ({ResponseMsgs.get('sell', lang)}) - "
                f"{ResponseMsgs.get('n_amd', n=n)}\n\n")
