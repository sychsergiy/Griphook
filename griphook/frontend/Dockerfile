FROM node
MAINTAINER Dockerfiles
WORKDIR /front/
COPY Griphook-Frontend .
RUN npm install
RUN npm run build

FROM nginx
MAINTAINER Dockerfiles
WORKDIR /etc/static
COPY --from=0 /front/dist/bundle.js /etc/nginx/dist/static/bundle.js
COPY --from=0 /front/dist/index.html /etc/nginx/html/index.html
EXPOSE 80