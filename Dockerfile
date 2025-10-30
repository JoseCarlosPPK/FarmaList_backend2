FROM mysql:8.0.21

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=centros_farmacia

COPY ./database/db.sql /docker-entrypoint-initdb.d/

#EXPOSE 3306
