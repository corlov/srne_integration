# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Портирование и доработка под Repka Pi 4 (c) 2025 Семён Платцев 

from contextlib import contextmanager
from .constants import HIGH, LOW, IN, OUT, NONE, RISING, FALLING, BOTH
import os
import time

WAIT_PERMISSION_TIMEOUT = 1.0

def await_permissions(path):
    start_time = time.time()
    def timed_out():
        return time.time() - start_time >= WAIT_PERMISSION_TIMEOUT
    while not os.access(path, os.W_OK) and not timed_out():
        time.sleep(0.01)

@contextmanager
def value_descriptor(pin, mode="r"):
    path = f"/sys/class/gpio/gpio{pin}/value"
    await_permissions(path)
    with open(path, mode) as fp:
        yield fp.fileno()

def export(pin):
    gpio_path = f"/sys/class/gpio/gpio{pin}"
    if os.path.exists(gpio_path):
        return
    
    path = "/sys/class/gpio/export"
    try:
        with open(path, "w") as fp:
            fp.write(str(pin))
    except OSError as e:
        if e.errno == 16: # Device or resource busy
            return
        else:
            raise e
            
    start_time = time.time()
    while not os.path.exists(gpio_path) and not (time.time() - start_time >= WAIT_PERMISSION_TIMEOUT):
        time.sleep(0.02)

def unexport(pin):
    gpio_path = f"/sys/class/gpio/gpio{pin}"
    if not os.path.exists(gpio_path):
        return

    path = "/sys/class/gpio/unexport"
    with open(path, "w") as fp:
        fp.write(str(pin))

def direction(pin, dir):
    assert dir in [IN, OUT]
    path = f"/sys/class/gpio/gpio{pin}/direction"
    await_permissions(path)
    target_dir_str = "in" if dir == IN else "out"
    with open(path, "w") as fp:
        fp.write(target_dir_str)

def input(pin):
    path = f"/sys/class/gpio/gpio{pin}/value"
    with open(path, "r") as fp:
        value = fp.read().strip()
        return HIGH if value == '1' else LOW

def output(pin, value):
    path = f"/sys/class/gpio/gpio{pin}/value"
    str_value = "1" if value else "0"
    with open(path, "w") as fp:
        fp.write(str_value)

def edge(pin, trigger):
    assert trigger in [NONE, RISING, FALLING, BOTH]
    path = f"/sys/class/gpio/gpio{pin}/edge"
    await_permissions(path)
    opts = {NONE: "none", RISING: "rising", FALLING: "falling", BOTH: "both"}
    with open(path, "w") as fp:
        fp.write(opts[trigger])

# Hardware PWM functionality:
#   resources: https://developer.toradex.com/knowledge-base/pwm-linux    &    https://www.faschingbauer.me/trainings/material/soup/hardware/pwm/topic.html


def PWM_Export(chip, pin):  # some chips will have more than 1 pwm chip. the RepkaPi 3 only has 1 called pwmchip0. To list what chips are available use 'ls -l /sys/class/pwm'
    path = "/sys/class/pwm/pwmchip{0}/export".format(chip)
    await_permissions(path)
    with open(path, "w") as fp:
        fp.write(str(pin))


def PWM_Unexport(chip, pin):
    path = "/sys/class/pwm/pwmchip{0}/unexport".format(chip)
    await_permissions(path)
    with open(path, "w") as fp:
        fp.write(str(pin))


def PWM_Enable(chip, pin):  # enables PWM so that it can be controlled
    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/enable".format(chip, pin)
    await_permissions(path)
    with open(path, "w") as fp:
        fp.write(str(1))


def PWM_Disable(chip, pin):  # disables PWM
    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/enable".format(chip, pin)
    await_permissions(path)
    with open(path, "w") as fp:
        fp.write(str(0))


def PWM_Polarity(chip, pin, invert=False):  # inverts the pwm signal. i.e rather than a higher duty cycle being brighter it becomes dimmer. Import to add as sometimes inverted is the defualt
    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/polarity".format(chip, pin)  # important! pwm must be disables before inverting or it wont work
    await_permissions(path)
    if invert is True:
        with open(path, "w") as fp:
            fp.write(str("inversed"))
    else:
        with open(path, "w") as fp:
            fp.write(str("normal"))


def PWM_Period(chip, pin, pwm_period):  # in nanoseconds
    duty_cycle_path = "/sys/class/pwm/pwmchip{0}/pwm{1}/duty_cycle".format(chip, pin)
    with open(duty_cycle_path, "r") as fp:  # read the current period to compare. this is necessary as the duty cycle has to be less than the period.
        current_duty_cycle_period = int(fp.read())
        fp.close()
    if (current_duty_cycle_period > pwm_period):
        print("Error the new duty cycle period must be less than or equal to the PWM Period: ", pwm_period)
        print("New Duty Cyce = ", current_duty_cycle_period, " Current PWM Period = ", pwm_period)
        os.error

    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/period".format(chip, pin)
    await_permissions(path)
    with open(path, "w") as fp:  # pretty sure this
        fp.write(str(pwm_period))


def PWM_Frequency(chip, pin, pwm_frequency):  # in Hz
    pwm_period = (1 / pwm_frequency) * 1e9  # convert freq to time in nanoseconds
    pwm_period = int(round(pwm_period, 0))
    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/period".format(chip, pin)
    await_permissions(path)
    with open(path, "w") as fp:  # pretty sure this
        fp.write(str(pwm_period))


def PWM_Duty_Cycle_Percent(chip, pin, Duty_cycle):  # in percentage
    PWM_period_path = "/sys/class/pwm/pwmchip{0}/pwm{1}/period".format(chip, pin)
    with open(PWM_period_path, "r") as fp:  # read the current period to compare. this is necessary as the duty cycle has to be less than the period.
        current_period = int(fp.read())
        fp.close()
    new_duty_cycle = int(round(Duty_cycle / 100 * current_period, 0))

    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/duty_cycle".format(chip, pin)
    with open(path, "w") as fp:  # pretty sure this
        fp.write(str(new_duty_cycle))


def PWM_Duty_Cycle(chip, pin, Duty_cycle):  # in nanoseconds
    PWM_period_path = "/sys/class/pwm/pwmchip{0}/pwm{1}/period".format(chip, pin)
    with open(PWM_period_path, "r") as fp:  # read the current period to compare. this is necessary as the duty cycle has to be less than the period.
        current_period = int(fp.read())
        fp.close()
    if (Duty_cycle > current_period):
        print("Error the new duty cycle period must be less than or equal to the PWM Period: ", current_period)
        print("New Duty Cyce = ", Duty_cycle, " Current PWM Period = ", current_period)
        os.error
    path = "/sys/class/pwm/pwmchip{0}/pwm{1}/duty_cycle".format(chip, pin)
    with open(path, "w") as fp:  # pretty sure this
        fp.write(str(Duty_cycle))
