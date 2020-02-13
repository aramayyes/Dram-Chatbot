from typing import List, Tuple

import httpx
from lxml import html

from exchange_rates_informers import ExchangeRate
from exchange_rates_informers.exchange_rates_informer import ExchangeRatesInformer
from exchange_rates_informers.bank import Bank
from bot_data import Language, Currency


class RateAmParserExchangeRatesInformer(ExchangeRatesInformer):
    """Informs AMD exchange rates by parsing the rate.am web page."""

    __URL = 'http://rate.am/{}/armenian-dram-exchange-rates/banks/{}'

    async def get_banks(self, lang: Language) -> List[str]:
        page_source = await self.__get_page_source(lang)

        parsed_source = html.fromstring(page_source)
        banks_tds = parsed_source.xpath('//td[@class="bank"]/a')
        banks_names = [bank_td.text for bank_td in banks_tds]

        return banks_names

    async def get_all(self, lang: Language, curr: Currency, non_cash: bool = True) -> Tuple[Tuple, List[Bank]]:
        # Get page source
        page_source = await self.__get_page_source(lang, non_cash)
        parsed_source = html.fromstring(page_source)
        banks_trs = parsed_source.xpath('//*[@id="rb"]/tr')

        # Get an offset from usd cells based on curr
        offset = 0
        if curr is Currency.rur:
            offset = 4

        best = ('', '')

        # noinspection PyBroadException
        try:
            max_tr = banks_trs[-3]
            max_tds = max_tr.xpath('./td')
            maximum = max_tds[1 + offset].text
            if maximum is None:
                maximum = ''
            elif '.' not in maximum:
                maximum = f"{maximum}.00"

            min_tr = banks_trs[-4]
            min_tds = min_tr.xpath('./td')
            minimum = min_tds[2 + offset].text
            if minimum is None:
                minimum = ''
            elif '.' not in minimum:
                minimum = f"{minimum}.00"

            best = maximum, minimum
        except Exception:
            pass

        # skip non-bank trs
        banks_trs = banks_trs[2:-5]

        rate_am_banks = []
        for bank_tr in banks_trs:
            try:
                bank_tds = bank_tr.xpath('./td')

                id_ = bank_tr.attrib['id']
                name = bank_tds[1].xpath('a[1]')[0].text

                buy = bank_tds[5 + offset].text if bank_tds[5 + offset].text is not None else \
                    bank_tds[5 + offset].xpath('./*[1]')[0].text
                if '.' not in buy:
                    buy = f"{buy}.00"

                sell = bank_tds[6 + offset].text if bank_tds[6 + offset].text is not None else \
                    bank_tds[6 + offset].xpath('./*[1]')[0].text
                if '.' not in sell:
                    sell = f"{sell}.00"

                ex_rate = ExchangeRate(curr.value, buy, sell)

                rate_am_banks.append(Bank(id_, name, ex_rates=[ex_rate]))
            except IndexError:
                pass

        return best, rate_am_banks

    async def get_bank_rates(self, bank_id: str, lang: Language, non_cash: bool = True) -> Bank:
        # Get page source
        page_source = await self.__get_page_source(lang, non_cash)
        parsed_source = html.fromstring(page_source)
        bank_tr = parsed_source.xpath(f'//tr[@id="{bank_id}"]')[0]

        bank_tds = bank_tr.xpath('./td')
        name = bank_tds[1].xpath('a[1]')[0].text
        update_time = bank_tds[4].text

        try:
            usd_buy = bank_tds[5].text if bank_tds[5].text is not None else \
                bank_tds[5].xpath('./*[1]')[0].text
        except IndexError:
            usd_buy = ''
        try:
            usd_sell = bank_tds[6].text if bank_tds[6].text is not None else \
                bank_tds[6].xpath('./*[1]')[0].text
        except IndexError:
            usd_sell = ''
        bank = Bank(bank_id, name, update_time, [ExchangeRate('usd', usd_buy, usd_sell)])

        try:
            rur_buy = bank_tds[9].text if bank_tds[9].text is not None else \
                bank_tds[9].xpath('./*[1]')[0].text
        except IndexError:
            rur_buy = ''
        try:
            rur_sell = bank_tds[10].text if bank_tds[10].text is not None else \
                bank_tds[10].xpath('./*[1]')[0].text
        except IndexError:
            rur_sell = ''

        bank.rates.append(ExchangeRate('rur', rur_buy, rur_sell))

        return bank

    @staticmethod
    async def __get_page_source(lang: Language, non_cash: bool = True):
        """Gets rate.am page source."""
        url_lang = lang.value if lang != Language.hy else 'am'

        url = RateAmParserExchangeRatesInformer.__URL.format(url_lang, 'non-cash' if non_cash else 'cash')
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'}

        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
            return r.text
