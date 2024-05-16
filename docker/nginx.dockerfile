# Use the official NGINX base image from the Docker Hub
FROM nginx:latest

# Install gettext for envsubst
RUN apt-get update && apt-get install -y gettext

# Copy custom NGINX configuration file into the container
COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the entire nginx directory (which includes certificates) into the container
COPY ./certs /etc/nginx/cert

# Expose the necessary ports
EXPOSE 80 443 5000

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]