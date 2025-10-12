## Общая архитектура и замечания.
Часть микросервисов (бОльшая) работает из под `k3s` (более легковесный варинат Кубера, специально под arm-одноплатники), другая часть сервисов запускается напрямую из Linux через `systemd` потому что они работают с системой (запуск wifi-точки доступа, сервис источника точного времени). В тоже время есть конфиг и все микросервисы можно запустить через docker-compose.

>При смене GPIO на плате нужно актуализировать это через интерфейс прописав текущие номера портов и затем перезагрузить Репку. После этого присоединить провода к новым пинам с теми номерами что прописали.



### docker-compose
Переименовать docker-compose.yaml.bak -> docker-compose.yaml
  
Запуск микросервисов:
```docker-compose up```
или
```docker-compose up -d```

Останов сервисов:
```docker-compose down```


Иногда при использовании docker сильно заполняется репозиторий неиспользуемыми файлами, чтобы почистить:
```
docker container prune

docker image prune

docker system prune

ls -l /var/snap/docker/common/var-lib-docker/overlay2
```
  


### k3s (основной подход)
Некоторые полезные команды кубера (которые легко забыть и так нужно вспомнить быстро :)


* Запустить деплой (важно при этом в каком каталоге находимся, если в конкретном сервисе, то только он будет перезапущен)

```kubectl apply -f . ```

``kubectl apply -f . -R``

``kubectl apply -f <файл.yaml>``  

* Остановить все:

``kubectl delete -f . -R``

``kubectl delete pods --all``

``kubectl delete services --all``

``kubectl delete ingress --all``  
  
* Просмотр

В режиме снапшота:
``kubectl get pods``
В режиме постоянного обновления состояния:
``kubectl get pods -w``

``kubectl get services``

``kubectl get ingress``
``
  
``kubectl describe pod <pod-name>``


* Поправить "конфиг" на лету;

``kubectl patch service service-api -p '{"spec": {"type": "NodePort"}}'``


* Зайти в Под и посмотреть что там происходит:

имя сервиса взять из get pods
``kubectl exec -it service-srne-adaptor-68f459c6c7-4klcl -- /bin/bash``
Уже внутри можно смотреть логи или что то запускать, например:
``tail -f logs/solar_monitor.log``

  

* Не заходя в Под посмотреть stdout:

М.б. полезно для Flask сервиса
``kubectl logs -f service-api-947887697-kzxxr``

  

* Вызвать изнутри пода какой либо скрипт или команду (например тест на пробу):

``kubectl exec service-gpio-64d56f4df4-ngknd -- python3 health_check.py``

``echo $?``

  

* Рестарт наживую подов после замены докеробраза, например:

узнать какие деплои запущены
``kubectl get deployments``
Затем рестартануть нужный деплой
``kubectl rollout restart deployment service-gpio``

  
  

### HTTPS
Скорее всего обмен данными между фронтом и бекендом будет по https
Поэтому нужно на репке сгенерировать сертификат
``openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365``
добавить его в Кубер
``kubectl create secret tls solar-tls-secret --cert=cert.pem --key=key.pem``
И этот сертификат прописать в ingress.yaml

После этого
Для доступа к интерфейсу с локальной машины (ноута) нужно: 

1. поправить файл /etc/hosts на локальной машине

2. зайти и принять сертификат в браузере руками  https://solar.local


либо запустить бекенд в режиме работы по http (NodePort вместо ClusterIP) и исправить адрес бекенда  в константах фронта с https -> http
  



## Общая схема разворячивания с ноля на Repka Pi

1. Сборка: docker build - собираешь образы под архитектуру Raspberry Pi (это очень важно собрать под АРМ, не под x86 amd и т.д.)

2. Публикация: docker push localhost:5000/... (складываешь образы в локальный Docker Registry).
Либо в централизованый если он имеется.
В идеале опубликовать на какой-то сетевой но наш ресурс образы чтобы на распберях просто быстро скачать оттуда и инсталлировать.

3. Развертывание: kubectl apply -f . -R (Kubernetes скачивает образы с localhost:5000 и запускает поды).

Еще для тех демонов которые запускаются из под systemctl придется установить необходимые пакеты на самой системе.
И также на системе понадобится установить Postgres, Redis и накатить скрипт миграции-создания БД.

 
#### Локальный репозиторий для Кубера

  

Это чтобы локальный репозиторий организовать:

docker run -d -p 5000:5000 --restart=always --name registry registry:2

Это кладем в локальный репозиторий образы:

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

  
  
### Проиче команды

Если нужно запустить по-быстрому какой-то докер образ чтобы пглядеть в нем что лежит и как работает и т.д.

docker run --rm -it --entrypoint /bin/bash localhost:5000/lamp_mode:latest












docker login -u corlovtb



 2143  git status
 2144  git add *
 2145  git status
 2146  git commit -m "test 26 sept v.1.0"
 2147  git push origin main