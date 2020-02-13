from bot_data.language import Language


class ResponseMsgs:
    """Holds all messages that are sent to user by bot."""
    _GLOBAL_MESSAGES = {
        'choose_language':
            ("Ընտրեք լեզուն։\n\n"
             "Choose your preferred language.\n\n"
             "Выберите язык.\n\n"),
        'lang_hy': u'\U0001F1E6\U0001F1F2 Հայերեն',  # AM flag
        'lang_en': u'\U0001F1FA\U0001F1F8 English',  # US flag
        'lang_ru': u'\U0001F1F7\U0001F1FA Русский',  # RU flag
        'n_amd': '\U0001F1E6\U0001F1F2 {n:,.2f}֏',  # AM flag
        'n_usd': '\U0001F1FA\U0001F1F8 {n:,.2f}$',  # US flag
        'n_rur': '\U0001F1F7\U0001F1FA {n:,.2f}₽',  # RU flag
        'choose_bank':
            ("Ընտրեք Ձեր բանկը։\n"
             "Choose your preferred bank.\n"
             "Выберите Ваш предпочитаемый банк."),
        'error': '\U0001F912\U0001F912\U0001F912\U0001F912\U0001F912'
    }

    _HY_MESSAGES = {
        'choose_bank': "Ընտրեք Ձեր բանկը։",
        'prefs_saved': ("Շատ լավ։ Կարգավորումները պահպանված են։ \U0001F44D\n\n"  # Thumbs up 👍
                        "\U0001F1E6\U0001F1F2 Լեզու՝ հայերեն\n\n"  # AM flag
                        "\U0001F3E6 Բանկ՝ {bank}"  # Bank 🏦
                        ),
        'welcome': u"Ողջույն։ \U0001F44B",  # Waving hand 👋
        'help': ('Ես կարող եմ օգնել Ձեզ իմանալ հայկական դրամի փոխարժեքները։\n\n'
                 '<br/>'
                 'Համապատասխան ինֆորմացիա ստանալու համար կարող եք օգտվել մենյուից և հետևյալ հրամաններից՝\n\n'
                 '- Բոլորը $(դոլար) - տեսնել բոլոր բանկերի կողմից սահմանված դրամի փոխարժեքները ԱՄՆ դոլարի նկատմամբ\n\n'
                 '- Բոլորը ₽(ռուբլի) - տեսնել բոլոր բանկերի կողմից սահմանված դրամի փոխարժեքները ՌԴ ռուբլու նկատմամբ\n\n'
                 '- Բանկեր - տեսնել բոլոր բանկերը\n\n'
                 '- Իմ բանկը - տեսնել իմ բանկի կողմից սահմանված դրամի փոխարժեքները\n\n'
                 '- Կարգավորումներ - փոխել լեզուն և բանկը\n\n'
                 '- Օգնություն - տեսնել հասանելի հրամանները\n\n'
                 '- Կապ - տեսնել կոնտակտային տվյալները\n\n'
                 '<br/>'
                 'Հաշվիչից օգտվելու համար պարզապես ուղարկեք անհրաժեշտ գումարը, այն դրամի փոխարկելու համար (օր․ 200), '
                 'իսկ դրամն ԱՄՆ դոլարի և ռուսական ռուբլու փոխարկելու համար, '
                 'գումարի հետ ուղարկեք «դրամ» բառը (օր․ 48000 դրամ)։'
                 ),
        'contact': 'Բոլոր տվյալները վերցվում են rate.am-ից։ Առաջարկների կամ թերություն գտնելու դեպքում '
                   'կարող եք գրել հետևյալ հասցեին՝ aramayis.amiraghyan@yandex.com',
        'choose_bank_for_rates': "Ընտրեք բանկը փոխարժեքները իմանալու համար",
        'non_cash': 'Անկանխիկ',
        'cash': 'Կանխիկ',
        'buy': 'Առք',
        'sell': 'Վաճ.',
        'bank_name': 'Բանկ',
        'err_n_big': "\U0001F911\U0001F911\U0001F911 Լու՞րջ:\n\n"  # Money-mouth face 🤑
        # Pensive face 😔
                     "Գումարը պետք է պարունակի ամենաշատը 9 նիշ, որ ես կարողանամ փոխակերպել այն։ \U0001F614",
        # Face with raised eyebrow 🤨
        'err_n_small': "Գումարը շատ փոքր է, ես էլ այդքան լավ չեմ միկրոսկոպիկ հաշվարկներից։ \U0001F928",
        'err_n_0': "Գուցե զարմանաք, բայց 0-ն բոլոր արժույթներով էլ 0 է։ \U0001F643",  # Upside-down face 🙃

        # Menu
        'all_usd': '\U0001F1FA\U0001F1F8 Բոլորը $',  # US flag
        'all_rur': '\U0001F1F7\U0001F1FA Բոլորը ₽',  # RU flag
        'banks': '\U0001F3DB Բանկեր',  # Classical building 🏛
        'my_bank': '\U0001F3E6 Իմ բանկը',  # Bank 🏦
        'preferences': '\U00002699 Կարգավորումներ'  # Gear ⚙
    }

    _EN_MESSAGES = {
        'choose_bank': "Choose your preferred bank.",
        'prefs_saved': ("Great, settings have been saved! \U0001F44D\n\n"  # Thumbs up 👍
                        "\U0001F1FA\U0001F1F8 Language: english\n\n"  # US flag
                        "\U0001F3E6 Bank: {bank}"  # Bank 🏦
                        ),
        'welcome': u"Hello and welcome!! \U0001F44B",  # Waving hand 👋
        'help': ('I can help you find out armenian dram exchange rates.\n\n'
                 '<br/>'
                 'You can use the menu and following commands to get relevant information:\n\n'
                 '- All $(dollar)- get AMD exchange rates against USD set by all banks\n\n'
                 '- All ₽(ruble)- get AMD exchange rates against RUR set by all banks \n\n'
                 '- Banks - get all banks\n\n'
                 '- My bank - get AMD exchange rates set by my bank\n\n'
                 '- Preferences - change the language and bank\n\n'
                 '- Help - get available commands\n\n'
                 '- Contact - get contact details\n\n'
                 '<br/>'
                 'To use currency converter just send the necessary amount to convert it to AMD (e.g. 200), '
                 'and to convert AMD to USD or RUR add the word \'dram\' to the amount (e.g. 48000 dram).'
                 ),
        'contact': 'All data is taken from rate.am. In case if you have any suggestions or find a bug, '
                   'please send an email to this address: aramayis.amiraghyan@yandex.com',
        'choose_bank_for_rates': "Choose a bank to get the exchange rates",
        'non_cash': 'Non-cash',
        'cash': 'Cash',
        'buy': 'Buy',
        'sell': 'Sell',
        'bank_name': 'Bank',
        'err_n_big': "\U0001F911\U0001F911\U0001F911 Are you serious?\n\n"  # Money-mouth face 🤑
                     "The amount should have at most 9 digits, so that I can convert. \U0001F614",  # Pensive face 😔
        # Face with raised eyebrow 🤨
        'err_n_small': "The amount is very small and I am not good at microscopic calculations. \U0001F928",
        'err_n_0': "Will you be surprised if I tell you that 0 is 0 everywhere? \U0001F643",  # Upside-down face 🙃

        # Menu
        'all_usd': '\U0001F1FA\U0001F1F8 All $',  # US flag
        'all_rur': '\U0001F1F7\U0001F1FA All ₽',  # RU flag
        'banks': '\U0001F3DB Banks',  # Classical building 🏛
        'my_bank': '\U0001F3E6 My bank',  # Bank 🏦
        'preferences': '\U00002699 Preferences'  # Gear ⚙
    }

    _RU_MESSAGES = {
        'choose_bank': "Выберите Ваш предпочитаемый банк.",
        'prefs_saved': ("Отлично, настройки сохранены! \U0001F44D\n\n"  # Thumbs up 👍
                        "\U0001F1F7\U0001F1FA Язык: русский\n\n"
                        "\U0001F3E6 Банк: {bank}"  # Bank 🏦
                        ),
        'welcome': u"Привет! \U0001F44B",  # Waving hand 👋
        'help': ('Я могу помочь Вам узнать курсы армянского драма.\n\n'
                 '<br/>'
                 'Для получения соответствующей информации, можете использовать меню и следующие команды։\n\n'
                 '- Все $(доллар) - узнать курс драма к доллару США\n\n'
                 '- Все ₽(рубль) - узнать курс драма к рублю РФ\n\n'
                 '- Банки - увидеть все банки\n\n'
                 '- Мой банк - узнать курс драма установленный моим банком\n\n'
                 '- Настройки - изменить язык и банк\n\n'
                 '- Помощь - увидеть доступные команды\n\n'
                 '- Контакты - увидеть контактную информацию\n\n'
                 '<br/>'
                 'Чтобы воспользоваться конвертером валют, просто отправьте необходимую сумму (например: 200) '
                 'и она будет конвертирована в драмы. Для конвертации драма в доллары США и рубли РФ, отправьте слово '
                 '«драм» вместе с суммой (например: 48000 драм).'
                 ),
        'contact': 'Все данные берутся из rate.am. Если у вас есть предложения или вы нашли ошибку, можете '
                   'отправить электронное письмо по адресу aramayis.amiraghyan@yandex.com',
        'choose_bank_for_rates': "Выберите банк, чтобы узнать курсы валют",
        'non_cash': 'Безналичный',
        'cash': 'Наличный',
        'buy': 'Куп.',
        'sell': 'Прод.',
        'bank_name': 'Банк',
        'err_n_big': "\U0001F911\U0001F911\U0001F911 Вы серьезно?\n\n"  # Money-mouth face 🤑
                     "Я умею конвертировать максимум девятизначные суммы. \U0001F614",  # Pensive face 😔
        # Face with raised eyebrow 🤨
        'err_n_small': "Сумма очень маленькая, а я не очень дружу с микроскопическими вычислениями. \U0001F928",
        'err_n_0': "0 он и в Африке 0. \U0001F643",  # Upside-down face 🙃

        # Menu
        'all_usd': '\U0001F1FA\U0001F1F8 Все $',  # US flag
        'all_rur': '\U0001F1F7\U0001F1FA Все ₽',  # RU flag
        'banks': '\U0001F3DB Банки',  # Classical building 🏛
        'my_bank': '\U0001F3E6 Мой банк',  # Bank 🏦
        'preferences': '\U00002699 Настройки'  # Gear ⚙
    }

    @staticmethod
    def get(id_, lang: Language = None, **kwargs):
        """Returns a message in the specified language with the given id.

        :param id_: Id of the message
        :param lang: Language of the message. Should be none for global messages.
        """
        msg = None
        if lang is None:
            msg = ResponseMsgs._GLOBAL_MESSAGES[id_]
        elif lang == Language.hy:
            msg = ResponseMsgs._HY_MESSAGES[id_]
        elif lang == Language.en:
            msg = ResponseMsgs._EN_MESSAGES[id_]
        elif lang == Language.ru:
            msg = ResponseMsgs._RU_MESSAGES[id_]

        if kwargs:
            return msg.format(**kwargs)
        else:
            return msg
