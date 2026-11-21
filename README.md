# python-asgi-demo

Демо-приложение на чистом ASGI (без фреймворков) — HTTP-эндпоинт с JSON-ответом и WebSocket-маршрутизатор с двумя сценариями: эхо-чат и серверные уведомления.

## Стек

- Python 3.10+
- ASGI (универсальный интерфейс `app(scope, receive, send)`)
- Uvicorn (сервер)

## Структура

| Файл | Назначение |
|------|------------|
| `app.py` | Точка входа: маршрутизация `scope["type"]` → HTTP или WebSocket |
| `handler/http_handler.py` | HTTP-обработчик: читает тело, возвращает JSON с метаданными запроса |
| `handler/ws_handler.py` | WebSocket-маршрутизатор: `/chat` (эхо) и `/notifications` (push-уведомления) |

## Маршруты / API

| Тип | Путь | Описание |
|-----|------|----------|
| HTTP GET/POST | `/` | Возвращает JSON: метод, путь, query-строку, тело запроса |
| WebSocket | `/chat` | Эхо-чат: клиент отправляет текст → сервер отвечает с префиксом `[Чат]` |
| WebSocket | `/notifications` | Сервер каждые 3 сек пушит `[Уведомление #N]` до разрыва соединения |

## Установка и запуск

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Примеры

```bash
curl http://localhost:8000/
curl -X POST -d "hello" http://localhost:8000/
```
