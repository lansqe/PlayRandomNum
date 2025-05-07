from pydantic import BaseModel


class GuessMessage(BaseModel):
    guess: int


class ServerMessage(BaseModel):
    message: str


class WinMessage(ServerMessage):
    winner_id: str
    winner_name: str
    target: int


class NewGameMessage(ServerMessage):
    ...

