import aiohttp
from aiohttp import web

from config import HOST, PORT

routes = web.RouteTableDef()

app = web.Application()
web.run_app(app,host=HOST,port=PORT)
