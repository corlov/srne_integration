Часть сервисов запускается напрямую из Линукса потому что они работают с системой (запуска вайфай, сервис источника точного времени)
и никаким образом не возможно выполнение из под Куба.

Другая часть для удобства управления и стандартизации запускается в подах под Кубером либо в докер-контейнерах под Докер-компоузом. 
(первый вариант предпочтительнее)

Замечание. Вместо обычного k8s используется более легковесный вараинт k3s.
================================================================================

-= docker-compose =-

docker-compose up

docker-compose up -d

docker-compose down

================================================================================
Иногда сильно заполняется место неиспользуемыми файлами, чтобы почистить:

    docker container prune

    docker image prune

    docker system prune

    ls -l /var/snap/docker/common/var-lib-docker/overlay2

================================================================================
-= k3s =-

Далее некоторые полезные команды кубера (которые легко забыть и так нужно вспомнить быстро :)

Запустить деплой (важно при этом в каком каталоге находимся, если в конкретном сервисе то только он будет перезапущен)
    kubectl apply -f .    или  kubectl apply -f . -R

Можно по одному подгружать:
    kubectl apply -f <имя-твоего-файла.yaml>

Остановить все:
    kubectl delete -f . -R


kubectl get pods
kubectl get services
kubectl get ingress

kubectl delete pods --all
kubectl delete services --all
kubectl  delete ingress --all



kubectl describe pod <pod-name>

kubectl get nodes -o wide



Поправить "конфиг" на лету;
    kubectl patch service service-api -p '{"spec": {"type": "NodePort"}}'


Зайти в Под и посмотреть что там происходит:
    kubectl exec -it service-srne-adaptor-68f459c6c7-4klcl -- /bin/bash
    tail -f logs/solar_monitor.log

Не заходя в Под посмотреть stdout:
    kubectl logs -f service-api-947887697-kzxxr

Вызвать изнутри пода тест на пробу:
    kubectl exec service-gpio-64d56f4df4-ngknd -- python3 health_check.py
    echo $?

Рестарт наживую подов после амены докеробраза:
    kubectl get deployments
    kubectl rollout restart deployment service-gpio

================================================================================
Общая схема разворячивания с ноля на расбери:

1. Сборка: docker build - собираешь образы под архитектуру Raspberry Pi

2. Публикация: docker push localhost:5000/... (складываешь образы в локальный Docker Registry).
В идеале опубликовать на какой-то сетевой но наш ресурс образы чтобы на распберях просто быстро скачать оттуда и инсталлировать.

3. Развертывание: kubectl apply -f . -R (Kubernetes скачивает образы с localhost:5000 и запускает поды).

Еще для тех демонов которые запускаются из под systemctl придется установить необходимые пакеты.

Также понадобится установить Postgres, Redis и накатить скрипт миграции-создания БД.



Локальный репозиторий для Кубера

Это чтобы локальный репозиторий организовать:
docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker tag gpio:latest localhost:5000/gpio:latest
docker push localhost:5000/gpio:latest

docker tag complex_api:latest localhost:5000/complex_api:latest
docker push localhost:5000/complex_api:latest


docker tag lamp_mode:latest localhost:5000/lamp_mode:latest
docker push localhost:5000/lamp_mode:latest
 

docker tag srne_adaptor:latest localhost:5000/srne_adaptor:latest
docker push localhost:5000/srne_adaptor:latest
 

docker tag trafficlight_mode:latest localhost:5000/trafficlight_mode:latest
docker push localhost:5000/trafficlight_mode:latest 
 
 
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml


================================================================================



