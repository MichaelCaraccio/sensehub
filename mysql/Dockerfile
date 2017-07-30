FROM mysql:5.7

MAINTAINER caraccio michael <michael.caraccio@gmail.com>
MAINTAINER huguenin nicolas <nichuguen@gmail.com>

#We dont need to create a user, nor to create a DB, because the the env variables are here to save our souls.

#PREVENT ERROR 2003
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
