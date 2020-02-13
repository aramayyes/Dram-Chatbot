import os


class WebAppConfig:
    """ Web App Configuration """
    PORT = os.environ.get("PORT", 3978)
    SENTRY_DSN = os.environ.get("SENTRY_DSN", '')
    MONGO_URL = os.environ.get("MONGO_URL", '')
    MONGO_DB = os.environ.get("MONGO_DB", '')
    MONGO_COL = os.environ.get("MONGO_COL", '')


class BotConfig:
    """ Bot Configuration """
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    FB_TOKEN = os.environ.get("FB_TOKEN", "")
