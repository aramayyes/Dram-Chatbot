from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, ActivityHandler

from .home import setup_home_routes
from .messages import setup_messages_routes


def setup_routes(app: web.Application, adapter: BotFrameworkAdapter, bot: ActivityHandler):
    setup_home_routes(app)
    setup_messages_routes(app, adapter, bot)
