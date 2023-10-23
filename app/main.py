from fastapi import FastAPI
from pydantic import BaseModel
from opentrons.simulate import simulate, format_runlog, get_protocol_api
import os
import io
import subprocess

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "this is a test api server"}


@app.get("/protocols")
def read_protocols():
    protocols = get_file_names()
    if len(protocols) == 0:
        return "no stored protocol"
    sorted_protocols = sorted(protocols)
    return {"protocols": sorted_protocols}


def get_file_names():
    folder_path = 'storage'
    if not os.path.exists(folder_path):
        # Create the storage folder
        os.makedirs(folder_path)
        return []

    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(file)

    return file_names


# @app.get("/protocols/{protocol_id}")
# def read_protocol(protocol_id: int, q: str = None):
#     # ToDo search folder and display a protocol file if there is a target protocol
#     if q:
#         return {"protocol_id": protocol_id, "q": q}
#     return {"protocol_id": protocol_id}


class Protocol(BaseModel):
    name: str
    content: str


@app.post("/protocol")
def upload_protocol(protocol: Protocol):
    file_path = 'storage/' + protocol.name
    save_result = save_text_as_file(protocol.content, file_path)

    if type(save_result) == str:
        # response = run_protocol_on_simulator(protocol.content)
        response = call_opentrons_simulate(file_path)
        print('response', response)
        if response["status"] == "success":
            return {"protocol_name": protocol.name, "run_log": response['run_log']}
        else:
            return {"error_message": response['error_message']}
    else:
        return {"error_message": "something wrong while saving a protocol"}


def call_opentrons_simulate(protocol_path: str):
    command = f"opentrons_simulate {protocol_path}"

    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)

    if result.returncode == 0:
        # print("Command executed successfully! Output:")
        # print(result.stdout)
        return {"status": "success", "run_log": result.stdout}
    else:
        print("Command failed. Error message:")
        # print(result.stderr)
        return {"status": "error", "error_message": result.stderr}


def save_text_as_file(text, file_path):
    base = os.path.splitext(file_path)[0]
    ext = os.path.splitext(file_path)[1]
    counter = 1

    while os.path.exists(file_path):
        file_path = base + "_" + str(counter) + ext
        counter += 1

    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print("Text saved successfully as", file_path)
        return file_path
    except Exception as e:
        print("An error occurred while saving the file:", str(e))
        return False
