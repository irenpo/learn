import pytest
from capacity_to_ship import shipWithinDays 

def test_basic_case():
    # Базовый случай из примера
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = 5
    assert shipWithinDays(weights, days) == 15

def test_single_day():
    # Все контейнеры за один день
    weights = [1, 2, 3, 4]
    days = 1
    assert shipWithinDays(weights, days) == 10

def test_each_container_separate():
    # Каждый контейнер в отдельный день
    weights = [1, 2, 3]
    days = 3
    assert shipWithinDays(weights, days) == 3

def test_minimum_capacity():
    # Минимум дней равен количеству контейнеров
    weights = [5, 5, 5, 5]
    days = 4
    assert shipWithinDays(weights, days) == 5

def test_large_weights():
    # Большие веса
    weights = [100, 200, 300, 400]
    days = 2
    assert shipWithinDays(weights, days) == 600

def test_single_container():
    # Один контейнер
    weights = [10]
    days = 1
    assert shipWithinDays(weights, days) == 10

def test_equal_distribution():
    # Равномерное распределение
    weights = [10, 10, 10, 10]
    days = 2
    assert shipWithinDays(weights, days) == 20

@pytest.mark.parametrize("weights, days, expected", [
    ([1, 2, 3], 2, 4),
    ([3, 2, 1], 3, 3),
    ([1, 2, 3, 1, 2, 3], 3, 6),
])
def test_various_cases(weights, days, expected):
    assert shipWithinDays(weights, days) == expected

if __name__ == "__main__":
    pytest.main()