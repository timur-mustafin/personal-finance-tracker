FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN mkdir -p /var/www/static /var/www/media \
 && cat >/etc/nginx/conf.d/default.conf <<'NGINXCONF'
server {
  listen 80;
  server_name _;

  add_header X-Content-Type-Options nosniff;
  add_header X-Frame-Options DENY;
  add_header X-XSS-Protection "1; mode=block";
  add_header Referrer-Policy strict-origin-when-cross-origin;
  add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https: http:; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https:;" always;

  root /usr/share/nginx/html;
  index index.html;

  location ~* \.(?:jpg|jpeg|gif|png|svg|ico|css|js|woff2?)$ {
    expires 30d;
    access_log off;
    add_header Cache-Control "public, max-age=2592000, immutable";
    try_files $uri =404;
  }

  location / {
    try_files $uri /index.html;
  }

  location /api/ {
    proxy_pass http://backend:8000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /static/ { alias /var/www/static/; }
  location /media/  { alias /var/www/media/; }

  gzip on;
  gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss application/octet-stream image/svg+xml;
  gzip_min_length 1024;
}
NGINXCONF
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
