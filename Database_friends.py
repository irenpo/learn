DATABASE = {
    'Серёга': 'Омск',
    'Соня': 'Москва',
    'Миша': 'Москва',
    'Дима': 'Челябинск',
    'Алина': 'Красноярск',
    'Егор': 'Пермь',
    'Коля': 'Красноярск'
}

def process_anfisa(query):
    if query == 'Сколько у меня друзей?':
        count = len(DATABASE)
        return 'У тебя ' + str(count) + ' друзей.'
    elif query == 'Кто все мои друзья?':  # Проверяем второй запрос
        friends_string = ''
        for friend in DATABASE.keys():  # Перебираем ключи словаря (имена друзей)
            friends_string += friend + ' '  # Добавляем имя друга и пробел
        return 'Твои друзья: ' + friends_string.strip()  # Убираем лишний пробел в конце
    elif query == 'Где все мои друзья?':  # Проверяем третий запрос
        friends_string = ''
        for friend in set(DATABASE.values()):  # Перебираем значения  словаря (названия городов)
            friends_string += friend + ' '  # Добавляем город друга и пробел
        return 'Твои друзья в городах: ' + friends_string.strip()  # Убираем лишний пробел в конце
    else:
        return '<неизвестный запрос>'

# Не изменяйте следующий код
print('Привет, я Анфиса!')
print(process_anfisa('Сколько у меня друзей?'))
print(process_anfisa('Кто все мои друзья?'))
print(process_anfisa('Где все мои друзья?'))