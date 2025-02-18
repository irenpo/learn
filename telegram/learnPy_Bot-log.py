import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Токен бота, полученный от BotFather
TOKEN = "  "

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Словарь для хранения состояния игры для каждого чата
game_state = {}

# Функция для создания пустой игровой доски 3x3
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Функция для отображения текущего состояния доски в виде строки
def print_board(board):
    board_str = "   A   B   C\n  -------------\n"
    for i, row in enumerate(board, 1):
        board_str += f"{i} | {' | '.join(row)} |\n  -------------\n"
    return board_str

# Функция для преобразования ввода пользователя (например, "A1") в координаты доски (строка, столбец)
def parse_move(move):
    letters = {'A': 0, 'B': 1, 'C': 2}
    if len(move) == 2 and move[0] in letters and move[1] in '123':
        return int(move[1]) - 1, letters[move[0]]
    return None

# Функция для проверки, выиграл ли игрок с указанным символом (X или O)
def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Функция для проверки, закончилась ли игра вничью
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Функция для выбора хода бота с выигрышной стратегией
def bot_move(board, bot_symbol, player_symbol):
    # Проверка на возможность победы бота
    for r, c in [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']:
        board[r][c] = bot_symbol
        if is_winner(board, bot_symbol):
            return r, c
        board[r][c] = ' '
    
    # Блокировка победы игрока
    for r, c in [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']:
        board[r][c] = player_symbol
        if is_winner(board, player_symbol):
            board[r][c] = ' '
            return r, c
        board[r][c] = ' '
    
    # Иначе случайный ход
    return random.choice([(r, c) for r in range(3) for c in range(3) if board[r][c] == ' '])

# Обработчик команды /start
@router.message(Command("start"))
async def start_game(message: Message):
    print("Бот запущен!")
    game_state[message.chat.id] = {
        "board": create_board(),
        "player_symbol": None,
        "bot_symbol": None
    }
    await message.answer("Привет! Выбери, за кого играешь (X или O):")

# Обработчик всех сообщений, кроме команды /start
@router.message()
async def game_handler(message: Message):
    chat_id = message.chat.id
    if chat_id not in game_state:
        await start_game(message)
        return
    
    state = game_state[chat_id]
    text = message.text.upper()
    
    if state["player_symbol"] is None:
        if text in ['X', 'O']:
            state["player_symbol"] = text
            state["bot_symbol"] = 'O' if text == 'X' else 'X'
            await message.answer(f"Ты играешь за {state['player_symbol']}, я за {state['bot_symbol']}.")
            if state["player_symbol"] == "O":
                bot_r, bot_c = bot_move(state["board"], state["bot_symbol"], state["player_symbol"])
                state["board"][bot_r][bot_c] = state["bot_symbol"]
                await message.answer(f"Я сходил: {chr(bot_c + 65)}{bot_r + 1}\n{print_board(state['board'])}\nТвой ход!")
            else:
                await message.answer(f"Вот игровое поле:\n{print_board(state['board'])}\nТвой ход! Введи координаты (например, A1):")
        else:
            await message.answer("Некорректный выбор. Выбери X или O.")
        return
    
    move = parse_move(text)
    if move:
        row, col = move
        if state["board"][row][col] == ' ':
            state["board"][row][col] = state["player_symbol"]
            if is_winner(state["board"], state["player_symbol"]):
                await message.answer(f"{print_board(state['board'])}\nПоздравляю, ты победил!")
                del game_state[chat_id]
                return
            if is_draw(state["board"]):
                await message.answer(f"{print_board(state['board'])}\nНичья!")
                del game_state[chat_id]
                return
            bot_r, bot_c = bot_move(state["board"], state["bot_symbol"], state["player_symbol"])
            state["board"][bot_r][bot_c] = state["bot_symbol"]
            if is_winner(state["board"], state["bot_symbol"]):
                await message.answer(f"{print_board(state['board'])}\nБот победил! Попробуй еще раз.")
                del game_state[chat_id]
                return
            if is_draw(state["board"]):
                await message.answer(f"{print_board(state['board'])}\nНичья!")
                del game_state[chat_id]
                return
            await message.answer(f"Я сходил: {chr(bot_c + 65)}{bot_r + 1}\n{print_board(state['board'])}\nТвой ход!")
        else:
            await message.answer("Эта клетка уже занята, попробуй снова.")
    else:
        await message.answer("Некорректный ввод. Используй формат A1, B2 и т. д.")

# Основная функция для запуска бота
async def main():
    print("Бот запущен и ожидает команды...")
    await dp.start_polling(bot, skip_updates=True)

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())