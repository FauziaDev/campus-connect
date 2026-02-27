# Use an official Python and Apache image
FROM python:3.10-slim

# Install Apache and CGI module
RUN apt-get update && \
    apt-get install -y apache2 apache2-utils && \
    apt-get clean

# Enable CGI module
RUN a2enmod cgi

# Set up the working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Make all .py files executable
RUN chmod +x /app/*.py

# Make /app the web root for Apache
RUN rm -rf /var/www/html && ln -s /app /var/www/html

# Configure Apache to allow CGI in /app
RUN echo "ScriptAlias /cgi-bin/ /app/\n\
<Directory \"/app\">\n\
    Options +ExecCGI\n\
    AddHandler cgi-script .py\n\
    Require all granted\n\
</Directory>" > /etc/apache2/conf-available/webtask-cgi.conf \
    && a2enconf webtask-cgi

# Expose port 80
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
