FROM nginx:1.29.5
RUN apt-get clean && apt-get update && apt-get install -y spawn-fcgi fcgiwrap

RUN sed -i 's/www-data/nginx/g' /etc/init.d/fcgiwrap
RUN chown nginx:nginx /etc/init.d/fcgiwrap

ADD ./res/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./app /var/www

WORKDIR /var/www

ADD ./res/start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]