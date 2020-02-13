import sentry_sdk
from aiohttp import web
from botbuilder.core import UserState, ConversationState
from botbuilder.core.integration import aiohttp_error_middleware

from adapter import ADAPTER
from bots import DramRateBot
from config import WebAppConfig
from dialogs.main_dialog import MainDialog
from exchange_rates_informers import RateAmParserExchangeRatesInformer
from routes import setup_routes
from storage import MongodbStorage

# Create config
CONFIG = WebAppConfig()

# Initialize Sentry
sentry_sdk.init(
    dsn=CONFIG.SENTRY_DSN
)

# Create storage and state stores
STORAGE = MongodbStorage(CONFIG.MONGO_URL, CONFIG.MONGO_DB, CONFIG.MONGO_COL)
USER_STATE = UserState(STORAGE)
CONVERSATION_STATE = ConversationState(STORAGE)

# Create main dialog
INFORMER = RateAmParserExchangeRatesInformer()
MAIN_DIALOG = MainDialog(USER_STATE, CONVERSATION_STATE, INFORMER)

# Create the Bot
BOT = DramRateBot(CONVERSATION_STATE, USER_STATE, MAIN_DIALOG)

# Create the aiohttp web app
APP = web.Application(middlewares=[aiohttp_error_middleware])
setup_routes(APP, ADAPTER, BOT)

if __name__ == "__main__":
    try:
        web.run_app(APP, port=CONFIG.PORT)
    except Exception as error:
        raise error
