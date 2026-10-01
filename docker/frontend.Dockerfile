# Build Stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Production Stage with Nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /usr/share/nginx/html

USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
