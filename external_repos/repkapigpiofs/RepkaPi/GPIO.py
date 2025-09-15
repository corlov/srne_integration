# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Портирование и доработка под Repka Pi 4 (c) 2025 Семён Платцев 

import os
import time
import atexit

import fcntl
import struct

from .PWM_A import PWM_A

from . import sysfs
from . import event
from . import constants 
from .Exceptions import (InvalidPinException, InvalidDirectionException,
                         InvalidPullException, InvalidChannelException,
                         SetupException, PermissionException)


# --- Глобальные переменные для хранения распиновки ---
# Они будут заполнены при первом обращении к библиотеке
BOARD_TO_BCM = None
BCM_TO_BOARD = None
PIN_FUNCTIONS = None
SUNXI_TO_BCM  = None
BCM_TO_SUNXI = None
PORT_PULL_OFFSET_MAP = None
# ----------------------------------------------------

# Режим нумерации GPIO
gpio_mode = None

# Список каналов
gpio_direction = {}

# Ручной выбор платы
_manual_board_model = None


def _get_board_model():
    """Определяет модель платы Repka Pi, читая /proc/device-tree/model."""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
        if 'Repka-Pi4-Optimal' in model:
            return 4
        # Добавляем проверки для других моделей по аналогии
        elif 'Repka-Pi3-H5' in model:
            return 3
        else:
            # Если модель неизвестна, можно попробовать угадать или выдать ошибку
            return 3 # По умолчанию Repka Pi 3 для обратной совместимости
    except FileNotFoundError:
        # Файл не найден, скорее всего старое ядро. Считаем, что это Repka Pi 3.
        return 3


def _load_pin_maps_if_needed(force_reload=False):
    """
    Проверяет, загружены ли карты пинов. Если нет, или если включена
    принудительная перезагрузка, определяет плату и загружает карты.
    Приоритет отдает ручному выбору.
    """
    global BOARD_TO_BCM, BCM_TO_BOARD, PIN_FUNCTIONS, SUNXI_TO_BCM, BCM_TO_SUNXI, PORT_PULL_OFFSET_MAP
    
    # Выходим, только если уже загружено И нет принуждения
    if BOARD_TO_BCM is not None and not force_reload:
        return

    # --- Новая гибридная логика ---
    model_to_load = None
    if _manual_board_model is not None:
        # Если пользователь сделал ручной выбор, используем его
        model_to_load = _manual_board_model
    else:
        # Иначе, запускаем автоматику
        model_to_load = _get_board_model()
    # -----------------------------

    if model_to_load == 4:
        from .boards import pin_maps_rpi4 as maps
    elif model_to_load == 3:
        from .boards import pin_maps_rpi3 as maps
    else:
        raise SetupException('Не удалось определить модель платы или она не поддерживается')

    BOARD_TO_BCM = maps.ALL_MAPS.get('BOARD_TO_BCM')
    BCM_TO_BOARD = maps.ALL_MAPS.get('BCM_TO_BOARD')
    PIN_FUNCTIONS = maps.ALL_MAPS.get('FUNCTIONS')
    SUNXI_TO_BCM = maps.ALL_MAPS.get('SUNXI_TO_BCM')
    BCM_TO_SUNXI = maps.ALL_MAPS.get('BCM_TO_SUNXI')
    PORT_PULL_OFFSET_MAP = maps.ALL_MAPS.get('PORT_PULL_OFFSET_MAP')


def _resolve_channel_to_bcm(channel):
    """
    Преобразует канал в любом режиме в его системный номер (sysfs/bcm),
    используя данные из загруженных карт пинов.
    """
    bcm_channel = None
    if gpio_mode == constants.BOARD:
        # Ищем в словаре BOARD -> BCM
        bcm_channel = BOARD_TO_BCM.get(channel)

    elif gpio_mode == constants.BCM or gpio_mode == constants.SOC:
        # В этих режимах номер канала - это и есть номер sysfs
        bcm_channel = channel

    elif gpio_mode == constants.SUNXI:
        # Ищем в словаре SUNXI -> BCM
        bcm_channel = SUNXI_TO_BCM.get(channel)

    # Финальная проверка
    if bcm_channel is None or not isinstance(bcm_channel, int):
        raise InvalidPinException(f"Не удалось определить системный номер для канала '{channel}' в установленном режиме.")
        
    return bcm_channel

