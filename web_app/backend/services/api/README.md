### АПИ через которое общается фронт и внешние системы с нашей

  

***<ИМЯ_ОБРАЗА>=complex_api***


**Локально собрать образ**

> docker build -t <ИМЯ_ОБРАЗА> .



**Затем, если под k3s:**

> docker tag <ИМЯ_ОБРАЗА>:latest localhost:5000/<ИМЯ_ОБРАЗА>:latest

> docker push localhost:5000/<ИМЯ_ОБРАЗА>:latest

> kubectl rollout restart deployment service-<ИМЯ_ОБРАЗА>

или

> kubectl apply -f . -R

  

Если под докером хотим запустить:

docker run -d --restart always --name complex-api-service -p 5011:5011 \
    -e DB_HOST=192.168.1.83 \
    -e DB_PORT=5432 \
    -e DB_USER=postgres \
    -e DB_PASSWORD=gen_postgress_password \
    -e DB_NAME=solar_controller_telemetry \
    -e REDIS_HOST=192.168.1.83 \
    -e REDIS_PORT=6379 \
    -e SECRET_KEY=uw3cok92adxmzpf35_secret_key_value_12082025 \
    -e EXP_LIMIT=600 \
    -e SSE_UPDATE_GPIO_TIMEOUT=5 \
    -e SSE_UPDATE_DYNAMIC_DATA_TIMEOUT=10 \
    -e SSE_UPDATE_COMPLEX_STATUS_TIMEOUT=3 \
    complex_api:latest

docker exec -it complex-api-service /bin/bash

docker logs -f complex-api-service

docker stop complex-api-service

docker rm complex-api-service
