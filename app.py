from handler.http_handler import HttpHandler
from handler.ws_handler import WebSocketRouter

http_app = HttpHandler()
ws_app = WebSocketRouter()


# Главная точка входа для Uvicorn
async def app(scope, receive, send):
    if scope["type"] == "http":
        await http_app(scope, receive, send)
    elif scope["type"] == "websocket":
        await ws_app(scope, receive, send)
