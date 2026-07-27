# QuickBite ETA

## Objective

Package a small machine-learning API into one Docker image.

`train.py` creates the model during the Docker build. `app.py` loads that model
and exposes a prediction endpoint.

## Build and run

```powershell
docker build -t quickbite-eta:v1 .
docker run -d -p 8000:8000 --name quickbite-eta quickbite-eta:v1
```

Open `http://localhost:8000/docs` and use `POST /predict`, or run:

```powershell
curl.exe -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"distance_km\":4.5,\"prep_time_min\":15,\"rider_available\":1,\"is_raining\":1}"
```

## Cleanup

```powershell
docker rm -f quickbite-eta
```

## Key idea

The Dockerfile installs dependencies, copies the code, trains the model, and
starts FastAPI. After changing the code, rebuild the image before running it again.
