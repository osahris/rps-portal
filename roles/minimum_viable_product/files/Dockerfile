FROM nginx:latest

COPY ./nginx/conf.d/default.conf /etc/nginx/conf.d
COPY ./nginx/html/index.html /usr/share/nginx/html

ENTRYPOINT nginx -g 'daemon off;'