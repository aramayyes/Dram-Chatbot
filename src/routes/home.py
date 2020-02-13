from aiohttp import web
from aiohttp.web import Request, Response


# Default route
# Listen for incoming requests on /
async def index(req: Request) -> Response:
    return Response(text="Everything is OK")


def setup_home_routes(app: web.Application):
    app.router.add_get("/", index)
