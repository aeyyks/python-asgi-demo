class WebSocketHandler:
    async def __call__(self, scope, receive, send):
        while True:
            event = await receive()

            # 1. Клиент запрашивает установку соединения — подтверждаем
            if event["type"] == "websocket.connect":
                await send({"type": "websocket.accept"})

            # 2. Клиент прислал сообщение — отправляем его обратно (эхо)
            elif event["type"] == "websocket.receive":
                text = event.get("text")
                data = event.get("bytes")

                if text is not None:
                    await send({
                        "type": "websocket.send",
                        "text": f"Эхо: {text}",
                    })
                elif data is not None:
                    await send({
                        "type": "websocket.send",
                        "bytes": data,
                    })

            # 3. Клиент разорвал соединение — выходим из цикла
            elif event["type"] == "websocket.disconnect":
                break
