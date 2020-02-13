from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
from botbuilder.dialogs import Dialog

from exchange_rates_informers import RateAmParserExchangeRatesInformer
from utils.helpers import DialogHelper

informer = RateAmParserExchangeRatesInformer()


class DramRateBot(ActivityHandler):
    """App's main bot, which will send dram exchange rates to the users."""

    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: Dialog) -> None:
        if conversation_state is None:
            raise TypeError(
                f"[{DramRateBot.__name__}]: Missing parameter. conversation_state is required but None was given."
            )
        if user_state is None:
            raise TypeError(
                f"[{DramRateBot.__name__}]: Missing parameter. user_state is required but None was given."
            )
        if dialog is None:
            raise TypeError(
                f"[{DramRateBot.__name__}]: Missing parameter. dialog is required but None was given."
            )

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.main_dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.text is None:
            return

        await DialogHelper.run_dialog(
            self.main_dialog,
            turn_context,
            self.conversation_state.create_property("dialog_state"),
        )
