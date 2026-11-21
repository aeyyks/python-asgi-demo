import asyncio


class WebSocketRouter:
    async def __call__(self, scope, receive, send):
        path = scope["path"]

        # Маршрутизируем по пути из scope
        if path == "/chat":
            await self.handle_chat(receive, send)
        elif path == "/notifications":
            await self.handle_notifications(receive, send)
        else:
            # Если путь неизвестен — закрываем сокет с кодом 4004 (кастомный код приложения)
            await send({"type": "websocket.close", "code": 4004})

    async def handle_chat(self, receive, send):
        """Маршрут /chat: интерактивный эхо-чат."""
        while True:
            event = await receive()
            if event["type"] == "websocket.connect":
                await send({"type": "websocket.accept"})
                await send({"type": "websocket.send", "text": "Добро пожаловать в чат!"})

            elif event["type"] == "websocket.receive":
                text = event.get("text", "")
                await send({"type": "websocket.send", "text": f"[Чат] Вы написали: {text}"})

            elif event["type"] == "websocket.disconnect":
                break

    async def handle_notifications(self, receive, send):
        """Маршрут /notifications: сервер сам шлёт уведомления каждые 3 секунды."""
        event = await receive()
        if event["type"] != "websocket.connect":
            return

        await send({"type": "websocket.accept"})

        # Фоновая задача: пушим уведомления клиенту, пока он не отключится
        async def push_alerts():
            count = 1
            while True:
                await asyncio.sleep(3)
                await send({
                    "type": "websocket.send",
                    "text": f"[Уведомление #{count}] Новое событие на сервере!",
                })
                count += 1

        sender_task = asyncio.create_task(push_alerts())

        try:
            # Ждём, пока клиент сам не закроет соединение
            while True:
                event = await receive()
                if event["type"] == "websocket.disconnect":
                    break
        finally:
            # Обязательно останавливаем фоновую рассылку при разрыве связи
            sender_task.cancel()
