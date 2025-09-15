# -*- coding: utf-8 -*-
# Портирование и доработка под Repka Pi 4 (c) 2025 Семён Платцев 
# Распиновка для Repka Pi 3 (ver 1.3 - 1.6)

from .. import constants

# Словарь преобразования нумерации BOARD в BCM (SYSFS номера из схемы)
BOARD_TO_BCM = {
    # Левая сторона гребенки
    3: 12,      # PA12
    5: 11,      # PA11
    7: 7,       # PA7
    11: 8,      # PA8
    13: 9,      # PA9
    15: 10,     # PA10
    19: 64,     # PC0 (SPI0_MOSI)
    21: 65,     # PC1 (SPI0_MISO)
    23: 66,     # PC2 (SPI0_CLK)
    27: 19,     # PA19 (I2C2_SDA)
    29: 0,      # PA0
    31: 1,      # PA1
    33: 362,    # PL10 (PWM0)
    35: 16,     # PA16
    37: 21,     # PA21

    # Правая сторона гребенки
    8: 4,       # PA4 (UART0_TX)
    10: 5,      # PA5 (UART0_RX)
    12: 6,      # PA6
    16: 354,    # PL2 (S_UART_TX)
    18: 355,    # PL3 (S_UART_RX)
    22: 2,      # PA2
    24: 67,     # PC3 (SPI0_CS0)
    26: 3,      # PA3
    28: 18,     # PA18 (I2C2_SCL)
    32: 363,    # PL11
    36: 13,     # PA13
    38: 15,     # PA15
    40: 14,     # PA14
}

SUNXI_TO_BCM = {
    # Имена с левой стороны гребенки
    "PA12": 12, "PA11": 11, "PA7": 7, "PA8": 8, "PA9": 9, "PA10": 10,
    "PC0": 64, "PC1": 65, "PC2": 66, "PA19": 19, "PA0": 0, "PA1": 1,
    "PL10": 362, "PA16": 16, "PA21": 21,

    # Имена с правой стороны гребенки
    "PA4": 4, "PA5": 5, "PA6": 6, "PL2": 354, "PL3": 355, "PA2": 2,
    "PC3": 67, "PA3": 3, "PA18": 18, "PL11": 363, "PA13": 13, "PA15": 15,
    "PA14": 14
}

# Словарь преобразования нумерации BCM в BOARD

BCM_TO_BOARD = {v: k for k, v in BOARD_TO_BCM.items()}

# Словарь, содержащий особые функции GPIO, ключи - SYSFS номера
FUNCTIONS = {
    # I2C1
    12: [constants.I2C, "I2C1-SDA"],
    11: [constants.I2C, "I2C1-SCL"],
    # UART0
    4:  [constants.SERIAL, "UART0-TX"],
    5:  [constants.SERIAL, "UART0-RX"],
    # S_UART
    354: [constants.SERIAL, "S_UART_TX"],
    355: [constants.SERIAL, "S_UART_RX"],
    # SPI0
    64: [constants.SPI, "SPI0_MOSI"],
    65: [constants.SPI, "SPI0_MISO"],
    66: [constants.SPI, "SPI0_CLK"],
    67: [constants.SPI, "SPI0_CS0"],
    # I2C2
    19: [constants.I2C, "I2C2_SDA"],
    18: [constants.I2C, "I2C2_SCL"],
    # PWM0
    362: [constants.HARD_PWM, "PWM0"]
}

INFO = {'P1_REVISION': 3, 'TYPE': 'Repka Pi 3', 'MANUFACTURER': 'NGO "RainbovSoft",NGO "Intellect"', 'RAM': '1024M', 'PROCESSOR': 'Allwinner H5'}

# --- РАЗДЕЛ ДЛЯ УПРАВЛЕНИЯ ПОДТЯЖКОЙ ---

# Базовые адреса контроллеров для Repka Pi 3 (Allwinner H5).

MAIN_PIO_BASE = 0x01C20800  # Для портов PA, PC и других
PL_PIO_BASE   = 0x01F02C00  # Отдельный контроллер для порта PL

# Обратная карта для поиска имени пина по его sysfs номеру
BCM_TO_SUNXI = {v: k for k, v in SUNXI_TO_BCM.items()}

# Карта смещений регистров PULL0 для каждого порта,
# который физически выведен на 40-пиновую гребенку Repka Pi 3.
PORT_PULL_OFFSET_MAP = {
    # Порты на главном контроллере (0x01C20800)
    'PA': {'controller': MAIN_PIO_BASE, 'offset': 0x1C},
    'PC': {'controller': MAIN_PIO_BASE, 'offset': 0x64},
    
    # Порт на "втором" контроллере (0x01F02C00)
    'PL': {'controller': PL_PIO_BASE, 'offset': 0x1C}
}

# Общий словарь, который будет импортироваться
ALL_MAPS = {
    'BOARD_TO_BCM': BOARD_TO_BCM,
    'BCM_TO_BOARD': BCM_TO_BOARD,
    'FUNCTIONS': FUNCTIONS,
    'SUNXI_TO_BCM': SUNXI_TO_BCM,
    'INFO': INFO,
    'BCM_TO_SUNXI': BCM_TO_SUNXI,
    'PORT_PULL_OFFSET_MAP': PORT_PULL_OFFSET_MAP
}