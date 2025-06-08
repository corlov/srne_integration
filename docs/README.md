## 1. База данных.

Использовать скрипт миграции.

БД разворчивается на хост-машине.

  
  

## 2. Redis

Разворачивается на хост машине.

  
  

## 3. MQTT broker

В него все Репки могут сбрасывать телеметрию и прочую информацию. Размещается в центральной части на серверах.

  
  

## Создание докер-образов производися на самой RepkaPI.

  Это обучловлено тем что архитектура машины разработчика скорее всгео amd64/x86 и т.д., на репке arm64. Можно использовать buildx либо прием с указанием целевой архитекутры, но способ создания образа на самое репке наиболее простой.
  

## 4. Образ сервиса(ов) общения с контроллером SRNE:

На одной Репке может быть подключено несколько контроллеров SRNE. Для каждого должен запуститься свой экземпляр контейнера со своими параметрами.

  

    docker build -t solar-monitor .

  

Запуск: 

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

  

Чтобы зайти на сам работающий конетйнер (чтобы поглядеть логи и т.д.) можно так:

  

    docker exec -it solar-monitor-service /bin/bash
    
      
      
      

  
  

Контейнеры:

    docker ps -a
    
    docker stop 7bb127b3a709
    
    docker kill 7bb127b3a709
    
    docker rm 7bb127b3a709



Образы:

    docker images

удаление образа

    docker rmi -f <image>
