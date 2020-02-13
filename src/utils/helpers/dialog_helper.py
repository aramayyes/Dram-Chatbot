from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


class DialogHelper:
    """ Contains methods for working with dialogs. """

    @staticmethod
    async def run_dialog(
            dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ) -> DialogTurnStatus:
        """ Runs the given dialog and returns the turn status.

        :param dialog: dialog to run
        :param turn_context: turn context
        :param accessor: StatePropertyAccessor to use for dialog state
        :return DialogTurnStatus: Dialog's turn status
         """
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            results = await dialog_context.begin_dialog(dialog.id)

        return results.status
