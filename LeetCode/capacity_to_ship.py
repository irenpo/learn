def check(weights, max_weight, days):
    current_weight = 0
    required_days = 1
    
    for weight in weights:
        # Если вес текущего контейнера превышает максимальную грузоподъемность
        if weight > max_weight:
            return False
            
        # Если добавление текущего контейнера превысит грузоподъемность
        if current_weight + weight > max_weight:
            required_days += 1
            current_weight = weight
        else:
            current_weight += weight
    
    # Проверяем, уложились ли в заданное количество дней
    return required_days <= days

def shipWithinDays(weights, days):
    # Минимальная грузоподъемность - максимальный вес одного контейнера
    min_capacity = max(weights)
    # Максимальная грузоподъемность - сумма всех весов
    max_capacity = sum(weights)
    
    # Бинарный поиск
    while min_capacity < max_capacity:
        mid = min_capacity + (max_capacity - min_capacity) // 2
        
        if check(weights, mid, days):
            max_capacity = mid
        else:
            min_capacity = mid + 1
            
    return min_capacity

# Пример использования
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5
result = shipWithinDays(weights, days)
print(f"Минимальная грузоподъемность: {result}")