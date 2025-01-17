all_cities = {
    'Абакан',
    'Астрахань', 
    'Бобруйск', 
    'Калуга',
    'Караганда',
    'Кострома',
    'Липецк', 
    'Новосибирск'
}

used_cities = {'Калуга', 'Абакан' , 'Новосибирск'}

def print_valid_cities(all_cities, used_cities):
    valid_cities = all_cities - used_cities
    if valid_cities:
        for city in valid_cities:
            print(city)
    else:
        print("Все города уже были использованы")


print_valid_cities(all_cities, used_cities)
