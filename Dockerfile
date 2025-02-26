# Use Ubuntu as base image
FROM ubuntu:22.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install latest version of Node 22
RUN curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Install global npm packages (Quasar CLI)
RUN npm install -g @quasar/cli

# Copy files
COPY whtapi /app/whtapi
COPY whtconsole /app/whtconsole

# Install Python dependencies
WORKDIR /app/whtapi
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

# Build Quasar application
WORKDIR /app/whtconsole
RUN npm install
RUN quasar build

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/whtesting
RUN ln -s /etc/nginx/sites-available/whtesting /etc/nginx/sites-enabled/

# Create directory for socket
RUN mkdir -p /run/whtesting

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port 80
EXPOSE 80

# Start services
CMD ["/start.sh"] 
