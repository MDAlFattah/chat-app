# Use the official PHP image as a base image
FROM php:apache

# Copy the contents of the current directory into the /var/www/html directory in the container
COPY . /var/www/html/

# Install mysqli extension
RUN docker-php-ext-install mysqli

# Set index.php as the default index file
RUN echo "DirectoryIndex index.php" >> /etc/apache2/apache2.conf

# Expose port 80
EXPOSE 80
