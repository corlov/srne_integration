### Режим работ светофора

*** ВАЖНО: осторожнее м.б. путаница в названии имен через - или _ ***

***<ИМЯ_ОБРАЗА>=traffic_light_mode***


**Локально собрать образ**

> docker build -t <ИМЯ_ОБРАЗА> .



**Затем, если под k3s:**

> docker tag <ИМЯ_ОБРАЗА>:latest localhost:5000/<ИМЯ_ОБРАЗА>:latest

> docker push localhost:5000/<ИМЯ_ОБРАЗА>:latest

> kubectl rollout restart deployment service-<ИМЯ_ОБРАЗА>

или

> kubectl apply -f . -R

  

Если под докером хотим запустить:


    docker run -d --restart always --name traf-ligth-mode-service \
        -e DEVICE_ID=2 \
        -e DB_HOST=192.168.1.83 \
        -e DB_PORT=5432 \
        -e DB_USER=postgres \
        -e DB_PASSWORD=gen_postgress_password \
        -e DB_NAME=solar_controller_telemetry \
        -e REDIS_HOST=192.168.1.83 \
        -e REDIS_PORT=6379 \
        traffic_light_mode:latest

    docker exec -it traf-ligth-mode-service /bin/bash


    docker logs -f traf-ligth-mode-service

    docker stop traf-ligth-mode-service

    docker rm traf-ligth-mode-service


