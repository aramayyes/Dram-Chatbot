from typing import List

from botbuilder.core import UserState, ConversationState, MessageFactory
from botbuilder.dialogs import (
    ComponentDialog, Dialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult)
from botbuilder.schema import ActivityTypes

from data_models import UserPreferences
from dialogs import UserPreferencesDialog
from exchange_rates_informers import ExchangeRatesInformer
from msg_responders import BaseMsgResponder, HelpMsgResponder, ChangePrefMsgResponder, ExchangeRateMsgResponder, \
    ContactMsgResponder, ConvertMsgResponder
from msg_recognizers import BaseMsgRecognizer, HelpMsgRecognizer, UserPrefMsgRecognizer, ExchangeRateMsgRecognizer, \
    RecognizedMessage, MessageIntent, ContactMsgRecognizer, ConvertMsgRecognizer
from resources import ResponseMsgs


class MainDialog(ComponentDialog):
    """Bot's main dialog."""
    # Nested dialog ids
    WATERFALL_DIALOG_ID = 'waterfall'

    def __init__(self, user_state: UserState, conversation_state: ConversationState, informer: ExchangeRatesInformer):
        # Validate input params
        if conversation_state is None:
            raise TypeError(
                f"[{MainDialog.__name__}]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                f"[{MainDialog.__name__}]: Missing parameter. user_state is required but None was given"
            )

        super(MainDialog, self).__init__(MainDialog.__name__)
        self.user_state = user_state
        self.conversation_state = conversation_state
        self.user_preferences_accessor = self.user_state.create_property("user_preferences")

        # Setup msg recognizers and responders
        self.msg_recognizers: List[BaseMsgRecognizer] = self.__create_msg_recognizers()
        self.msg_responders: List[BaseMsgResponder] = self.__create_msg_responders(informer)

        # Setup dialogs
        self.user_preferences_dialog_id = 'welcome_user_prefs'
        self.add_dialog(UserPreferencesDialog(self.user_preferences_dialog_id, user_state))

        self.add_dialog(
            WaterfallDialog(
                MainDialog.WATERFALL_DIALOG_ID,
                [
                    self.initial_step,
                    self.final_step
                ],
            )
        )
        self.initial_dialog_id = MainDialog.WATERFALL_DIALOG_ID

    async def initial_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Dialog's initial step. Main logic for request message handling is implemented here."""
        turn_context = step_context.context
        message = turn_context.activity.text
        channel = turn_context.activity.channel_id

        typing = MessageFactory.text('')
        typing.type = ActivityTypes.typing

        await turn_context.send_activity(typing)

        # Get the state properties from the turn context.
        # noinspection PyTypeChecker
        user_preferences: UserPreferences = await self.user_preferences_accessor.get(turn_context, UserPreferences)

        # If the lang in user profile is empty, which means that the user hasn't set it yet,
        #   start the user profile dialog to get it from the user. Also, if the user profile is not empty but
        #   the message text is '/start', which probably means that the user deleted the chat, and wants to start a new
        #   one, then start the conversation over.
        # NOTE: Running the user profile dialog will also set the user profile's other properties, but it's OK,
        #   because if the lang is None then the others are None too.
        # User profile is empty at the start.
        if user_preferences.lang is None or message == '/start':
            # Set a flag to send a welcome message after the dialog
            step_context.values['first_time'] = True
            return await step_context.begin_dialog(self.user_preferences_dialog_id)
        else:
            # Recognize the message
            rec_msg = await self.__recognize_message(message)

            # Find the msg responder which can respond to current message, create a respond and set it to the user.
            for msg_responder in self.msg_responders:
                if await msg_responder.can_respond(rec_msg, channel):
                    res = await msg_responder.create_response(rec_msg, channel, message, user_preferences)
                    if isinstance(res, list) or isinstance(res, tuple):
                        for msg in res:
                            await turn_context.send_activity(msg)
                        return await step_context.end_dialog()
                    elif isinstance(res, Dialog):
                        if not await self.find_dialog(res.id):
                            self.add_dialog(res)
                        return await step_context.begin_dialog(res.id)
                    else:
                        await turn_context.send_activity(res)
                        return await step_context.end_dialog()

            # Raise an exception if no message responder was found for the recognized message.
            raise Exception(
                f"{MainDialog.__name__}: no message responder for intent: {rec_msg.intent}"
                f"{f'and action: {rec_msg.action}' if rec_msg.action else ''}")

    async def final_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Dialog's final step. Dialog can reach this step if an inner dialog was begun in the initial step."""
        # Check whether this step has been reached as a result of the very first user pref dialog,
        #   and if so, send a welcome message to the user.
        if step_context.values.get('first_time'):
            user_preferences = await self.user_preferences_accessor.get(step_context.context, UserPreferences)

            welcome_message = ResponseMsgs.get('welcome', user_preferences.lang)
            help_message = ResponseMsgs.get('help', user_preferences.lang)

            res_message = f"{welcome_message}\n\n{help_message}"
            await step_context.context.send_activity(res_message)
        return await step_context.end_dialog()

    @staticmethod
    def __create_msg_recognizers() -> List[BaseMsgRecognizer]:
        """Creates and returns message recognizers."""
        return [HelpMsgRecognizer(), ContactMsgRecognizer(), UserPrefMsgRecognizer(), ExchangeRateMsgRecognizer(),
                ConvertMsgRecognizer()]

    def __create_msg_responders(self, informer: ExchangeRatesInformer) -> List[BaseMsgResponder]:
        """Creates and returns message responders."""
        return [ChangePrefMsgResponder(self.conversation_state, self.user_state),
                ContactMsgResponder(self.conversation_state, self.user_state),
                ExchangeRateMsgResponder(self.conversation_state, self.user_state, informer),
                ConvertMsgResponder(self.conversation_state, self.user_state, informer),
                # HelpMsgResponder is the default responder, so if no responder responds to a message,
                #   this one will do.
                HelpMsgResponder(self.conversation_state, self.user_state), ]

    async def __recognize_message(self, message: str) -> RecognizedMessage:
        """Tries to recognize the given message.

        :param str message: message which needs to be recognized
        :return RecognizedMessage: recognized message with intent and action attributes,
                    or instance of RecognizedMessage with the unrecognized intent.
        """
        # Try to recognize the message
        for recognizer in self.msg_recognizers:
            rec_message = recognizer.recognize(message)
            if rec_message is not None:
                return rec_message

        # If none of the recognizers managed to recognize the message, then return
        #   an instance of RecognizedMessage with unrecognized intent.
        return RecognizedMessage(MessageIntent.unknown_intent)
