#!/bin/bash
set -e

APACHE_PORT=${APACHE_PORT:-8080}

# Modifier le port d'écoute d'Apache
sed -i "s/Listen 80/Listen ${APACHE_PORT}/" /etc/apache2/ports.conf
sed -i "s/<VirtualHost *:80>/<VirtualHost *:${APACHE_PORT}>/" /etc/apache2/sites-available/000-default.conf

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf 