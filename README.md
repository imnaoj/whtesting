# README

This project is a helper tool to review incoming webhooks. Just create a path to get its webhook URL and provide it to the third party app. Whenever it posts JSON data, you'll get an update in realtime.

You can run the project locally or via Docker. The only requirement is to have a MongoDB server available - if you haven't one, you may run it as Docker instance or even signing in a MongoDB free account M0 Sandbox (see below)

## Set up a free MongoDB Atlas account

Cluster tier M0 (AWS, Azure or GCP) available forever free at https://www.mongodb.com/pricing 

## Run the project locally

### The Flask API

```bash
MONGO_URI="mongodb+srv://******:******@testing.random.mongodb.net/whtesting?retryWrites=true&w=majority&appName=Testing" python wsgi.py
```

### The Vue3+Quasar frontend

```bash
quasar dev
```

## Run the project as a Docker

### Build the image

```bash
docker build -t whtesting .
```

### Run the image

```bash
docker run --detach --name whtinstance --env MONGO_URI="mongodb+srv://******:******@testing.random.mongodb.net/whtesting?retryWrites=true&w=majority&appName=Testing" --env API_URL="http://localhost" --env CORS_ORIGINS="http://localhost" -p 80:80 whtesting:latest
```

## Testing the webhook

```bash
curl -X POST http://localhost/api/webhook/fkONWGJveJj20LlH/ejemplo1
  -H "Content-Type: application/json"
  -d '{
        "event": "process_completed",
        "solicitud_id": 2346787867,
        "firmantes_id":[34534534534,534543534534]
    }'
```
