# Step 1: Build the React app
FROM node:16 AS build

WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
#RUN npm install
RUN yarn add
#RUN yarn add axios
COPY . .
#RUN npm run build
RUN yarn start

# Step 2: Serve the app using a static server
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]