def setboard(model):
    """
    Позволяет принудительно установить модель платы вручную.
    Имеет приоритет над автоматическим определением.
    Нужен для обратной совместимости со старыми скриптами.
    """
    global _manual_board_model
    if model in [constants.REPKAPI3, constants.REPKAPI4]:
        _manual_board_model = model
        # Сразу же загружаем карты, чтобы библиотека была готова к работе
        _load_pin_maps_if_needed(force_reload=True)
    else:
        raise ValueError("Неверная модель платы для setboard")


def setmode(mode):
    """
    Устанавливает режим нумерации пинов
    :param mode: constants.BOARD или constants.BCM
    """
    global gpio_mode
    _load_pin_maps_if_needed() # Загружаем карты перед первой операцией
    if mode in [constants.BOARD, constants.BCM, constants.SUNXI, constants.SOC]:
        gpio_mode = mode
    else:
        raise ValueError("Неверный режим нумерации пинов")


# --- КЛИЕНТ ДЛЯ ДРАЙВЕРА ---
# RepkaPi/GPIO.py

def _set_pull_via_driver(command):
    """Формирует бинарную структуру и отправляет ее драйверу через ioctl."""
    DEVICE_PATH = "/dev/repka_pud" # Имя устройства из нашего C-драйвера
    
    # Определяем универсальную IOCTL команду (должна совпадать с драйвером)
    # В нашем C-коде мы использовали cmd=0 для этой структуры.
    # Но правильнее определить ее через _IOWR.
    # Для простоты пока оставим cmd=0.
    IOCTL_PUD_RMW = 0 
    
    try:
        # Запаковываем наши данные из словаря Python в бинарную C-структуру.
        # Формат '@LII' означает:
        # @ - использовать нативное выравнивание (стандартное)
        # L - Unsigned Long (для addr)
        # I - Unsigned Int (для shift)
        # I - Unsigned Int (для code)
        packed_data = struct.pack('@LII', command['addr'], command['shift'], command['code'])
        
        # Открываем файл устройства, созданный нашим драйвером
        with open(DEVICE_PATH, "w") as fd:
            # Отправляем команду. IOCTL_PUD_RMW - это номер команды (cmd),
            # packed_data - это данные (arg), которые мы передаем.
            fcntl.ioctl(fd, IOCTL_PUD_RMW, packed_data)

    except (OSError, FileNotFoundError):
        # Если драйвер не загружен, нет прав или устройство не создано,
        # просто молча ничего не делаем.
        pass
# ------------------------------------

# --- ФУНКЦИЯ-КАЛЬКУЛЯТОР ДЛЯ PULL-UP/DOWN ---
def _calculate_and_send_pud_command(sysfs_pin, mode):
    """
    Вычисляет параметры для управления регистром подтяжки и отправляет
    команду на драйвер.
    """
    # 1. Загружаем карты, если они еще не загружены
    _load_pin_maps_if_needed()
        
    if BCM_TO_SUNXI is None or PORT_PULL_OFFSET_MAP is None:
        # print("Warning: Pin maps not loaded, cannot set PUD.")
        return
    # 2. Находим имя пина (напр., "PD22") по его sysfs номеру
    sunxi_name = BCM_TO_SUNXI.get(sysfs_pin)
    if not sunxi_name:
        return # Не можем найти пин в карте, ничего не делаем

    # 3. Разбираем имя на порт и номер
    port_name = sunxi_name[:2]
    pin_num_in_port = int(sunxi_name[2:])
    
    # 4. Ищем конфигурацию для этого порта в справочнике
    if 'PORT_PULL_OFFSET_MAP' not in globals() or port_name not in PORT_PULL_OFFSET_MAP:
        return # В конфиге нет информации для этого порта
        
    port_config = PORT_PULL_OFFSET_MAP[port_name]

    # 5. Вычисляем адрес регистра и смещение битов
    reg_offset = port_config['offset']
    # Регистр PUL0 управляет пинами 0-15, PUL1 - пинами 16-31
    if pin_num_in_port >= 16:
        reg_offset += 0x04  # Смещение до регистра PUL1
        pin_num_in_port -= 16
        
    register_addr = port_config['controller'] + reg_offset
    bit_shift = pin_num_in_port * 2
    
    # 6. Определяем код для записи
    pull_code = 0  # Код для PUD_OFF
    if mode == constants.PUD_UP:
        pull_code = 1
    elif mode == constants.PUD_DOWN:
        pull_code = 2
    
    # 7. Формируем финальный приказ для "хирурга"
    command = {
        "addr": register_addr,
        "shift": bit_shift,
        "code": pull_code
    }
    
    # 8. Отправляем приказ
    _set_pull_via_driver(command)
