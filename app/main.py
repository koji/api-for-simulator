from fastapi import FastAPI
from pydantic import BaseModel
from opentrons.simulate import simulate, format_runlog, get_protocol_api
import os
import io

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "this is a test api server"}


@app.get("/protocols")
def read_protocols():
    protocols = get_file_names()
    sorted_protocols = sorted(protocols)
    return {"protocols": sorted_protocols}


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
    file_path = 'storage/' + protocol.name
    save_result = save_text_as_file(protocol.content, file_path)
    
    if save_result:
        response = run_protocol_on_simulator(protocol.content)
        
        print('response', response)
        if response["status"] == "success":
            return {"protocol_name": protocol.name, "run_log": response['run_log']}
        else:
            return {"error_message": response['error_message']}
    else:
        return {"error_message": "something wrong while saving a protocol"}


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
    try:
        run_log = simulate(protocol_file)
        run_log = format_runlog(run_log)
        return {"status": "success", "run_log": run_log, "error_message": error_message}
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {"status": "error", "run_log": '', "error_message": error_message}
