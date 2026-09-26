import json

def load_data(files):
    data = []

    for filename in files:
        with open(filename, "r", encoding="utf-8") as file:
            file_data = json.load(file)

        data.extend(file_data)

    return data

def load_travel_overrides(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)