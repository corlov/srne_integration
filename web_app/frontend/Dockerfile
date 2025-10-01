# --- ЭТАП 1: Сборка приложения ---
# Берем официальный образ Node.js 18 на базе легковесного Alpine Linux
FROM node:18-alpine AS builder

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и yarn.lock для установки зависимостей
# Этот шаг кэшируется, если файлы не менялись, что ускоряет сборку
COPY package.json yarn.lock ./

RUN apk add --no-cache python3 make g++

# Устанавливаем зависимости
RUN yarn install --frozen-lockfile --network-timeout 100000

# Копируем все остальные файлы с исходным кодом
COPY . .

# Собираем статические файлы для продакшена
RUN yarn build

# --- ЭТАП 2: Создание финального образа ---
# Берем официальный образ Nginx на базе Alpine Linux
FROM nginx:1.25-alpine

# Копируем только собранные статические файлы из этапа "builder"
# в папку, из которой Nginx раздает контент
COPY --from=builder /app/build /usr/share/nginx/html

# Копируем кастомный конфиг для Nginx (создадим его ниже)
# Это нужно, чтобы React Router работал корректно
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Сообщаем Docker, что контейнер будет слушать порт 80
EXPOSE 80

# Команда для запуска Nginx при старте контейнера
CMD ["nginx", "-g", "daemon off;"]