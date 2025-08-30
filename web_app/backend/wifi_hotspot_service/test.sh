#!/bin/bash

AP_NAME="Hotspot"
CHECK_INTERVAL=30
MAX_ATTEMPTS=3
CONNECT_TIMEOUT=20  # Увеличено время ожидания подключения

# Функция проверки подключения с проверкой IP-адреса
is_connected() {
    # Проверяем наличие IP-адреса и доступность интернета
    if ip -4 addr show wlan0 | grep -q "inet" && ping -c1 -W2 8.8.8.8 >/dev/null; then
        return 0
    else
        return 1
    fi
}

# Функция подключения к сети
scan_and_connect() {
    # Сканируем сети и выводим результат
    nmcli device wifi rescan --refresh 2>/dev/null

    # Получаем список сохраненных сетей (исключая точку доступа)
    saved_networks=$(nmcli -t -f NAME con show | grep -v "^$AP_NAME$")

    for network in $saved_networks; do
        echo "Проверка доступности сети: $network"
        # Ищем SSID среди доступных сетей
        if nmcli -t -g SSID dev wifi list | grep -q "^$network$"; then
            echo "Подключаемся к $network..."
            nmcli con up "$network" >/dev/null 2>&1 &
            sleep $CONNECT_TIMEOUT

            if is_connected; then
                echo "Успешно подключено к $network"
                return 0
            else
                echo "Ошибка подключения к $network"
                nmcli con down "$network" >/dev/null 2>&1
            fi
        fi
    done
    return 1
}

# Основной цикл
attempt=0
while true; do
    if is_connected; then
        echo "Активное подключение: $(nmcli -t -f DEVICE,CONNECTION dev status | grep wlan0 | cut -d: -f2)"
        # Если подключение активно, сбрасываем счетчик и ждем
        attempt=0
        sleep $CHECK_INTERVAL
        continue
    fi

    echo "Нет подключения. Поиск сетей (попытка $((attempt + 1))/$MAX_ATTEMPTS)..."
    if scan_and_connect; then
        attempt=0
        sleep $CHECK_INTERVAL
        continue
    else
        attempt=$((attempt + 1))
    fi

    if [ $attempt -ge $MAX_ATTEMPTS ]; then
        echo "Запуск точки доступа $AP_NAME..."
        nmcli con down "$(nmcli -t -f NAME con show --active | grep -v "^$AP_NAME$")" >/dev/null 2>&1
        nmcli con up "$AP_NAME"
        break  # Выход из цикла после активации AP
    fi

    sleep $CHECK_INTERVAL
done