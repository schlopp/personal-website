from aiohttp.web import Request, RouteTableDef
from aiohttp_jinja2 import template

routes = RouteTableDef()


@routes.get("/")
@template('index.j2')
async def index(request: Request):
    """Index of the website"""

    return {}
    