FROM node:20

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

COPY frontend /app
RUN npm run build

EXPOSE 5173
CMD ["npm", "run", "dev"]