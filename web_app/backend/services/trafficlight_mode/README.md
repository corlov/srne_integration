docker build -t traffic_light_mode .

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


