#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import getpass
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

# --- Константы для нашего драйвера ---
DRIVER_NAME = 'repka_pud_driver'
DRIVER_SOURCE_DIR = 'driver'
DEVICE_NAME_IN_DEV = 'repka_pud' # Имя, с которым он появится в /dev

def run_command(command, check=True):
    """
    Упрощенная и более надежная функция для запуска команд.
    Если команда провалится, скрипт остановится.
    """
    print(f"--- EXEC: {' '.join(command)}")
    try:
        # Используем check=True, чтобы subprocess сам вызвал исключение при ошибке
        subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"!!! ОШИБКА выполнения команды: {' '.join(command)}", file=sys.stderr)
        print(f"!!! Код возврата: {e.returncode}", file=sys.stderr)
        print(f"!!! stderr:\n{e.stderr.decode('utf-8', errors='ignore')}", file=sys.stderr)
        # Критическая ошибка, останавливаем всю установку
        sys.exit(1)
    except FileNotFoundError:
        print(f"!!! ОШИБКА: Команда не найдена - {command[0]}. Убедитесь, что она установлена.", file=sys.stderr)
        sys.exit(1)


# --- Наша главная команда, которая выполняется после стандартной установки ---
class PostInstallCommand(install):
    def run(self):
        # --- ШАГ 0: ПРОВЕРКА ПРАВ ---
        if os.geteuid() != 0:
            print("!!! ОШИБКА: Этот установщик управляет модулями ядра и системными файлами.", file=sys.stderr)
            print("!!! Пожалуйста, запустите его с правами суперпользователя: sudo python3 setup.py install", file=sys.stderr)
            sys.exit(1)

        # Сначала выполняем стандартную установку (копирование Python файлов)
        print("--- Выполнение стандартной установки пакета... ---")
        install.run(self)
        print("--- Стандартная установка завершена. ---")

        # --- ШАГ 1: КОМПИЛЯЦИЯ ДРАЙВЕРА ---
        print("\n--- Компиляция модуля ядра... ---")
        # Используем `make` напрямую. Если он провалится, скрипт остановится.
        run_command(['make', '-C', DRIVER_SOURCE_DIR])

        # --- ШАГ 2: УСТАНОВКА ДРАЙВЕРА В СИСТЕМУ ---
        print("\n--- Установка модуля ядра в систему... ---")
        kernel_version = subprocess.check_output(['uname', '-r']).strip().decode()
        install_dir = f"/lib/modules/{kernel_version}/extra"
        driver_ko_file = f"{DRIVER_SOURCE_DIR}/{DRIVER_NAME}.ko"

        # **ИСПРАВЛЕНИЕ: Создаем каталог, если его не существует**
        print(f"Создание каталога {install_dir} (если необходимо)...")
        os.makedirs(install_dir, exist_ok=True)
        
        # Копируем скомпилированный файл
        print(f"Копирование {driver_ko_file} в {install_dir}...")
        shutil.copy(driver_ko_file, install_dir)

        # Обновляем зависимости модулей
        run_command(['depmod', '-a'])

        # --- ШАГ 3: НАСТРОЙКА АВТОЗАГРУЗКИ И ПРАВ ДОСТУПА ---
        print("\n--- Настройка автозагрузки и прав доступа... ---")
        
        # Автозагрузка при старте системы
        autoload_conf = f"/etc/modules-load.d/{DRIVER_NAME}.conf"
        print(f"Создание файла автозагрузки {autoload_conf}...")
        with open(autoload_conf, "w") as f:
            f.write(DRIVER_NAME)

        # Правило UDEV для прав доступа
        udev_rule = f'KERNEL=="{DEVICE_NAME_IN_DEV}", GROUP="gpio", MODE="0660"'
        udev_file = f"/etc/udev/rules.d/99-{DRIVER_NAME}.rules"
        print(f"Создание файла правил udev {udev_file}...")
        with open(udev_file, "w") as f:
            f.write(udev_rule)

        # Добавляем пользователя в группу 'gpio'
        if not subprocess.run(['getent', 'group', 'gpio'], capture_output=True).stdout:
            print("Создание группы 'gpio'...")
            run_command(['groupadd', 'gpio'])
        
        # Получаем имя пользователя, который запустил sudo
        username = os.getenv('SUDO_USER') or getpass.getuser()
        print(f"Добавление пользователя '{username}' в группу 'gpio'...")
        run_command(['usermod', '-aG', 'gpio', username])

        # --- ШАГ 4: АКТИВАЦИЯ ИЗМЕНЕНИЙ ---
        print("\n--- Применение изменений и запуск драйвера... ---")
        run_command(['udevadm', 'control', '--reload-rules'])
        run_command(['udevadm', 'trigger'])
        
        # Пытаемся загрузить драйвер прямо сейчас
        # Используем check=False, т.к. модуль может быть уже загружен, это не ошибка.
        print(f"Попытка загрузки модуля {DRIVER_NAME}...")
        run_command(['modprobe', DRIVER_NAME], check=False)

        # --- ФИНАЛЬНОЕ СООБЩЕНИЕ ---
        print("\n\n*******************************************************")
        print("  Установка RepkaPi.GPIO и драйвера успешно завершена!")
        print("  Чтобы права доступа для вашего пользователя вступили")
        print("  в силу, РЕКОМЕНДУЕТСЯ ПЕРЕЗАГРУЗИТЬСЯ.")
        print("    sudo reboot")
        print("*******************************************************")


# --- Основная часть setup ---
setup(
    name="RepkaPi.GPIO_SysFS",
    version="0.1.5", # Поднимем версию
    author="@screatorpro & @your_name",
    description=("Библиотека замена RPi.GPIO для Repka Pi с драйвером PUD"),
    long_description=open("README.md").read(),
    license="MIT",
    keywords="Repka Pi RepkaPi gpio",
    url="https://gitflic.ru/project/repka_pi/repkapigpiofs",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    # Используем нашу кастомную команду для установки
    cmdclass={
        'install': PostInstallCommand,
    }
)