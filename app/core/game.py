import asyncio
import random
from typing import Dict
from fastapi import WebSocket
from starlette.websockets import WebSocketState

from app.core.player import Player
from app.core.message import WinMessage, NewGameMessage, ServerMessage


class Game:

    def __init__(self):
        self.target: int = random.randint(1, 100)
        self.players: Dict[WebSocket, Player] = {}

    def new_round(self):
        self.target: int = random.randint(1, 100)


    async def broadcast(self, message: str, exclude: WebSocket = None):
        for ws, player in self.players.items():
            if ws != exclude and ws.client_state == WebSocketState.CONNECTED:
                await ws.send_text(message)

    async def handle_guess(self, websocket: WebSocket, guess: int):
        if guess < self.target:
            return "Больше"
        elif guess > self.target:
            return "Меньше"
        else:
            winner = self.players[websocket]
            winner.wins += 1

            await websocket.send_text("Вы угадали!") # ServerMessage(message="Вы угадали!").json()

            await self.broadcast(
                f"{winner.name} угадал число {self.target}!",
                exclude=websocket
            )

            await asyncio.sleep(5)

            self.new_round()
            await self.broadcast("Новая игра началась!") # NewGameMessage(message="Новая игра началась!").json()
            return ""
