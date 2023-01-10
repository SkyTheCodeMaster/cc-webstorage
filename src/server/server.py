import json

import aiohttp
from aiohttp import web

from config import HOST, PORT
from funcs import commands

routes = web.RouteTableDef()

@routes.get("/")
async def ws_handler(request: web.Request) -> web.Response:
  ws = web.WebSocketResponse()
  await ws.prepare(request)
  async for msg in ws:
    if msg.type == aiohttp.WSMsgType.TEXT:
      data = msg.json()
      command = data.get("command")
      if not command: await ws.send("invalid command")
      if command in commands:
        cmd = commands[command]
        args = data.get("arguments")
        out = cmd(*args)
        await ws.send(json.dumps(out))
      elif command == "close":
        await ws.close()

    elif msg.type == aiohttp.WSMsgType.ERROR:
      print('ws connection closed with exception %s' %
      ws.exception())

  print('websocket connection closed')
  return ws

app = web.Application()

app.add_routes(routes)

web.run_app(app,host=HOST,port=PORT)