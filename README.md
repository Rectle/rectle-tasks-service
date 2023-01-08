
## Build

```
docker build --tag rectle-tasks-service:python .
```

## Run Locally

```sh
python main.py
```

```
docker run --rm -p 5000:5000 -e PORT=5000 rectle-tasks-service:python
```

## Deploy

```sh
export GOOGLE_CLOUD_PROJECT=rectle-platform

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/rectle-tasks-service

# Deploy to Cloud Run
gcloud run deploy rectle-tasks-service --image gcr.io/${GOOGLE_CLOUD_PROJECT}/rectle-tasks-service
```