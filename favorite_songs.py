favorite_songs = {
    'Серёга': ['Unforgiven', 'Holiday', 'Highway to hell'], 
    'Соня': ['Shake it out', 'The Show Must Go On', 'Наше лето'], 
    'Дима': ['Владимирский централ', 'Мурка', 'Третье сентября']
}
# Ниже напишите код, который напечатает на экран, сколько у Димы любимых песен
# Получаем список песен Димы
dima_songs = favorite_songs['Дима']
print(len(dima_songs))

# Ниже напишите код, который построчно напечатает
# все любимые песни Сони.
# Получаем список песен Сони
sonya_songs = favorite_songs['Соня']

# Печатаем песни построчно
for song in sonya_songs:
    print(song)
