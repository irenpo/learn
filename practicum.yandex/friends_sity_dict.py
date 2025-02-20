friends_names = ['Аня', 'Коля', 'Лёша', 'Лена', 'Миша']
friends_cities = ['Владивосток', 'Красноярск', 'Москва', 'Обнинск', 'Чебоксары']

# Объявлен пустой словарь, его нужно будет наполнить элементами, 
# каждый из которых составлен по схеме "имя: город"
friends = {}

# Наполняем словарь с помощью цикла
for name, city in zip(friends_names, friends_cities):
    friends[name] = city
    # Печатаем, чтобы проверить результат
print('Лена живёт в городе' + ' ' + (friends['Лена']))