### Сервис работы с контроллером заряда АКБ по протоколу SRNE. 

Непосредсвтенно сама интеграция с контроллером заряда АКБ.

База данных - внешняя, на хосте, Редис также на хотс-машине.


Удаление старого образа (если это необходимо)
        остановить конткейнер
            docker stop e3083d82db1f
        удалить контейнер
            docker rm e3083d82db1f
        удалить образ 
            docker rmi solar-monitor:latest

Сборка (производится строг на Репке Пи либо если на машине с архитектурой отличной от репки (arm64),  нужно при сборке это указывать):
Из минусов - на репке собирается долго образ:

    cd <директория с файло Dockerfile>
    docker build -t solar-monitor .


Если потребуется получить сам tar с докер образом то
    docker save -o <output_file>.tar <image_name>
    docker load -i <input_file>.tar

Прочие команды:
    docker images
    docker rmi -f image_id_or_name
    


Запуск образа с передачей переменных:

    docker rm $(docker ps -a -f status=exited -q)

    docker run -d --restart=always --name solar-monitor-service --device=/dev/ttyS0 \
        -e DEVICE_ID=2 \
        -e DEVICE_SYS_ADDR='/dev/ttyS0' \
        -e DB_HOST=192.168.1.193 \
        -e DB_PORT=5432 \
        -e DB_USER=postgres \
        -e DB_PASSWORD=gen_postgress_password \
        -e DB_NAME=solar_controller_telemetry \
        -e REDIS_HOST=192.168.1.193 \
        -e REDIS_PORT=6379 \
        -e PUBLISH_BROKER_ENABLED=true \
        -e MQTT_SERVER_ADDR=192.168.1.199 \
        -e MQTT_PORT=1883 \
        -e MQTT_USER=srne_user \
        -e MQTT_PASS=qwe123 \
        solar-monitor:latest
        
    или

    docker run -d --restart=always --name solar-monitor-service --device=/dev/ttyS0 \
        -e DEVICE_ID=2 \
        -e DEVICE_SYS_ADDR='/dev/ttyS0' \
        -e DB_HOST=192.168.1.83 \
        -e DB_PORT=5432 \
        -e DB_USER=postgres \
        -e DB_PASSWORD=gen_postgress_password \
        -e DB_NAME=solar_controller_telemetry \
        -e REDIS_HOST=192.168.1.83 \
        -e REDIS_PORT=6379 \
        -e PUBLISH_BROKER_ENABLED=false \
        -e MQTT_SERVER_ADDR=192.168.1.199 \
        -e MQTT_PORT=1883 \
        -e MQTT_USER=srne_user \
        -e MQTT_PASS=qwe123 \
        solar-monitor:latest



Зайти внутрь запущенного образа, нужно знать его id:
    docker exec -it solar-monitor-service /bin/bash

    docker ps -a

    docker stop $(docker ps -a -q)
    docker kill $(docker ps -a -q)
    docker rm $(docker ps -a -f status=exited -q)




