Программная часть ПО работающего на Репке состоит из:
    1) докер-образа микросервиса сопряжения с контроллером SRNE (если несколько контроллеров, то нескоко образов с разными параметрами)
    2) докер образа микро веб-сервиса (один на все устройства)
    3) база данных (скрипт миграции), БД устанавливается на хост-машину
    4) редис - для обмена между микроервисами
    5) брокер MQTT в центре принимает всю телеметрию (опционально, чтобы не дергать Репку по ресту)
    
БОльшая часть кода веб-сервиса сгенерирована автоматически по сваггер-файлу, который составлялся в редакторе VS Code.
Имплементации методов дописаны вручную.


Изначально интеграция с контроллером делалась через Ардуино, весь код в соотв. каталоге.

Затем на базе GPIO и Max3232 и Репки Пи.

При этом в случае переключения распиновки Репки нужно запускать докер-образы с соотв. параметрами сериал-портов и их нумераций.






