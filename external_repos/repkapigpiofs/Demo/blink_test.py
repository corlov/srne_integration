#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Универсальный скрипт для демонстрации управления GPIO
# Принимает режим нумерации и пин в качестве аргументов командной строки.

import RepkaPi.GPIO as GPIO
from time import sleep
import sys

# --- 1. Определяем словари для удобства ---
# Словарь для сопоставления строковых аргументов с константами библиотеки
MODES = {
    "BOARD": GPIO.BOARD,
    "BCM": GPIO.BCM,
    "SOC": GPIO.SOC,
    "SUNXI": GPIO.SUNXI
}

# --- 2. Функция для вывода помощи ---
def print_usage():
    print("\nОшибка: Неверные аргументы.")
    print("Использование: python3 blink_unified.py <РЕЖИМ> <ПИН>")
    print("\nПримеры:")
    print("  python3 blink_unified.py BOARD 7")
    print("  python3 blink_unified.py BCM 118")
    print("  python3 blink_unified.py SUNXI PL10")
    print("  python3 blink_unified.py SOC \"GPIO.PL+10\"")
    print("\nДоступные режимы:", ", ".join(MODES.keys()))
    sys.exit(1) # Выходим с кодом ошибки

# --- 3. Проверка и обработка аргументов командной строки ---
if len(sys.argv) != 3:
    print_usage()

# Берем аргументы
mode_str = sys.argv[1].upper()
pin_str = sys.argv[2]

# Проверяем, правильный ли режим
if mode_str not in MODES:
    print(f"\nОшибка: Неизвестный режим '{sys.argv[1]}'.")
    print_usage()

# --- 4. Основная логика программы ---
try:
    # Устанавливаем режим нумерации
    selected_mode = MODES[mode_str]
    GPIO.setmode(selected_mode)
    
    # Преобразуем пин в нужный формат
    # Для SUNXI это строка, для остальных - пытаемся превратить в число
    if selected_mode == GPIO.SUNXI:
        led_pin = pin_str
    elif selected_mode == GPIO.SOC:
        # Для SOC выполняем Python-выражение, это "хак", но для демо подойдет
        try:
            led_pin = eval(pin_str.replace("GPIO.", "GPIO."))
        except:
            print(f"\nОшибка: Не удалось вычислить выражение для пина '{pin_str}'")
            print_usage()
    else: # BOARD и BCM
        try:
            led_pin = int(pin_str)
        except ValueError:
            print(f"\nОшибка: Для режима {mode_str} пин должен быть числом.")
            print_usage()

    print(f"Настройка пина '{pin_str}' в режиме '{mode_str}'...")
    GPIO.setup(led_pin, GPIO.OUT)

    print ("Светодиод мигает. Нажмите CTRL+C для завершения.")
    while True:
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(0.5)

except KeyboardInterrupt:
    print ("\nЗавершение работы.")
except Exception as e:
    print(f"\nПроизошла ошибка во время выполнения: {e}")
finally:
    print("Очистка GPIO...")
    GPIO.cleanup()
