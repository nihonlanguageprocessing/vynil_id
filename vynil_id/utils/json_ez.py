import json

def json_ez(json_string, destination, **kwargs):
    with open(destination, 'w') as outfile:
        json.dump(json_string, outfile, **kwargs)
