#!/bin/bash

# If API_URL is present, replace the default localhost:5000 with the provided value
if [ ! -z "$API_URL" ]; then
    sed -i "s|http://localhost:5000|$API_URL|g" /app/whtconsole/dist/spa/js/*.js
fi

# Start Gunicorn with gevent worker
cd /app/whtapi
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
         --workers 1 \
         --bind unix:/run/whtesting/gunicorn.sock \
         'app:create_app()' &

# Start Nginx
nginx -g 'daemon off;' 