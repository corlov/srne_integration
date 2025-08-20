import time
import RepkaPi.GPIO as GPIO
import redis
import os

# Задача этого модуля все состояния по гпио в редис поместить

# https://repka-pi.ru/blog/post/45
# sudo apt-get install python3-dev python3-setuptools git
# git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git
# cd repkapigpiofs
# sudo python3 setup.py install

# print(GPIO.getboardmodel(), GPIO.VERSION, GPIO.RPI_INFO)

PIN_OUT_K2_TRAFFICLIGHT = 11
PIN_OUT_K3_LAMP = 13
PIN_OUT_K4_MODEM = 15
PIN_IN_WIFI_BUTTON = 16
PIN_IN_CABINET_OPEN_DOOR_BUTTON = 18

PinsOut = [PIN_OUT_K2_TRAFFICLIGHT, PIN_OUT_K3_LAMP, PIN_OUT_K4_MODEM]
PinsIn = [PIN_IN_WIFI_BUTTON, PIN_IN_CABINET_OPEN_DOOR_BUTTON]


def init_pins():
    GPIO.setmode(GPIO.BOARD)

    for pin in PinsOut:
        GPIO.setup(pin, GPIO.OUT)

    for pin in PinsIn:
        # GPIO.PUD_UP = state (HIGH) when the button is not pressed
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def main():
    init_pins()

    REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    try:
        while True:
            # Small delay to debounce
            time.sleep(1)

            r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

            # обновляем значения в редисе по входным пинам
            for pin in PinsIn:
                redis_pin_name = f'GPIO.{pin}'
                state = GPIO.input(pin)
                if state == GPIO.LOW:
                    r.set(redis_pin_name, 0)
                else:
                    r.set(redis_pin_name, 1)

            # в зависмости от того что установлено в Редисе отправляем на устройство соотв. сигнал
            for pin in PinsOut:
                redis_pin_name = f'GPIO.{pin}'
                if r.exists(redis_pin_name):
                    state = r.get(f'GPIO.{pin}')
                    if state:
                        GPIO.output(pin, GPIO.HIGH)
                    else:
                        GPIO.output(pin, GPIO.LOW)
    finally:
        GPIO.cleanup()

main()
