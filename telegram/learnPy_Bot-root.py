import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

# Токен вашего бота в Telegram
TOKEN = "7971363257:AAFK4jnC0P_ALoyRXpjd0JjtxIRrwI2OakM"  # Замените на ваш токен

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Словарь для хранения состояния игры для каждого чата
game_state = {}

# Словарь для хранения истории игр для каждого чата
game_history = {}

# Символы для отображения на игровом поле
symbols = {"X": "❌", "O": "⭕", " ": "⬜"}

# Функция для создания пустого игрового поля 3x3
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Функция для отображения игрового поля с использованием символов
def print_static_board(board):
    lines = []
    for row in board:
        line = " | ".join(symbols[cell] for cell in row)
        lines.append(line)
    fixed_size = "\n-----------\n".join(lines)
    return f"\n{fixed_size}\n"

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

# Обработчик команды /start
@router.message(Command("start"))
async def start_game(message: Message):
    # Инициализация состояния игры для текущего чата
    game_state[message.chat.id] = {
        "board": create_board(),
        "player_symbol": None,
        "bot_symbol": None
    }
    # Отправка сообщения с меню выбора символа
    await message.answer("Привет! Выбери, за кого играешь:", reply_markup=get_menu())

# Обработчик callback-запросов от кнопок
@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if callback.data == "stop_game":
        # Остановка игры и сохранение её в историю как незавершённой
        state = game_state.get(chat_id)
        if state:
            result = f"Игра {len(game_history.get(chat_id, [])) + 1} - Игра прервана:\n{print_static_board(state['board'])}"
            if chat_id not in game_history:
                game_history[chat_id] = []
            game_history[chat_id].append(result)
            del game_state[chat_id]  # Удаляем состояние игры
            await callback.message.edit_text("Игра остановлена. Начните новую игру с помощью команды /start.", reply_markup=get_menu())
        return
    elif callback.data == "rules":
        # Отправка правил игры
        await callback.message.answer("Выберите X или O. Игра идет по правилам крестиков-ноликов. Делайте ход, нажимая на кнопку на игровом поле.")
    elif callback.data == "history":
        # Отображение истории игр
        if chat_id in game_history and game_history[chat_id]:
            history_text = "История игр:\n\n" + "\n\n".join(game_history[chat_id])
            await callback.message.answer(history_text)
        else:
            await callback.message.answer("История игр пуста.")
    elif callback.data.startswith("choose_"):
        # Выбор символа игроком
        player_symbol = "X" if callback.data == "choose_X" else "O"
        bot_symbol = "O" if player_symbol == "X" else "X"
        game_state[chat_id] = {
            "board": create_board(),
            "player_symbol": player_symbol,
            "bot_symbol": bot_symbol
        }
        state = game_state[chat_id]
        # Если игрок выбрал O, бот делает первый ход
        if player_symbol == "O":
            bot_r, bot_c = bot_move(state["board"], bot_symbol, player_symbol)
            state["board"][bot_r][bot_c] = bot_symbol
        await callback.message.edit_text(f"Ты играешь за {symbols[state['player_symbol']]}, я за {symbols[state['bot_symbol']]}\nТвой ход!", reply_markup=get_keyboard(state["board"]))
    elif callback.data.startswith("move"):
        # Обработка хода игрока
        _, r, c = callback.data.split(":")
        r, c = int(r), int(c)
        state = game_state.get(chat_id)
        if state and state["board"][r][c] == ' ':
            state["board"][r][c] = state["player_symbol"]
            # Проверка, выиграл ли игрок
            if is_winner(state["board"], state["player_symbol"]):
                result = f"Игра {len(game_history.get(chat_id, [])) + 1} - Победа игрока:\n{print_static_board(state['board'])}"
                if chat_id not in game_history:
                    game_history[chat_id] = []
                game_history[chat_id].append(result)
                await callback.message.edit_text(f"{print_static_board(state['board'])}\nТы победил!", reply_markup=get_menu())
                return
            # Проверка, закончилась ли игра вничью
            if is_draw(state["board"]):
                result = f"Игра {len(game_history.get(chat_id, [])) + 1} - Ничья:\n{print_static_board(state['board'])}"
                if chat_id not in game_history:
                    game_history[chat_id] = []
                game_history[chat_id].append(result)
                await callback.message.edit_text(f"{print_static_board(state['board'])}\nНичья!", reply_markup=get_menu())
                return
            # Ход бота
            bot_r, bot_c = bot_move(state["board"], state["bot_symbol"], state["player_symbol"])
            state["board"][bot_r][bot_c] = state["bot_symbol"]
            # Проверка, выиграл ли бот
            if is_winner(state["board"], state["bot_symbol"]):
                result = f"Игра {len(game_history.get(chat_id, [])) + 1} - Победа бота:\n{print_static_board(state['board'])}"
                if chat_id not in game_history:
                    game_history[chat_id] = []
                game_history[chat_id].append(result)
                await callback.message.edit_text(f"{print_static_board(state['board'])}\nБот победил!", reply_markup=get_menu())
                return
            # Проверка, закончилась ли игра вничью
            if is_draw(state["board"]):
                result = f"Игра {len(game_history.get(chat_id, [])) + 1} - Ничья:\n{print_static_board(state['board'])}"
                if chat_id not in game_history:
                    game_history[chat_id] = []
                game_history[chat_id].append(result)
                await callback.message.edit_text(f"{print_static_board(state['board'])}\nНичья!", reply_markup=get_menu())
                return
            # Обновление игрового поля и запрос следующего хода игрока
            await callback.message.edit_reply_markup(reply_markup=get_keyboard(state["board"]))
    await callback.answer("Я сходил, теперь твой ход.")

# Основная функция для запуска бота
async def main():
    try:
        print("Бот запущен и ожидает команды...")
        await asyncio.sleep(0.1)  # Добавляем небольшую задержку
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())