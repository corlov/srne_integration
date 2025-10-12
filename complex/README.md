На текущий момент достигнута автоматизация на уровне helm.

Изначально приложение строилось по микросервисной архитектуре и каждый микросервис запускался как докре-образ.

Затем все запускалось через docker-compose

Далее был переход на k3s и докер образы уже запускались как поды под кубером.

Затем связка с гит-репозиторием и при каждом пуше в него через githubactions и  runner на Репке все обновлялось

Но чтобы не было пробелм с откатами на более страые версии и не раскидывать ямл-файлы повсюду переход на Хелм.






С твоей девлоперской машины (это для тестирвоания хелма когда он еще не включен в конвейр):
    helm install solar-main ./web_app/
    helm uninstall solar-main
    helm upgrade --install solar-main ./web_app/
    helm upgrade solar-main ./web_app/
    
Поскольку self-hosted runner на Raspberry Pi, то потребуется установить helm на нее.            

Протестировать тестовый сервис:
    kubectl port-forward solar-main-test-service-55bb9ccbb-97hhj 8001:8001
    curl http://localhost:8001/version


На девелоперском ноутбуке (pavilion), д.б. установлен Helm и настроен kubeconfig.

helm list
helm history solar-main
helm rollback solar-main 4