FROM node:19-slim
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY app.js .
CMD ["npm", "start"]