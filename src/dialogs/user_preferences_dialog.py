from typing import Dict

import httpx
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ListStyle)
from botbuilder.dialogs.choices import Choice
from botbuilder.dialogs.prompts import (
    ChoicePrompt,
    PromptOptions,
)

from bot_data import banks
from bot_data.language import Language
from config import BotConfig
from data_models import UserPreferences
from resources import ResponseMsgs


class UserPreferencesDialog(ComponentDialog):
    """Represents a dialog which is used for gathering user profile information and preferences."""
    # Nested dialog ids ids
    WATERFALL_DIALOG_ID = 'waterfall'
    LANG_CHOICE_PROMPT_ID = 'lang_prompt'
    BANK_CHOICE_PROMPT_ID = 'bank_prompt'

    FB_USER_SETTINGS_URL = 'https://graph.facebook.com/v5.0/me/custom_user_settings'

    def __init__(self, dialog_id: str, user_state: UserState):
        super(UserPreferencesDialog, self).__init__(dialog_id)

        self.user_preferences_accessor = user_state.create_property("user_preferences")

        # Setup dialogs
        self.add_dialog(
            WaterfallDialog(
                UserPreferencesDialog.WATERFALL_DIALOG_ID,
                [
                    self.language_step,
                    self.bank_step,
                    self.summary_step
                ],
            )
        )
        self.add_dialog(ChoicePrompt(UserPreferencesDialog.LANG_CHOICE_PROMPT_ID))
        self.add_dialog(ChoicePrompt(UserPreferencesDialog.BANK_CHOICE_PROMPT_ID))

        self.initial_dialog_id = UserPreferencesDialog.WATERFALL_DIALOG_ID

    async def language_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Runs a prompt to get user preferred language.

        :param step_context:
        :return DialogTurnResult:
        """
        return await step_context.prompt(
            UserPreferencesDialog.LANG_CHOICE_PROMPT_ID,
            PromptOptions(
                prompt=MessageFactory.text(ResponseMsgs.get('choose_language')),
                style=ListStyle.hero_card,
                choices=[Choice(ResponseMsgs.get('lang_hy')),
                         Choice(ResponseMsgs.get('lang_en')),
                         Choice(ResponseMsgs.get('lang_ru'))],
            ),
        )

    async def bank_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Runs a prompt to get user preferred bank.

        :param step_context:
        :return DialogTurnResult:
        """
        # Get the previous dialog result, i.e. user chosen language, and parse it to get a Language() object
        prev_dialog_result = step_context.result.value
        if prev_dialog_result == ResponseMsgs.get('lang_en'):
            chosen_lang = Language.en
        elif prev_dialog_result == ResponseMsgs.get('lang_ru'):
            chosen_lang = Language.ru
        else:
            chosen_lang = Language.hy

        step_context.values["lang"] = chosen_lang

        # Run a prompt to get user preferred bank.
        return await step_context.prompt(
            UserPreferencesDialog.BANK_CHOICE_PROMPT_ID,
            PromptOptions(
                prompt=MessageFactory.text(ResponseMsgs.get('choose_bank', lang=chosen_lang)),
                style=ListStyle.hero_card,
                choices=[Choice(getattr(bank, f'{chosen_lang.value}_name')) for bank in banks.BANKS]
            ),
        )

    async def summary_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Saves the user preferences got from previous dialogs and sends to user a confirmation message.

        :param step_context:
        :return DialogTurnResult:
        """
        # Get results from the previous dialogs
        prev_dialog_result = step_context.result.value
        chosen_lang = step_context.values["lang"]

        # Get the chosen bank id
        chosen_bank_id = banks.get_by_name(prev_dialog_result).id_

        # Get the current profile object from user state.
        user_preferences = await self.user_preferences_accessor.get(
            step_context.context, UserPreferences
        )

        # Save the user profile data in memory so that it will be saved in db later.
        # This will be saved to the storage later.
        user_preferences.lang = chosen_lang
        user_preferences.bank = chosen_bank_id

        # Construct OK message
        msg = MessageFactory.text(ResponseMsgs.get('prefs_saved', chosen_lang, bank=prev_dialog_result))
        # Attach a keyboard-menu to the message for telegram
        if step_context.context.activity.channel_id == 'telegram':
            msg.channel_data = UserPreferencesDialog.__construct_telegram_keyboard(chosen_lang)

        # Send OK message
        await step_context.context.send_activity(msg)

        # Construct a keyboard-menu for facebook
        if step_context.context.activity.channel_id == 'facebook':
            # noinspection PyBroadException
            try:
                await UserPreferencesDialog.__make_fb_keyboard(step_context.context.activity.from_property.id,
                                                               chosen_lang)
            except Exception:
                pass

        return await step_context.end_dialog()

    @staticmethod
    def __construct_telegram_keyboard(lang: Language) -> Dict:
        """Constructs and returns a JSON (dict) obj for telegram keyboard."""
        all_usd = ResponseMsgs.get('all_usd', lang)
        all_rur = ResponseMsgs.get('all_rur', lang)
        banks_msg = ResponseMsgs.get('banks', lang)
        my_bank = ResponseMsgs.get('my_bank', lang)
        preferences = ResponseMsgs.get('preferences', lang)

        return {
            "method": "sendMessage",
            "parameters": {
                "reply_markup": {
                    "keyboard": [
                        [{"text": all_usd}, {"text": all_rur}],
                        [{"text": banks_msg}, {"text": my_bank}],
                        [{"text": preferences}]
                    ],
                    "resize_keyboard": True
                }
            }
        }

    @staticmethod
    async def __make_fb_keyboard(psid: int, lang: Language):
        """Makes an http request to FB API to make a persistent menu appear for the given user."""
        all_usd = ResponseMsgs.get('all_usd', lang)
        all_rur = ResponseMsgs.get('all_rur', lang)
        my_bank = ResponseMsgs.get('my_bank', lang)

        async with httpx.AsyncClient() as client:
            await client.post(UserPreferencesDialog.FB_USER_SETTINGS_URL, params={
                "access_token": BotConfig.FB_TOKEN
            }, json={
                "psid": psid,
                "persistent_menu": [
                    {
                        "locale": "default",
                        "call_to_actions": [
                            {"type": "postback", "title": all_usd, "payload": all_usd},
                            {"type": "postback", "title": all_rur, "payload": all_rur},
                            {"type": "postback", "title": my_bank, "payload": my_bank},
                        ]
                    }
                ]
            })
