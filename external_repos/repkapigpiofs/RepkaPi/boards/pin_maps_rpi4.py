# -*- coding: utf-8 -*-
# Портирование и доработка под Repka Pi 4 (c) 2025 Семён Платцев 
# Распиновка для Repka Pi 4.


from .. import constants

# Словарь преобразования нумерации BOARD в BCM (SYSFS номера из схемы)
BOARD_TO_BCM = {
    # Левая сторона гребенки
    3: 122,     # PD26 (I2C1_SDA)
    5: 121,     # PD25 (I2C1_SCL)
    7: 362,     # PL10
    11: 111,    # PD15
    13: 112,    # PD16
    15: 113,    # PD17
    19: 229,    # PH5 (SPI0_MOSI)
    21: 230,    # PH6 (SPI0_MISO)
    23: 228,    # PH4 (SPI0_CLK)
    27: 120,    # PD24 (I2C2_SDA)
    29: 356,    # PL4
    31: 357,    # PL5
    33: 118,    # PD22 (В схеме дублирование, пин 11 и 33 - это один и тот же PG11)
    35: 202,    # PG10 (I2S_LRCK)
    37: 358,    # PL6 (I2S_ADC)

    # Правая сторона гребенки
    8: 224,     # PH0 (UART0_TX)
    10: 225,    # PH1 (UART0_RX)
    12: 203,    # PG11
    16: 354,    # PL2
    18: 355,    # PL3
    22: 359,    # PL7
    24: 227,    # PH3 (SPI0_CS0)
    26: 226,    # PH2 (SPI0_CS1)
    28: 119,    # PD23 (I2C2_SCL)
    32: 360,    # PL8 (PWM0)
    36: 231,    # PH7 (В схеме дублирование, пин 23 и 36 - это один и тот же PH7)
    38: 205,    # PG13 (I2S_MCLK)
    40: 204     # PG12 (PCM5102, в схеме Repka-Pi4 на 40м пине PG12, а не 204)
                # Оставляю 204, как указано в колонке SYSFS, но с комментарием.
}

SUNXI_TO_BCM = {
    # Имена с левой стороны гребенки
    "PD26": 122, "PD25": 121, "PL10": 362, "PD15": 111, "PD16": 112,
    "PD17": 113, "PH5": 229, "PH6": 230, "PH4": 228, "PD24": 120,
    "PL4": 356, "PL5": 357, "PD22": 118, "PG10": 202, "PL6": 358,

    # Имена с правой стороны гребенки
    "PH0": 224, "PH1": 225, "PG11": 203, "PL2": 354, "PL3": 355,
    "PL7": 359, "PH3": 227, "PH2": 226, "PD23": 119, "PL8": 360,
    "PH7": 231, "PG13": 205, "PG12": 204
}

# BCM_TO_BOARD генерируется автоматически, здесь все в порядке
BCM_TO_BOARD = {v: k for k, v in BOARD_TO_BCM.items()}

# Словарь, содержащий особые функции GPIO, ключи - SYSFS номера
FUNCTIONS = {
    # I2C1
    122: [constants.I2C, "I2C1_SDA"],
    121: [constants.I2C, "I2C1_SDL"],
    # UART0
    224: [constants.SERIAL, "UART0_TX"],
    225: [constants.SERIAL, "UART0_RX"],
    # SPI0
    229: [constants.SPI, "SPI0_MOSI"],
    230: [constants.SPI, "SPI0_MISO"],
    231: [constants.SPI, "SPI0_CLK"],
    227: [constants.SPI, "SPI0_CS0"],
    226: [constants.SPI, "SPI0_CS1"],
    # I2C2
    120: [constants.I2C, "I2C2_SDA"],
    119: [constants.I2C, "I2C2_SCL"],
    # PWM0
    118: [constants.HARD_PWM, "PWM0"],
}

INFO = {'P1_REVISION': 4, 'TYPE': 'Repka Pi 4', 'MANUFACTURER': 'NGO "RainbovSoft",NGO "Intellect"', 'RAM': '4096M', 'PROCESSOR': 'Allwinner H6'}

# --- РАЗДЕЛ ДЛЯ УПРАВЛЕНИЯ ПОДТЯЖКОЙ ---

# Базовые адреса контроллеров для Repka Pi 4 (Allwinner H6),

MAIN_PIO_BASE = 0x0300B000  # Для портов PC, PD, PF, PG, PH
SECOND_PIO_BASE = 0x07022000 # Для портов PL, PM

# Обратная карта для поиска имени пина по его sysfs номеру
BCM_TO_SUNXI = {v: k for k, v in SUNXI_TO_BCM.items()}

# Карта смещений регистров PULL0 для каждого порта,
# который физически выведен на 40-пиновую гребенку.

PORT_PULL_OFFSET_MAP = {
    # Порты на главном контроллере (0x0300B000)
    'PC': {'controller': MAIN_PIO_BASE, 'offset': 0x64}, # n=2
    'PD': {'controller': MAIN_PIO_BASE, 'offset': 0x88}, # n=3
    'PG': {'controller': MAIN_PIO_BASE, 'offset': 0xF4}, # n=6
    'PH': {'controller': MAIN_PIO_BASE, 'offset': 0x118},# n=7
    
    # Порты на "втором" контроллере (0x07022000)
    'PL': {'controller': SECOND_PIO_BASE, 'offset': 0x1C} # n=0
    
    # Порты PA, PB, PE, PF, PM не добавляем, так как их нет на гребенке,
    # и пользователь не сможет к ним обратиться.
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