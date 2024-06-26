# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the Nginx configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static website files into the container
COPY . /usr/share/nginx/html

# Expose the port that Nginx will run on
EXPOSE 8002

# Start Nginx (default command of the Nginx image)