FROM node:8

WORKDIR /app

# Cache dependencies if possible
ADD package.json .
RUN npm install

ADD tsconfig.json .
ADD src ./src
RUN npm run compile

ADD src/protos ./built/protos
ADD src/config ./built/config
ENV NODE_CONFIG_DIR=./built/config

EXPOSE 8080

CMD npm run start
