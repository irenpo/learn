# game_ui.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Символы для отображения на игровом поле
symbols = {"X": "❌", "O": "⭕", " ": "⬜"}

# Функция для отображения игрового поля с использованием символов
def print_static_board(board):
    lines = []
    for row in board:
        line = " | ".join(symbols[cell] for cell in row)
        lines.append(line)
    fixed_size = "\n-----------\n".join(lines)
    return f"\n{fixed_size}\n"

# Функция для создания клавиатуры с текущим состоянием игрового поля
def get_keyboard(board):
    keyboard = []
    for r in range(3):
        row = [InlineKeyboardButton(text=symbols[board[r][c]], callback_data=f"move:{r}:{c}") for c in range(3)]
        keyboard.append(row)
    # Добавляем кнопку "Остановить игру"
    keyboard.append([InlineKeyboardButton(text="🚫 Остановить игру", callback_data="stop_game")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Функция для создания меню с кнопками
def get_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Правила", callback_data="rules")],
        [InlineKeyboardButton(text="📜 История", callback_data="history")],
        [InlineKeyboardButton(text="Играть за ❌", callback_data="choose_X"),
         InlineKeyboardButton(text="Играть за ⭕", callback_data="choose_O")]
    ])