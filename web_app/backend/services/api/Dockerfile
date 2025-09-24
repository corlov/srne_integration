FROM python:3.10-slim

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5011

CMD ["python3", "complex.py"]