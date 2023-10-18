# api-for-simulator

api server for opentrons-simulator

## how to run locally

```shell
pip install -r requirements.txt

cd app
uvicorn main:app --reload
```

### docs

```shell
uvicorn main:app
```

Then go to http://localhost:8000/docs to check the api doc.

`/protocol/id` does not work since it is a dummy function right now.

## How to run the server with Dockerfile

```shell
git clone https://github.com/koji/api-for-simulator.git
cd api-for-simulator
docker build -t simulator-api:1.0.0 .
```

After building the image

```shell
docker run -d --name simulator-api-container -p 80:80 simulator-api:1.0.0
```

Check the container

```shell
docker ps -q -f "name=simulator-api-container" | xargs docker logs -f
```

Test the api server with curl or postman/httpie

```shell
curl localhost:80
```

## Tool

- postman: https://www.postman.com/
- httpie: https://httpie.io/
