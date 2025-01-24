mobile_devices = {
    'cucuPhone': 2010,
    'cucuBlet': 2013,
    'cucuClock': 2015,
    'cucuEar': 2018,
    'cuCube': 2015,
}

home_devices = {
    'cucuLot': 2011,
    'cucuBlock': 2010,
    'cucuWall': 2010,
    'cucuMonitor': 2020,
    'cucuLamp': 2015,
    'cucuTable': 2016,
    'cucuTV': 2017,
}

not_supported_devices = {'cucuBlock', 'cucuBlet', 'cucuWall'}

result_catalog = {}


# Функция, которая возвращает словарь поддерживаемого устройства
def get_supported_catalog(dict_devices, device):
    if device in dict_devices:
        return {device: dict_devices[device]}  # Вернуть только одну пару ключ-значение
    return {}  # Если устройства нет в словаре, вернуть пустой словарь


# Собираем полный список устройств (из двух словарей)
all_devices = set(mobile_devices.keys()).union(home_devices.keys())

# Фильтруем поддерживаемые устройства
supported_devices = all_devices - not_supported_devices

# Проверяем каждое устройство из поддерживаемых
for device in supported_devices:
    # Обработка мобильных устройств
    supported_mob_dev = get_supported_catalog(mobile_devices, device)
    result_catalog.update(supported_mob_dev)  # Добавляем в итоговый словарь

    # Обработка домашних устройств
    supported_home_dev = get_supported_catalog(home_devices, device)
    result_catalog.update(supported_home_dev)  # Добавляем в итоговый словарь

# Выводим результат
print('Каталог поддерживаемых девайсов:')
print(result_catalog)
