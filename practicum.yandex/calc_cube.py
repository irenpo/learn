# Функция для вычисления периметра куба.
def calc_cube_perimeter(side):
    return side * 12

# 3 метра - это длина ребра куба.

one_cube_perimeter = calc_cube_perimeter(3)

# Вычислите общую длину палок, необходимых 
# для строительства 8 кубов, 
# и сохраните это значение в переменную full_length 
full_length = one_cube_perimeter * 8

# А теперь напечатаем результат 
print('Необходимый метраж палок для 8 кубов:', full_length)


# Функция для вычисления площади куба.
def calc_cube_area(side):
    # Формулу для вычисления площади одной грани куба Афанасий написал:
    one_face = side * side

    # Вычислите полную площадь куба: у него шесть одинаковых граней.
    cube_area = one_face * 6

    # Удалите многоточие и допишите функцию так, 
    # чтобы она возвращала полную площадь куба
    return cube_area

# Присвойте переменной one_cube_area значение,
# которое вернёт функция calc_cube_area() с аргументом 3:
# 3 метра - это длина ребра куба.
one_cube_area = calc_cube_area(3)

# Вычислите общую площадь стекла, необходимого 
# для строительства 8 кубов, 
# и сохраните это значение в переменную full_area 
full_area = one_cube_area * 8

print('Необходимая площадь стекла для 8 кубов, кв.м:', full_area)


# Правильный калькулятор

# Функция для вычисления периметра кубов.
def calc_cube_perimeter(side):
    return side * 12


# Функция для вычисления площади кубов.
def calc_cube_area(side):
    one_face = side * side
    cube_area = one_face * 6
    return cube_area


# Дополните объявление функции: 
# теперь должна принимать два параметра -
# длину ребра куба и количество кубов.
def calc_cube(side, quantity):
    # Вызываем функцию, рассчитывающую периметр
    # и передаём в неё размер куба
    one_cube_perimeter = calc_cube_perimeter(side)

    # Здесь вместо многоточия должна стоять переменная, 
    # хранящая количество кубов, переданное во втором аргументе.
    full_length = one_cube_perimeter * quantity

    # Вызываем функцию, рассчитывающую площадь стекла
    # и передаём в неё размер куба
    one_cube_area = calc_cube_area(side)

    # Здесь вместо многоточия должна стоять переменная, 
    # хранящая количество кубов, переданное во втором аргументе.
    full_area = one_cube_area * quantity

    # В этой строке замените многоточие на переменную, хранящую количество кубов
    print('Для', quantity, 'кубов понадобится палок (м):', full_length, 'и стекла (кв.м):', full_area)


# Для проверки работы кода вызываем функцию с двумя аргументами: 
# 3 - это размер ребра куба,
# 2 - это необходимое количество кубов
calc_cube(3, 2)