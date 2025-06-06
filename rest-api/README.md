Действия  машине разраба:
    sudo docker run --rm -v ${PWD}:/local   openapitools/openapi-generator-cli generate   -i /local/srne_3.0.json   -g python-flask   -o /local/flask_app
    sudo chmod -R 777 flask_app
    sudo chown -R kostya:kostya flask_app
    изменить файлы 
        default_controller.py, 
        requiriments.txt, 
        Dockerfile

    скопировать на репку пи каталог flask_app
    
Действия на Репке:    
        cd flask_app 
        docker build -t openapi_server .
        docker run -d --restart=always --name openapi-service -p 8080:8080 -e REDIS_HOST=192.168.1.193 -e REDIS_PORT=6379 openapi_server:latest
    Для оладки лучше так:
        docker run -p 8080:8080 -e REDIS_HOST=192.168.1.193 -e REDIS_PORT=6379 openapi_server:latest
    
    
docker ps -a    
docker stop 7bb127b3a709
docker rm 7bb127b3a709





GET  (chrome):
    http://192.168.1.163:8080/v1/dynamic_data?deviceId=2
    http://192.168.1.163:8080/v1/settings?deviceId=2
    http://192.168.1.163:8080/v1/system_info?deviceId=2
    http://192.168.1.163:8080/v1/history?deviceId=2&date=2025-05-29
    http://192.168.1.193:8080/v1/command_status?uuid=83bd3ccf-1dd2-42c6-80e8-08f3e8ef2f06

  POST (postman, curl):
    192.168.1.163:8080/v1/control_load_on_off?deviceId=2&on=false
    192.168.1.163:8080/v1/control_load_on_off?deviceId=2&on=false
    192.168.1.163:8080/v1/reset_to_factory_default_settings?deviceId=2
    192.168.1.163:8080/v1/set_load_working_mode?deviceId=2&modeCode=15
    192.168.1.163:8080/v1/set_parameters?deviceId=2&overVoltageThreshold=0&chargingLimitVoltage=0&equalizingChargingVoltage=0&boostChargingVoltage=0&floatingChargingVoltage=0&boostChargingRecovery=0&overDischargeRecovery=0&underVoltageThreshold=0&overDischargeVoltage=0&overDischargeLimitVoltage=0&endOfChargeAndDischargeCapacity=0&overDischargeTimeDelay=0&equalizingChargingTime=0&boostChargingTime=0&equalizingChargingInterval=0&temperatureCompensation=0

