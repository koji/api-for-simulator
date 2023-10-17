# api-for-simulator
api server for opentrons-simulator


### how to run
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
