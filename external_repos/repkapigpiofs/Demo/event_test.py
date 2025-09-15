#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Универсальный скрипт для демонстрации прерываний (событий)
# Объединяет add_event_detect, add_event_callback, event_detected, wait_for_edge.

import RepkaPi.GPIO as GPIO
from time import sleep
import sys

# --- 1. Настройка пинов по умолчанию. Их можно будет переопределить. ---
# Используем физическую нумерацию BOARD для простоты
BUTTON_PIN = 15
LED_PIN = 12
# ---------------------------------------------------------------

# --- Функции-обработчики (Callbacks) для демонстрации ---
def simple_callback(channel):
    """Простой обработчик, который просто печатает сообщение."""
    print(f"\n[CALLBACK] Событие на пине {channel} в {time.time():.2f}!")

def toggle_led_callback(channel):
    """Обработчик, который переключает светодиод."""
    print(f"\n[CALLBACK] Переключаю светодиод (событие на пине {channel})...")
    current_state = GPIO.input(LED_PIN)
    GPIO.output(LED_PIN, not current_state)
# ---------------------------------------------------------

def run_menu():
    """Основная функция, которая показывает меню и запускает тесты."""
    
    # --- Настройка GPIO ---
    GPIO.setmode(GPIO.BOARD)
    # Используем внутреннюю стяжку к земле. Кнопка должна быть подключена к 3.3V.
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    print(f"Пины настроены: Кнопка (вход) на BOARD пине {BUTTON_PIN}, Светодиод (выход) на BOARD пине {LED_PIN}.")
    print("---")

    while True:
        print("\n--- Меню тестов событий ---")
        print("1. wait_for_edge (Блокирующее ожидание)")
        print("2. event_detected (Неблокирующая проверка)")
        print("3. Простой Callback (Асинхронная реакция)")
        print("4. Callback с защитой от дребезга (bouncetime)")
        print("0. Выход")
        
        choice = input("Выберите тест: ")

        if choice == '1':
            test_wait_for_edge()
        elif choice == '2':
            test_event_detected()
        elif choice == '3':
            test_simple_callback()
        elif choice == '4':
            test_bouncetime_callback()
        elif choice == '0':
            break
        else:
            print("Неверный выбор.")

def test_wait_for_edge():
    print("\n--- Тест wait_for_edge ---")
    print("Программа 'зависнет' на 10 секунд или до нажатия кнопки...")
    channel = GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING, timeout=10000)
    
    if channel is None:
        print("...Тайм-аут! Кнопка не была нажата.")
    else:
        print(f"...Кнопка на пине {channel} была нажата! Включаю светодиод на 2 секунды.")
        GPIO.output(LED_PIN, GPIO.HIGH)
        sleep(2)
        GPIO.output(LED_PIN, GPIO.LOW)

def test_event_detected():
    print("\n--- Тест event_detected ---")
    print("Нажмите кнопку в течение следующих 5 секунд...")
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)
    
    # Даем пользователю время нажать
    start_time = time.time()
    pressed = False
    while time.time() - start_time < 5:
        if GPIO.event_detected(BUTTON_PIN):
            print("...Событие зафиксировано!")
            pressed = True
            break
        sleep(0.01) # Проверяем каждые 10 мс
        
    if not pressed:
        print("...Кнопка не была нажата за 5 секунд.")
        
    GPIO.remove_event_detect(BUTTON_PIN)

def test_simple_callback():
    print("\n--- Тест простого Callback ---")
    print("Теперь программа будет реагировать на каждое нажатие в течение 10 секунд.")
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=simple_callback)
    
    sleep(10) # Основной поток просто спит, вся магия в callback
    
    print("\n...Тест завершен.")
    GPIO.remove_event_detect(BUTTON_PIN)

def test_bouncetime_callback():
    print("\n--- Тест Callback с bouncetime ---")
    print("Включена защита от дребезга (bouncetime=300ms).")
    print("Попробуйте очень быстро нажать кнопку несколько раз.")
    print("Callback сработает только один раз. Тест длится 10 секунд.")
    
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=toggle_led_callback, bouncetime=300)
    
    sleep(10)
    
    print("\n...Тест завершен.")
    GPIO.remove_event_detect(BUTTON_PIN)

# --- Основная точка входа ---
if __name__ == '__main__':
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\nВыход из программы.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
    finally:
        print("Финальная очистка GPIO...")
        GPIO.cleanup()
