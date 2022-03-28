import json, io


def load(json_string=None, json_file=None):
    HDR10Plus_DCT = {}
    if json_string and json_file:
        raise RuntimeError(
            f"{__name__ }.load() expected only one 'json_string' or 'json_file' to be specified."
        )
    if not (json_string or json_file):
        raise RuntimeError(
            f"{__name__ }.load() expected either 'json_string' or 'json_file' to be specified."
        )
    if json_string:
        if type(json_string) is not str:
            raise ValueError(
                f"{__name__ }.load() expected 'json_string' to be a string, recieved type: '{ype(json_string)}'."
            )
        HDR10Plus_DCT = json.loads(json_string)
    elif json_file:
        if (type(json_file) is not str) and (type(json_file) is not io.TextIOWrapper):
            pass
            raise ValueError(
                f"{__name__ }.load() expected 'json_file' to be a string or a file, recieved type: '{type(json_file)}'."
            )
        if type(json_file) is str:
            json_file = open(json_file)
        HDR10Plus_DCT = json.load(json_file)
    return HDR10Plus_DCT


def export(dct, saveName):
    with open(saveName, "w") as jsonFile:
        json.dump(dct, jsonFile)
