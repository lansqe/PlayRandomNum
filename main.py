from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.core.game import Game
from app.dtos.message import GuessMessage
from app.core.player import Player


app = FastAPI()
game = Game()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    player = Player.create()
    game.players[websocket] = player

    try:
        await websocket.send_text("Добро пожаловать! Угадайте число от 1 до 100.")

        while True:
            data = await websocket.receive_text()
            try:
                guess = GuessMessage.model_validate_json(data)
                result = await game.handle_guess(websocket, guess.guess)

                if result and result != "":
                    await websocket.send_text(result)

            except ValueError as e:
                await websocket.send_text(f'Ошибка: {str(e)}. Отправьте {{"guess": число}}')

    except WebSocketDisconnect:
        if websocket in game.players:
            del game.players[websocket]
