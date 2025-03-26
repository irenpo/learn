import pytest
from game_logic import create_board, is_winner, is_draw, bot_move
from game_ui import print_static_board, get_keyboard, get_menu, symbols

# Тесты для game_logic.py
def test_create_board():
    """Проверяем, что создаётся пустое поле 3x3."""
    board = create_board()
    assert len(board) == 3
    assert all(len(row) == 3 for row in board)
    assert all(cell == ' ' for row in board for cell in row)

@pytest.mark.parametrize("board, player, expected", [
    ([['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']], 'X', True),  # Горизонталь
    ([[' ', ' ', ' '], ['O', 'O', 'O'], [' ', ' ', ' ']], 'O', True),  # Горизонталь
    ([['X', ' ', ' '], ['X', ' ', ' '], ['X', ' ', ' ']], 'X', True),  # Вертикаль
    ([['X', ' ', ' '], [' ', 'X', ' '], [' ', ' ', 'X']], 'X', True),  # Диагональ
    ([[' ', ' ', 'X'], [' ', 'X', ' '], ['X', ' ', ' ']], 'X', True),  # Обратная диагональ
    ([['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']], 'X', False),  # Нет победы
])
def test_is_winner(board, player, expected):
    """Проверяем определение победителя."""
    assert is_winner(board, player) == expected

def test_is_draw():
    """Проверяем определение ничьи."""
    full_board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert is_draw(full_board) is True
    empty_board = create_board()
    assert is_draw(empty_board) is False

def test_bot_move():
    """Проверяем ход бота (блокировка победы игрока)."""
    board = [['X', 'X', ' '], ['O', ' ', ' '], [' ', ' ', ' ']]
    player_symbol = 'X'
    bot_symbol = 'O'
    r, c = bot_move(board, bot_symbol, player_symbol)
    assert 0 <= r <= 2 and 0 <= c <= 2
    assert board[r][c] == ' '

def test_bot_move_winning():
    """Проверяем, что бот делает выигрышный ход."""
    board = [['O', 'O', ' '], ['X', ' ', ' '], ['X', ' ', ' ']]
    bot_symbol = 'O'
    player_symbol = 'X'
    r, c = bot_move(board, bot_symbol, player_symbol)
    assert (r, c) == (0, 2)

def test_bot_move_random():
    """Проверяем, что бот делает случайный ход, если нет выигрышных или блокирующих ходов."""
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    bot_symbol = 'O'
    player_symbol = 'X'
    r, c = bot_move(board, bot_symbol, player_symbol)
    assert 0 <= r <= 2 and 0 <= c <= 2
    assert board[r][c] == ' '

def test_bot_move_no_moves():
    """Проверяем, что бот выбросит исключение, если нет доступных ходов."""
    board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 'O', 'X']]
    bot_symbol = 'O'
    player_symbol = 'X'
    with pytest.raises(ValueError, match="No available moves left"):
        bot_move(board, bot_symbol, player_symbol)

def test_bot_move_no_blocking_needed():
    """Проверяем, что бот проверяет ходы игрока, но не блокирует, и доходит до случайного хода."""
    board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    bot_symbol = 'O'
    player_symbol = 'X'
    r, c = bot_move(board, bot_symbol, player_symbol)
    assert 0 <= r <= 2 and 0 <= c <= 2
    assert board[r][c] == ' '

def test_bot_move_block_vertical():
    """Проверяем, что бот блокирует победу игрока по вертикали."""
    board = [['X', ' ', ' '], ['X', ' ', ' '], [' ', ' ', ' ']]
    bot_symbol = 'O'
    player_symbol = 'X'
    r, c = bot_move(board, bot_symbol, player_symbol)
    assert (r, c) == (2, 0)

# Тесты для game_ui.py
def test_print_static_board():
    """Проверяем форматирование игрового поля."""
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    result = print_static_board(board)
    expected = "\n❌ | ⬜ | ⭕\n-----------\n⬜ | ❌ | ⬜\n-----------\n⭕ | ⬜ | ❌\n"
    assert result == expected

def test_get_keyboard():
    """Проверяем генерацию клавиатуры."""
    board = [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]
    keyboard = get_keyboard(board)
    assert len(keyboard.inline_keyboard) == 4
    assert keyboard.inline_keyboard[0][0].text == symbols['X']
    assert keyboard.inline_keyboard[1][1].text == symbols['O']
    assert keyboard.inline_keyboard[3][0].callback_data == "stop_game"

def test_get_menu():
    """Проверяем генерацию меню."""
    menu = get_menu()
    assert len(menu.inline_keyboard) == 3
    assert menu.inline_keyboard[0][0].text == "ℹ️ Правила"
    assert menu.inline_keyboard[1][0].text == "📜 История"
    assert menu.inline_keyboard[2][0].callback_data == "choose_X"
    assert menu.inline_keyboard[2][1].callback_data == "choose_O"

# Фикстура для пустого поля
@pytest.fixture
def empty_board():
    return create_board()

def test_is_winner_empty_board(empty_board):
    """Проверяем, что на пустом поле нет победителя."""
    assert is_winner(empty_board, 'X') is False
    assert is_winner(empty_board, 'O') is False