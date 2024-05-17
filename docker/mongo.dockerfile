FROM mongo:latest

# Set environment variables
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=password

# Copy the initialization script
COPY ./conf/init-mongo.sh /docker-entrypoint-initdb.d/init-mongo.sh

# Install dos2unix and convert line endings
RUN apt-get update && apt-get install -y dos2unix && dos2unix /docker-entrypoint-initdb.d/init-mongo.sh && \
    chmod +x /docker-entrypoint-initdb.d/init-mongo.sh

EXPOSE 27017
