# web_app/backend/services/test_service/Dockerfile

# Используем самый маленький базовый образ Python
FROM python:3.10-alpine

# Получаем версию из аргумента сборки
ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app
COPY test_app.py .

# Запускаем приложение
CMD ["python", "-u", "test_app.py"]