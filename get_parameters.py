import json


def to_json() -> dict:
    with open("./storage/store.json") as file:
        json_dict = json.load(file)
        return json_dict

def get_parameters(name: str = None) -> dict:
    if not str:
        return to_json()
    state = to_json()
    if name in state:
        return state[name]
    else:
        return state

