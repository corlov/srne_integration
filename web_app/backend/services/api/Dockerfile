# FROM python:3.10-slim

# ARG APP_VERSION
# ENV APP_VERSION=${APP_VERSION}

# WORKDIR /app

# COPY . .

# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
    
# RUN pip3 install --no-cache-dir -r requirements.txt

# EXPOSE 5011

# CMD ["python3", "complex.py"]


FROM python:3.10-slim

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Копируем ТОЛЬКО файл с зависимостями
COPY requirements.txt .

# 2. Устанавливаем системные зависимости (если они нужны для pip)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# 3. Устанавливаем Python-зависимости. Этот слой будет переиспользоваться, пока requirements.txt не изменится
RUN pip3 install --no-cache-dir -r requirements.txt

# 4. И только теперь копируем ВЕСЬ остальной код
COPY . .

EXPOSE 5011

CMD ["python3", "complex.py"]