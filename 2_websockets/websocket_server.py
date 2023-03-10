import asyncio
import websockets  # Установите этот пакет, если у вас его нет

peoples = {}  # Словарь будет содержать ник подключившегося человека и указатель на его websocket-соединение.
# Это понадобится для маршрутизации сообщений между пользователями

async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    # При подключнии к серверу попросим указать свой ник и пополним им словарь peoples
    await websocket.send('Представьтесь!') # Метод websocket.send отправляет сообщение пользователю
    name = await websocket.recv()  # websocket.recv ожидает получения сообщения
    await websocket.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.')
    await websocket.send('Посмотреть список участников можно командой "?"')
    peoples[name.strip()] = websocket
    return name

async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None: 
    name = await welcome(websocket)
    while True:
        try:
            message = (await websocket.recv()).strip()
        except websockets.exceptions.ConnectionClosed:
            del peoples[name]
            await asyncio.gather(*(ws.send(f"{name} вышел из чата") for name, ws in peoples.items()))
            break
        if not message.find(':'):
            await websocket.send("Неправильный формат сообщения. Используйте: '<имя>: <сообщение>'")
            continue
        if message == '?':  # На знак вопроса вернём список ников подключившихся людей
            await websocket.send(', '.join(peoples.keys()))
            continue
        try:
            name_to, message = message.split(':')
            name_to = name_to.strip()
            message = message.strip()
        except ValueError:
            await websocket.send("Неправильный формат сообщения. Используйте: '<имя>: <сообщение>'")
            continue
        if name_to not in peoples:
            await websocket.send("Пользователя с таким именем нет в чате")
            continue
        await peoples[name_to].send(f"{name}: {message}")


# Создаём сервер, который будет обрабатывать подключения
ws_server = websockets.serve(receiver, "localhost", 8765)

# Запускаем event-loop
loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()