# game_logic.py
import random

# Функция для создания пустого игрового поля 3x3
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Функция для проверки, выиграл ли игрок
def is_winner(board, player):
    # Проверка строк
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Проверка столбцов
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Проверка диагоналей
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Функция для проверки, закончилась ли игра вничью
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Функция для хода бота
def bot_move(board, bot_symbol, player_symbol):
    available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
    for r, c in available_moves:
        board[r][c] = bot_symbol
        if is_winner(board, bot_symbol):
            return r, c
        board[r][c] = ' '
    for r, c in available_moves:
        board[r][c] = player_symbol
        if is_winner(board, player_symbol):
            board[r][c] = ' '
            return r, c
        board[r][c] = ' '
    return random.choice(available_moves)