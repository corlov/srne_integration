docker build -t gpio .

docker run -d --restart always --privileged --name gpio-service -v /sys:/sys \
    -e DB_HOST=192.168.1.83 \
    -e DB_PORT=5432 \
    -e DB_USER=postgres \
    -e DB_PASSWORD=gen_postgress_password \
    -e DB_NAME=solar_controller_telemetry \
    -e REDIS_HOST=192.168.1.83 \
    -e REDIS_PORT=6379 \
    gpio:latest

docker exec -it gpio-service /bin/bash


docker logs -f gpio-service


