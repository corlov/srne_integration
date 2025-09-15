# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Портирование и доработка под Repka Pi 4 (c) 2025 Семён Платцев 

import threading
import select
import time

from select import EPOLLIN, EPOLLET, EPOLLPRI

from RepkaPi.constants import NONE, RISING, FALLING, BOTH
from . import sysfs


_threads = {}


class _worker(threading.Thread):

    def __init__(self, pin, trigger, callback=None, bouncetime=0):
        super(_worker, self).__init__()
        self.daemon = True
        self._pin = pin
        self._trigger = trigger
        self._event_detected = False
        self._lock = threading.Lock()
        self._finished = False
        self._bouncetime = bouncetime
        self._lastcall = 0
        self._callbacks = []
        if callback is not None:
            self.add_callback(callback)

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def lastcall(self, lastcall):
        self._lastcall=lastcall

    def event_detected(self):
        with self._lock:
            if self._event_detected:
                self._event_detected = False
                return True
            else:
                return False

    def cancel(self):
        self._finished = True
        self.join()

    def run(self):
        self.exc = None

        try:
            sysfs.edge(self._pin, self._trigger)
            initial_edge = True

            with sysfs.value_descriptor(self._pin) as fd:
                e = select.epoll()
                e.register(fd, EPOLLIN | EPOLLET | EPOLLPRI)
                try:
                    while not self._finished:
                        timenow=time.time_ns()
                        if(self._bouncetime <= 0 or timenow - self._lastcall > self._bouncetime*1000000 or self._lastcall == 0 or self._lastcall > timenow):
                            self.lastcall(timenow)
                            events = e.poll(0.1, maxevents=1)
                            if initial_edge:
                                initial_edge = False
                            elif len(events) > 0:
                                with self._lock:
                                    self._event_detected = True
                                    self.notify_callbacks()

                finally:
                    e.unregister(fd)
                    e.close()

        except BaseException as e:
            self.exc = e

        finally:
            sysfs.edge(self._pin, NONE)

    def join(self):
        super(_worker, self).join()
        if self.exc:
            e = self.exc
            self.exc = None
            raise e

    def notify_callbacks(self):
        for cb in self._callbacks:
            cb(self._pin)


def blocking_wait_for_edge(pin, trigger, timeout=-1):
    assert trigger in [RISING, FALLING, BOTH]

    if pin in _threads:
        raise RuntimeError("Для этого канала GPIO уже существуют конфликтующие события обнаружения границ.")

    try:
        sysfs.edge(pin, trigger)

        finished = False
        initial_edge = True

        with sysfs.value_descriptor(pin) as fd:
            e = select.epoll()
            e.register(fd, EPOLLIN | EPOLLET | EPOLLPRI)
            try:
                while not finished:
                    events = e.poll(timeout / 1000.0, maxevents=1)
                    if initial_edge:
                        initial_edge = False
                    else:
                        finished = True

                n = len(events)
                if n == 0:
                    return None
                else:
                    return pin
            finally:
                e.unregister(fd)
                e.close()

    finally:
        sysfs.edge(pin, NONE)


def edge_detected(pin):
    if pin in _threads:
        return _threads[pin].event_detected()
    else:
        return False


def add_edge_detect(pin, trigger, callback=None, bouncetime=0):
    assert trigger in [RISING, FALLING, BOTH]

    if pin in _threads:
        raise RuntimeError("Обнаружение события уже включено для этого канала GPIO.")

    _threads[pin] = _worker(pin, trigger, callback, bouncetime)
    _threads[pin].start()


def remove_edge_detect(pin):
    if pin in _threads:
        _threads[pin].cancel()
        del _threads[pin]


def add_edge_callback(pin, callback):
    if pin in _threads:
        _threads[pin].add_callback(callback)
    else:
        raise RuntimeError("Добавьте обнаружение событий перед добавлением обратного вызова")


def cleanup(pin=None):
    if pin is None:
        cleanup(list(_threads.keys()))
    elif isinstance(pin, list):
        for p in pin:
            cleanup(p)
    else:
        remove_edge_detect(pin)

def get_active_events():
    """
    Возвращает список пинов, на которых в данный момент отслеживаются события.
    Это публичный метод для получения отчета о работе модуля.
    """
    # Мы возвращаем копию ключей, чтобы быть уверенными,
    # что внешний код не сможет случайно изменить наш внутренний словарь.
    return list(_threads.keys())
