Два варината деплоя: через docker-compose либо через k3s


================================================================================
-= docker-compose =-

docker-compose up

docker-compose up -d

docker-compose down

================================================================================
-= k3s =-

kubectl apply -f .    или       kubectl apply -f . -R

Остановить все:
    kubectl delete -f . -R


kubectl get pods

kubectl get services

kubectl get ingress

kubectl delete pods --all

kubectl delete services --all

delete ingress --all

kubectl describe pod <pod-name>

kubectl get nodes -o wide

Можно по одному подгружать:
    kubectl apply -f <имя-твоего-файла.yaml>

Поправить "конфиг" на лету;
    kubectl patch service service-api -p '{"spec": {"type": "NodePort"}}'


kubectl exec -it service-srne-adaptor-68f459c6c7-4klcl -- /bin/sh
    tail -f logs/solar_monitor.log

================================================================================
1. Сборка: docker build ... (собираешь образы под архитектуру Raspberry Pi).

2. Публикация: docker push localhost:5000/... (складываешь образы в локальный Docker Registry).

3. Развертывание: kubectl apply -f . -R (Kubernetes скачивает образы с localhost:5000 и запускает поды).



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
docker container prune

docker image prune

docker system prune

ls -l /var/snap/docker/common/var-lib-docker/overlay2


