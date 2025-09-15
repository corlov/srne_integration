# -*- coding: utf-8 -*-
# Общие константы для библиотеки RepkaPi.GPIO

#Версия библиотеки
VERSION = '0.1.4'

# Нумерация пинов
BOARD = 10
BCM = 11
SUNXI = 12  
SOC = 13   

# Возможности
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

# Состояния
HIGH = 1
LOW = 0

# Направления
OUT = 0
IN = 1

# Специальные функции
SERIAL = 40
SPI = 41
I2C = 42
HARD_PWM = 43
UNKNOWN = -1

# Константы для обработки событий (прерываний)
NONE = 'none'
RISING = 'rising'
FALLING = 'falling'
BOTH = 'both'

# Константы для ручного выбора платы
REPKAPI3 = 3
REPKAPI4 = 4

# Константы для вычисления номеров пинов в режиме SUNXI/SOC ("калькулятор")
PA = 0
PB = 32
PC = 64
PD = 96
PE = 128
PF = 160
PG = 192
PH = 224
# У Allwinner нет PI, PJ, PK
PL = 352
# -------------------------