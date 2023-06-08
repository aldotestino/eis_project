FROM node
WORKDIR /usr/app/frontend
COPY package*.json ./
RUN yarn
COPY . .
RUN yarn build
CMD yarn preview