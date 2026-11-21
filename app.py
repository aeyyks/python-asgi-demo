from handler.http_handler import HttpHandler
from handler.ws_handler import WebSocketHandler

http_app = HttpHandler()
ws_app = WebSocketHandler()


# Главная точка входа для Uvicorn
async def app(scope, receive, send):
    if scope["type"] == "http":
        await http_app(scope, receive, send)
    elif scope["type"] == "websocket":
        await ws_app(scope, receive, send)