# ---------------------------------------------

def setup(channel, direction, initial=None, pull_up_down=constants.PUD_OFF):
    """
    Устанавливает режим работы канала
    :param channel: Номер канала
    :param direction: constants.IN или constants.OUT
    :param pull_up_down: constants.PUD_UP, constants.PUD_DOWN или constants.PUD_OFF
    :param initial: Начальное значение для выходного канала
    """
    _load_pin_maps_if_needed()

    if gpio_mode is None:
        raise SetupException("Режим нумерации пинов не установлен (setmode)")

    bcm_channel = _resolve_channel_to_bcm(channel)

    if direction not in [constants.IN, constants.OUT]:
        raise InvalidDirectionException()

    if pull_up_down not in [constants.PUD_UP, constants.PUD_DOWN, constants.PUD_OFF]:
        raise InvalidPullException()

    _calculate_and_send_pud_command(bcm_channel, pull_up_down)
    
    # перенаправляем работу 

    sysfs.export(bcm_channel)
    sysfs.direction(bcm_channel, direction)

    gpio_direction[bcm_channel] = direction
    if initial is not None and direction == constants.OUT:
        output(channel, initial)

def cleanup(channel=None):
    """
    Полностью и надежно очищает настройки GPIO, включая события и направления.
    """
    pins_to_clean = []
    if channel is None:
        # Собираем ПОЛНЫЙ список всех пинов, о которых мы можем знать
        event_pins = set(event.get_active_events()) 
        direction_pins = set(gpio_direction.keys())
        pins_to_clean = list(event_pins.union(direction_pins))
    else:
        pins_to_clean = [_resolve_channel_to_bcm(channel)]

    for pin in pins_to_clean:
        # отправляем команду сервису выключить подтяжки
        _calculate_and_send_pud_command(pin, constants.PUD_OFF)
        # Для каждого пина пытаемся убрать событие
        event.remove_edge_detect(pin)
        # И пытаемся убрать экспорт
        if pin in gpio_direction:
            sysfs.unexport(pin)
            del gpio_direction[pin]

def output(channel, value):
    """
    Устанавливает значение на выходном канале
    :param channel: Номер канала
    :param value: constants.HIGH или constants.LOW
    """
    _load_pin_maps_if_needed()
    bcm_channel = _resolve_channel_to_bcm(channel)

    # Строгая проверка: пин должен быть настроен через setup как выход.
    if bcm_channel not in gpio_direction or gpio_direction[bcm_channel] != constants.OUT:
        raise SetupException(f"Канал {channel} ({bcm_channel}) не был настроен как выход. Вызовите GPIO.setup(channel, GPIO.OUT) сначала.")

    sysfs.output(bcm_channel, value)

def input(channel):
    """
    Читает значение с входного канала
    :param channel: Номер канала
    :return: constants.HIGH или constants.LOW
    """
    _load_pin_maps_if_needed()
    bcm_channel = _resolve_channel_to_bcm(channel)

    # Строгая проверка: пин должен быть настроен через setup как вход.
    if bcm_channel not in gpio_direction or gpio_direction[bcm_channel] != constants.IN:
        raise SetupException(f"Канал {channel} ({bcm_channel}) не был настроен как вход. Вызовите GPIO.setup(channel, GPIO.IN) сначала.")

    return sysfs.input(bcm_channel)

def get_function(channel):
    """
    Возвращает функцию пина
    :param channel: Номер канала
    :return: Функция пина (например, constants.OUT, constants.IN, constants.I2C)
    """
    _load_pin_maps_if_needed()

    bcm_channel = _resolve_channel_to_bcm(channel)

    if bcm_channel in PIN_FUNCTIONS:
        return PIN_FUNCTIONS[bcm_channel][0]

    if bcm_channel in gpio_direction:
        return gpio_direction[bcm_channel]

    return constants.UNKNOWN

