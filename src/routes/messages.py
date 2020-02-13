from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import BotFrameworkAdapter, ActivityHandler
from botbuilder.schema import Activity

ADAPTER = None
BOT = None


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    try:
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=201)
    except Exception as exception:
        if "unauth" in str(exception).lower():
            return Response(status=401)
        else:
            return Response(status=400)


def setup_messages_routes(app: web.Application, adapter: BotFrameworkAdapter, bot: ActivityHandler):
    global ADAPTER, BOT
    ADAPTER = adapter
    BOT = bot

    app.router.add_post("/api/messages", messages)
