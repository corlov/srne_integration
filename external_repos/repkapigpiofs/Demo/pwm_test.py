#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Интерактивная демонстрация работы с аппаратным ШИМ (PWM)

import RepkaPi.GPIO as GPIO
import sys

# --- Параметры по умолчанию ---
PWM_CHIP = 0
PWM_PIN_IN_CHIP = 0
FREQUENCY_HZ = 100
# -----------------------------

def print_pwm_menu():
    print("\n--- Пульт управления ШИМ ---")
    print("Введите команду:")
    print("  d <0-100>  - изменить скважность (duty cycle), например: d 75")
    print("  f <число>  - изменить частоту (frequency), например: f 500")
    print("  p          - инвертировать полярность (polarity)")
    print("  stop       - остановить ШИM (скважность 0%)")
    print("  start      - запустить ШИМ (с последней скважностью)")
    print("  q          - выход")
    print("----------------------------")

if __name__ == "__main__":
    
    # --- Настройка ШИМ ---
    try:
        print("Инициализация ШИМ...")
        # Создаем объект PWM с начальной скважностью 0%
        pwm = GPIO.PWM_A(PWM_CHIP, PWM_PIN_IN_CHIP, FREQUENCY_HZ, duty_cycle_percent=0)
        print(f"ШИМ на chip={PWM_CHIP}, pin={PWM_PIN_IN_CHIP} готов к работе.")
    except Exception as e:
        print(f"\n!!! ОШИБКА ИНИЦИАЛИЗАЦИИ ШИМ: {e}")
        print("Убедитесь, что ШИМ включен в конфигурации вашей системы (repka-config).")
        sys.exit(1)
        
    # --- Основной цикл ---
    try:
        while True:
            print_pwm_menu()
            user_input = input("> ").strip().lower()
            parts = user_input.split()
            command = parts[0]

            if command == 'd' and len(parts) == 2:
                try:
                    dc = int(parts[1])
                    if 0 <= dc <= 100:
                        pwm.duty_cycle(dc)
                        print(f"Скважность установлена в {dc}%.")
                    else:
                        print("Ошибка: скважность должна быть от 0 до 100.")
                except ValueError:
                    print("Ошибка: введите число после 'd'.")
            
            elif command == 'f' and len(parts) == 2:
                try:
                    freq = int(parts[1])
                    if freq > 0:
                        pwm.change_frequency(freq)
                        print(f"Частота установлена в {freq} Гц.")
                    else:
                        print("Ошибка: частота должна быть больше 0.")
                except ValueError:
                    print("Ошибка: введите число после 'f'.")
            
            elif command == 'p':
                pwm.pwm_polarity()
                print("Полярность инвертирована.")
                
            elif command == 'stop':
                pwm.stop_pwm()
                print("ШИМ остановлен.")
                
            elif command == 'start':
                pwm.start_pwm()
                print("ШИМ запущен.")
            
            elif command == 'q':
                print("Выход из программы...")
                break
            else:
                print("Неизвестная команда.")

    except KeyboardInterrupt:
        print("\nВыход по Ctrl+C.")
    finally:
        print("Очистка ресурсов ШИМ...")
        if 'pwm' in locals():
            pwm.stop_pwm()
            pwm.pwm_close()
