# main.py
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

# Импорт функций из других файлов
from game_logic import create_board, is_winner, is_draw, bot_move
from game_ui import print_static_board, get_keyboard, get_menu, symbols

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