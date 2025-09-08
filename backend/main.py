# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://charlesfeng2021.github.io",  # your site
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoveRequest(BaseModel):
    board: list[str]  # Example: ["X","O","","","","","","",""]
# Determine if there is a winner
def check_winner(board):
    winning_combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in winning_combos:
        if board[a] != "" and board[a] == board[b] and board[a] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

# Minimax algorithm
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

# Pick the best move
def best_move(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.post("/move")
def get_ai_move(req: MoveRequest):
    board = req.board
    move = best_move(board)
    return {"move": move}