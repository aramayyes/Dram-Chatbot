import sys
import traceback

from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter, TurnContext
from sentry_sdk import configure_scope, capture_exception

from config import BotConfig

# Create the bot framework adapter
from resources import ResponseMsgs

_CONFIG = BotConfig()
_SETTINGS = BotFrameworkAdapterSettings(_CONFIG.APP_ID, _CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(_SETTINGS)


# Catch-all for errors.
async def _on_error(context: TurnContext, error: Exception):
    # noinspection PyBroadException
    try:
        user_id = f"{context.activity.channel_id}/{context.activity.from_property.id}"
        username = context.activity.from_property.name
    except Exception:
        user_id = None
        username = None

    # Send the exception to sentry
    with configure_scope() as scope:
        scope.user = {
            "id": user_id,
            "username": username
        }

        scope.set_extra("channel", context.activity.channel_id)
        scope.set_extra("message", context.activity.text)
    capture_exception(error)

    # Log the error
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity(ResponseMsgs.get('error'))


ADAPTER.on_turn_error = _on_error
