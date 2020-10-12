import aiohttp_session
import discord
from aiohttp.web import HTTPFound, Request, RouteTableDef
from aiohttp_jinja2 import template

from website import utils as webutils

routes = RouteTableDef()


@routes.get("/discord")
@template('discord.j2')
@webutils.add_output_args()
async def discord_code(request: Request):
    """Index of the website"""

    return {"code": request.query.get('code')}


@routes.get("/")
@template('index.j2')
@webutils.add_output_args()
async def index(request: Request):
    """Index of the website"""

    return {}