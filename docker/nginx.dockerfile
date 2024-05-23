# Use the official NGINX base image from the Docker Hub
FROM nginx:latest

# Install gettext for envsubst
RUN apt-get update && apt-get install -y gettext

# Copy custom NGINX configuration files into the container
COPY ./conf/nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates into the container
COPY ./certs/server.crt /etc/nginx/certs/server.crt
COPY ./certs/server.key /etc/nginx/certs/server.key

# Expose the necessary ports
EXPOSE 80 443 5000

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
