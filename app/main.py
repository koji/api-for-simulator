from fastapi import FastAPI
from pydantic import BaseModel
from opentrons.simulate import simulate, format_runlog, get_protocol_api
import io
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "this is a test api server"}


@app.get("/protocols")
def read_protocols():
    protocols = get_file_names()
    print(protocols)
    return {"protocols": protocols}


def get_file_names():
    folder_path = 'storage'
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(file)
    return file_names


@app.get("/protocols/{protocol_id}")
def read_protocol(protocol_id: int, q: str = None):
  # ToDo search folder and display a protocol file if there is a target protocol
    if q:
        return {"protocol_id": protocol_id, "q": q}
    return {"protocol_id": protocol_id}



class Protocol(BaseModel):
    name: str
    content: str

@app.post("/protocol")
def upload_protocol(protocol: Protocol):
    file_path = 'storage/'+protocol.name
    save_result = save_text_as_file(protocol.content, file_path)
    if save_result == True:
        run_log = run_protocol_on_simulator(protocol.content)
        return {"protocol_name": protocol.name, "runlog": run_log}
    else:
        return {"message": "something wrong"}


def save_text_as_file(text, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print("Text saved successfully as", file_path)
        return True
    except Exception as e:
        print("An error occurred while saving the file:", str(e))
        return False


def run_protocol_on_simulator(protocol_string):
    protocol_file = io.StringIO(protocol_string)

    # Simulate the protocol
    protocol_context, run_log = simulate(protocol_file)
    return (format_runlog(protocol_context))
