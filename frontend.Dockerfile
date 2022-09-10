FROM node:16.6.0-slim

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# RUN npm init -y
COPY . .
# RUN npm i -s express
RUN npm i
RUN npm run build


EXPOSE 3000
CMD [ "node", "server.js" ]
