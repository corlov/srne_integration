#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Утилита для вывода полной информации о плате и библиотеке RepkaPi.GPIO

import RepkaPi.GPIO as GPIO
import sys

def print_header(title):
    """Вспомогательная функция для красивого вывода заголовков."""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

if __name__ == "__main__":

    try:
        # --- 1. Информация о библиотеке ---
        print_header("Информация о библиотеке")
        print(f"Версия RepkaPi.GPIO: {GPIO.VERSION}")

        # --- 2. Информация о плате (автоматическое определение) ---
        print_header("Информация об устройстве")
        
        # Функция get_rpi_info() сама запускает всю логику определения
        board_info = GPIO.RPI_INFO 
        
        if not board_info:
            print("Не удалось получить информацию о плате.")
        else:
            print(f"  Тип платы: {board_info.get('TYPE', 'Неизвестно')}")
            print(f"  Производитель: {board_info.get('MANUFACTURER', 'Неизвестно')}")
            print(f"  Процессор: {board_info.get('PROCESSOR', 'Неизвестно')}")
            print(f"  Объем ОЗУ: {board_info.get('RAM', 'Неизвестно')}")
            print(f"  Ревизия P1: {board_info.get('P1_REVISION', 'Неизвестно')}")

        # --- 3. Информация о функциях пинов ---
        print_header("Карта специальных функций пинов (режим BCM)")
        
        # Устанавливаем режим, чтобы загрузить карты
        GPIO.setmode(GPIO.BCM)
        
        # Получаем доступ к словарю FUNCTIONS
        functions_map = GPIO.PIN_FUNCTIONS
        
        if not functions_map:
            print("Не удалось загрузить карту функций пинов.")
        else:
            # Сортируем пины по их BCM номеру для красивого вывода
            for pin_bcm in sorted(functions_map.keys()):
                func_const, func_name = functions_map[pin_bcm]
                print(f"  BCM пин {pin_bcm:<3} -> {func_name}")
                
    except Exception as e:
        print(f"\n!!! Произошла ошибка при получении информации: {e}")
        # Выводим полный traceback для отладки
        import traceback
        traceback.print_exc()

    # cleanup() здесь не нужен, так как мы не меняли состояние пинов,
    # но хорошей практикой будет его все же вызвать.
    finally:
        GPIO.cleanup()
