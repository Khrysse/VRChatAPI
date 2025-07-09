FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y apache2 php libapache2-mod-php supervisor && \
    a2enmod rewrite && \
    a2enmod headers && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Configure Apache
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf
RUN rm -rf /var/www/html && ln -s /app/php /var/www/html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 