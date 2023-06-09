FROM php:8.0-fpm
LABEL MAINTAINER="Thomas Laurenson <thomas@thomaslaurenson.com>"


RUN apt-get update \
    && apt-get install -y libpq-dev \
    && docker-php-ext-install pdo pgsql