def get_function_name(channel):
    """
    Возвращает название функции пина
    :param channel: Номер канала
    :return: Название функции пина
    """
    _load_pin_maps_if_needed()

    bcm_channel = _resolve_channel_to_bcm(channel)

    if bcm_channel in PIN_FUNCTIONS:
        return PIN_FUNCTIONS[bcm_channel][1]
    
    return "GPIO"

def get_rpi_info():
    """Возвращает словарь с информацией об определенной плате."""
    _load_pin_maps_if_needed()
    # Загружаем карты, чтобы определить модель и импортировать нужный модуль
    model = _get_board_model()
    if model == 4:
        from .boards import pin_maps_rpi4 as maps
    elif model == 3:
        from .boards import pin_maps_rpi3 as maps
    else:
        return {} # Возвращаем пустоту, если плата не определена
    return maps.INFO

def getboardmodel():
    """
    Возвращает номер определенной модели платы (3 или 4).
    """
    return _get_board_model()

# Инициализация модуля
def add_event_detect(channel, edge, callback=None, bouncetime=0):
    """
    Включает отслеживание события на пине.
    channel: пин в текущем режиме нумерации.
    edge: RISING, FALLING или BOTH.
    """
    bcm_channel = _resolve_channel_to_bcm(channel)
    
    # Строгая проверка: для событий пин тоже должен быть настроен как вход
    if bcm_channel not in gpio_direction or gpio_direction[bcm_channel] != constants.IN:
        raise SetupException(f"Для отслеживания событий канал {channel} ({bcm_channel}) должен быть настроен как вход. Вызовите GPIO.setup(channel, GPIO.IN) сначала.")

    event.add_edge_detect(bcm_channel, edge, callback, bouncetime)

def remove_event_detect(channel):
    """Отключает отслеживание события на пине."""
    _load_pin_maps_if_needed()
    bcm_channel = _resolve_channel_to_bcm(channel)
    event.remove_edge_detect(bcm_channel)

def add_event_callback(channel, callback):
    """Добавляет callback-функцию к уже отслеживаемому событию."""
    _load_pin_maps_if_needed()
    bcm_channel = _resolve_channel_to_bcm(channel)
    event.add_edge_callback(bcm_channel, callback)

def event_detected(channel):
    """Проверяет, произошло ли событие (без callback)."""
    _load_pin_maps_if_needed()
    bcm_channel = _resolve_channel_to_bcm(channel)
    return event.edge_detected(bcm_channel)

def wait_for_edge(channel, edge, timeout=-1):
    """Блокирует выполнение программы до наступления события."""
    _load_pin_maps_if_needed()
    if gpio_mode is None: raise SetupException("Режим нумерации не установлен")
    bcm_channel = _resolve_channel_to_bcm(channel)
    return event.blocking_wait_for_edge(bcm_channel, edge, timeout)

atexit.register(cleanup)

# Витрина 

# Переменная словарь для информации о репке
RPI_INFO = get_rpi_info()

# Явно выставленные константы для API 
BOARD = constants.BOARD
BCM = constants.BCM
SUNXI = constants.SUNXI
SOC = constants.SOC
OUT = constants.OUT
IN = constants.IN
HIGH = constants.HIGH
LOW = constants.LOW
PUD_UP = constants.PUD_UP
PUD_DOWN = constants.PUD_DOWN
PUD_OFF = constants.PUD_OFF
RISING = constants.RISING
FALLING = constants.FALLING
BOTH = constants.BOTH

REPKAPI3 = constants.REPKAPI3
REPKAPI4 = constants.REPKAPI4

VERSION = constants.VERSION

# Ярлыки для "калькулятора" портов
PA = constants.PA
PB = constants.PB
PC = constants.PC
PD = constants.PD
PE = constants.PE
PF = constants.PF
PG = constants.PG
PH = constants.PH
PL = constants.PL
# -------------------------

# "Прогрев" чтобы все константы были доступны после экспорта
_load_pin_maps_if_needed()

