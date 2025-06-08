# Как сгенерировать по swagger файлу код веб-сервиса?

Вручную написан json-файл (swagger), который нужно передать шгенератор кода в качестве аргумента.

Обычно из того каталога где лежит этот джсон-файл удобнее всего произвести запуск докер-образа передав ему его в качестве параметра.

## Действия машине разраба *(предварительно скачать в виде докер-образа сам генератор кода)*:

    sudo docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/srne_3.0.json -g python-flask -o /local/flask_app
    
    sudo chmod -R 777 flask_app
    
    sudo chown -R kostya:kostya flask_app

Изменить файлы, внеся в них правки как в git

 - default_controller.py
 - requiriments.txt
 - Dockerfile
  
Скопировать на репку пи сгенеренный каталог с кодом сервиса **flask_app**

## Действия на Репке

    cd flask_app
    
    docker build -t openapi_server .
    
    docker run -d --restart=always --name openapi-service -p 8080:8080 -e REDIS_HOST=192.168.1.193 -e REDIS_PORT=6379 openapi_server:latest

Для отладки лучше так:

    docker run -p 8080:8080 -e REDIS_HOST=192.168.1.193 -e REDIS_PORT=6379 openapi_server:latest

Также могут понадобиться, чтобы перезапуска контейнеы по id:

    docker ps -a
    
    docker stop 7bb127b3a709
    
    docker rm 7bb127b3a709

