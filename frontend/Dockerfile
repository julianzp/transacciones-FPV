FROM node:14

WORKDIR /web-app

COPY web-app/package*.json ./

RUN npm install

COPY web-app/ ./

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
