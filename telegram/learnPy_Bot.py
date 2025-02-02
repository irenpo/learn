import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Токен бота, полученный от BotFather
TOKEN = "7971363257:AAFK4jnC0P_ALoyRXpjd0JjtxIRrwI2OakM"

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

# Функция для выбора случайного хода бота
def bot_move(board, bot_symbol):
    available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
    return random.choice(available_moves) if available_moves else None

# Обработчик команды /start
@router.message(Command("start"))
async def start_game(message: Message):
    # Инициализация состояния игры для текущего чата
    game_state[message.chat.id] = {
        "board": create_board(),  # Создание пустой доски
        "player_symbol": None,    # Символ игрока (X или O)
        "bot_symbol": None        # Символ бота (O или X)
    }
    await message.answer("Привет! Выбери, за кого играешь (X или O):")

# Обработчик всех сообщений, кроме команды /start
@router.message()
async def game_handler(message: Message):
    chat_id = message.chat.id
    # Если состояние игры для этого чата не инициализировано, запускаем игру
    if chat_id not in game_state:
        await start_game(message)
        return
    
    state = game_state[chat_id]
    text = message.text.upper()  # Приводим текст сообщения к верхнему регистру
    
    # Если игрок еще не выбрал символ (X или O)
    if state["player_symbol"] is None:
        if text in ['X', 'O']:
            # Устанавливаем символы для игрока и бота
            state["player_symbol"] = text
            state["bot_symbol"] = 'O' if text == 'X' else 'X'
            await message.answer(f"Ты играешь за {state['player_symbol']}, я за {state['bot_symbol']}.")
            await message.answer(f"Вот игровое поле:\n{print_board(state['board'])}\nТвой ход! Введи координаты (например, A1):")
        else:
            await message.answer("Некорректный выбор. Выбери X или O.")
        return
    
    # Парсим ход игрока
    move = parse_move(text)
    if move:
        row, col = move
        # Проверяем, свободна ли клетка
        if state["board"][row][col] == ' ':
            # Делаем ход игрока
            state["board"][row][col] = state["player_symbol"]
            # Проверяем, выиграл ли игрок
            if is_winner(state["board"], state["player_symbol"]):
                await message.answer(f"{print_board(state['board'])}\nПоздравляю, ты победил!")
                del game_state[chat_id]  # Удаляем состояние игры
                return
            # Проверяем, закончилась ли игра вничью
            if is_draw(state["board"]):
                await message.answer(f"{print_board(state['board'])}\nНичья!")
                del game_state[chat_id]
                return
            
            # Ход бота
            bot_move_result = bot_move(state["board"], state["bot_symbol"])
            if bot_move_result:
                bot_r, bot_c = bot_move_result
                state["board"][bot_r][bot_c] = state["bot_symbol"]
                # Проверяем, выиграл ли бот
                if is_winner(state["board"], state["bot_symbol"]):
                    await message.answer(f"{print_board(state['board'])}\nБот победил! Попробуй еще раз.")
                    del game_state[chat_id]
                    return
                # Проверяем, закончилась ли игра вничью
                if is_draw(state["board"]):
                    await message.answer(f"{print_board(state['board'])}\nНичья!")
                    del game_state[chat_id]
                    return
            
            # Показываем обновленное состояние доски и ждем хода игрока
            await message.answer(f"{print_board(state['board'])}\nТвой ход! Введи координаты:")
        else:
            await message.answer("Эта клетка уже занята, попробуй снова.")
    else:
        await message.answer("Некорректный ввод. Используй формат A1, B2 и т. д.")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())