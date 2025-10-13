# Stage 1: Build assets
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Inline nginx config (no external file required)
RUN printf '%s\n'       'server {'       '  listen 80;'       '  server_name _;'       '  root /usr/share/nginx/html;'       '  index index.html;'       '  location /api/ {'       '    proxy_pass http://backend:8000/api/;'       '    proxy_set_header Host $host;'       '    proxy_set_header X-Real-IP $remote_addr;'       '    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;'       '    proxy_set_header X-Forwarded-Proto $scheme;'       '  }'       '  location / {'       '    try_files $uri /index.html;'       '  }'       '}' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
