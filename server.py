from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ttt import Game, messages

app = FastAPI()

origins = [
  "http://127.0.0.1:8080"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)

game = Game()


@app.get("/")
def options_player_input():
  return {"GET": "ALLOWED"}


@app.options("/cross/{row_index}/{col_index}")
def options_player_input(row_index: int, col_index: int):
  return {"RESPONSE": "ALLOWED"}

@app.post("/game/start")
def start_game():
  global game
  game = Game()
  return {
    "turn_result": (True, game.field.get_field(), game.is_game_not_finished(), messages["GAME_IS_STARTING"])
  }



@app.post("/cross/{row_index}/{col_index}")
def put_player_input(row_index: int, col_index: int):
  global game
  if game == None:
    return {
      "turn_result": (False, [[]], False, messages["GAME_IS_NOT_STARTING"])
    }
  else:
    return {
      "turn_result": game.make_turn((row_index, col_index))
    }