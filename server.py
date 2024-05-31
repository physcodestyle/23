from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ttt import Game

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

@app.post("/cross/{row_index}/{col_index}")
def put_player_input(row_index: int, col_index: int):
  turn_result = game.make_turn((row_index, col_index))
  return {
    "row_index": row_index,
    "col_index": col_index,
    "turn_result": turn_result
  }