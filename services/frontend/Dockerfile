FROM node:8

WORKDIR /app

# Cache dependencies if possible
ADD package.json .
RUN npm install

ADD tsconfig.json .
ADD src ./src
RUN npm run compile

EXPOSE 8080

CMD npm run start
