import json


class HttpHandler:
    async def __call__(self, scope, receive, send):

        # Читаем тело входящего запроса через канал receive
        # Тело может приходить частями (чанками), поэтому собираем его в цикле
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break

        # Формируем полезную нагрузку ответа на основе данных из scope
        response_data = {
            "message": "Привет из чистого ASGI!",
            "method": scope["method"],
            "path": scope["path"],
            "query_string": scope["query_string"].decode("utf-8"),
            "received_body": body.decode("utf-8"),
        }
        response_bytes = json.dumps(response_data, ensure_ascii=False).encode("utf-8")

        # Отправляем заголовки ответа (аналог start_response в WSGI)
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
            ],
        })

        # Отправляем само тело ответа
        await send({
            "type": "http.response.body",
            "body": response_bytes,
        })
