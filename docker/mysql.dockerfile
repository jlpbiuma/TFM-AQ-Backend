# Use the latest MySQL image
FROM mysql:latest

# Copy the initialization script to the Docker entrypoint directory
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306
