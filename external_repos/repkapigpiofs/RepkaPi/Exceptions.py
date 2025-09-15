# -*- coding: utf-8 -*-
#
# Copyright (c) 2023-2024 RepkaPi
#
# Этот файл определяет уникальные типы исключений (ошибок) для библиотеки.
# Это позволяет пользователям библиотеки точно обрабатывать конкретные проблемы.

class InvalidPinException(Exception):
    """Ошибка: указан несуществующий пин."""
    pass

class InvalidDirectionException(Exception):
    """Ошибка: указано неверное направление для пина (не IN и не OUT)."""
    pass

class InvalidPullException(Exception):
    """Ошибка: указан неверный режим подтяжки (не UP, DOWN или OFF)."""
    pass

class InvalidChannelException(Exception):
    """Ошибка: указан неверный канал (обобщенная ошибка)."""
    pass

class SetupException(Exception):
    """Ошибка: попытка использовать пин до его настройки (или до выбора платы)."""
    pass

class PermissionException(Exception):
    """Ошибка: недостаточно прав для доступа к sysfs GPIO (запустите с sudo)."""
    pass