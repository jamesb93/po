import json

def read_json(path: str) -> dict:
    with open(path) as json_file:
        return json.load(json_file)

def write_json(path: str, data: dict) -> None:
    with open(path, 'w') as output:
        json.dump(data, output, indent=4)