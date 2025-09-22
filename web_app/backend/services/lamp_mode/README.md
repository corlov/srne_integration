docker build -t lamp_mode .

Затем, если под кубером:
    docker tag lamp_mode:latest localhost:5000/lamp_mode:latest
    docker push localhost:5000/lamp_mode:latest 
    kubectl rollout restart deployment service-lamp-mode


Если под докером:

    docker run -d --restart always --name lamp-mode-service \
        -e DEVICE_ID=2 \
        -e DB_HOST=192.168.1.83 \
        -e DB_PORT=5432 \
        -e DB_USER=postgres \
        -e DB_PASSWORD=gen_postgress_password \
        -e DB_NAME=solar_controller_telemetry \
        -e REDIS_HOST=192.168.1.83 \
        -e REDIS_PORT=6379 \
        lamp_mode:latest

    docker exec -it lamp-mode-service /bin/bash


    docker logs -f lamp-mode-service







docker run --rm -it --entrypoint /bin/bash localhost:5000/lamp_mode:latest





<none>                              <none>    aeae7e94091a   5 minutes ago    366MB
localhost:5000/traffic_light_mode   <none>    53f8ae39f041   43 minutes ago   366MB
localhost:5000/traffic_light_mode   <none>    e20ea5671103   3 hours ago      366MB
<none>                              <none>    7a5b1258ec1e   3 hours ago      366MB
localhost:5000/complex_api          <none>    92d14315cf39   3 days ago       373MB
lamp_mode                           latest    5297f3a25ced   3 days ago       366MB
localhost:5000/lamp_mode            latest    5297f3a25ced   3 days ago       366MB
gpio                                latest    0b2fea03154e   3 days ago       601MB
localhost:5000/gpio                 <none>    0b2fea03154e   3 days ago       601MB
trafficlight_mode                   latest    8774c7fad6f1   4 days ago       366MB
localhost:5000/trafficlight_mode    latest    8774c7fad6f1   4 days ago       366MB
registry                            2         33eeff39e0aa   24 months ago    25MB



docker rmi aeae7e94091a 53f8ae39f041 e20ea5671103 7a5b1258ec1e 92d14315cf39 5297f3a25ced 5297f3a25ced 0b2fea03154e 0b2fea03154e 8774c7fad6f1 8774c7fad6f1 33eeff39e0aa
