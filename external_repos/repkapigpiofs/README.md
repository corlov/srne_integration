RepkaPi.GPIO SysFS
========


Подключаемая библиотека замена для [RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/)
для Repka Pi. Реализованы только основные функции работы с GPIO,
используется sysfs: это позволяет получить доступ к контактам GPIO из пользовательского приложения.


Установка
----------
```bash
  sudo apt-get update
  sudo apt-get install python3-dev python3-setuptools git
  git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git
  cd repkapigpiofs
  sudo python3 setup.py install
```


Поддерживаемые модели платы
----------

* Repka Pi 3
* Repka Pi 4



Использование
----------

То же, что и RPi.GPIO, но с новой функцией выбора платы Repka Pi.

```python
    import RepkaPi.GPIO as GPIO

    GPIO.setboard(GPIO.REPKAPI3) # Не обязательно. Позволяет мануально определить плату вписав REPKAPI3 или REPKAPI4.

    GPIO.setmode(GPIO.BOARD)

    GPIO.output(5, 1)
```


Примеры использования в папке Demo

## Статьи по RepkaPi.GPIO
* [Знакомимся с RepkaPi.GPIO SysFS. Установка библиотеки и управление GPIO через Python 3. Теоретические основы работы GPIO портов](https://repka-pi.ru/blog/post/45)
* [Знакомимся с RepkaPi.GPIO SysFS. Разбираем подтягивающие резисторы, прерывания и примеры работы](https://repka-pi.ru/blog/post/61)




Без root-доступа
---------------
Если вы хотите использовать библиотеку как пользователь без полномочий root, вам необходимо сначала настроить правило UDEV, чтобы предоставить вам разрешения.
Это можно сделать следующим образом:

```bash
  $ sudo groupadd gpio
  $ sudo usermod -aG gpio <ваш пользователь>
  $ sudo nano /etc/udev/rules.d/99-gpio.rules
```
Это должно добавить вашего пользователя в группу GPIO, создать новое правило UDEV и открыть его в текстовом редакторе Nano.

Введите следующее в Nano:

```

    KERNEL=="gpio*", MODE:="0660", GROUP:="gpio"
    KERNEL=="pwm*", MODE:="0660", GROUP:="gpio"
    KERNEL=="gpiochip*", MODE:="0660", GROUP:="gpio"
    SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 777 /sys/class/gpio && chown -R root:gpio /sys/class/gpio/* && chmod -R 777 /sys/class/gpio/* && chown -R root:gpio /sys/devices/platform/soc/*.pinctrl/gpio && chmod -R 777 /sys/devices/platform/soc/*.pinctrl/gpio'"
    SUBSYSTEM=="pwm*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/pwm && chmod -R 777 /sys/class/pwm && chown -R root:gpio /sys/class/pwm/* && chmod -R 777 /sys/class/pwm/* && chown -R root:gpio /sys/class/pwm/pwmchip0/* && chmod -R 777 /sys/class/pwm/pwmchip0/* && chown -R root:gpio /sys/devices/platform/soc/*.pwm/pwm && chmod -R 777 /sys/devices/platform/soc/*.pwm/pwm '"
```

Нажмите ``ctrl-x``, ``Y`` и ``ENTER``, чтобы сохранить и закрыть файл.

Перезагрузитесь, и вы можите использовать ``RepkaPi.GPIO`` из под пользователя без полномочий root.


Рекомендации
----------
* https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
* http://linux-sunxi.org/GPIO

Лицензия MIT
---------------------

Copyright (c) 2023 Дмитрий Шевцов (@screatorpro) & Contributors

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения и сопутствующей документации (далее — Программное обеспечение), безвозмездно использовать Программное обеспечение без ограничений, включая неограниченное право на использование, копирование, изменение, слияние, публикацию, распространение, сублицензирование и/или продажу копий Программного обеспечения, а также лицам, которым предоставляется данное Программное обеспечение, при соблюдении следующих условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во все копии или значимые части данного Программного обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ. 
