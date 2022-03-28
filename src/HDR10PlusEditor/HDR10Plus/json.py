"""Functions for loading/saving a JSON file.
"""
# pylint: disable=invalid-name,line-too-long

import json
import io


def load(json_string=None, json_file=None):
    """Load the json to a dct
    Keyword arguments:
    json_string -- The path, as a string.
    json_file -- The path, as a file.
    """
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
        if not isinstance(json_string, str):
            raise ValueError(
                f"{__name__ }.load() expected 'json_string' to be a string, recieved type: '{type(json_string)}'."
            )
        HDR10Plus_DCT = json.loads(json_string)
    elif json_file:
        if not isinstance(json_file, str) and not isinstance(
            json_file, io.TextIOWrapper
        ):
            raise ValueError(
                f"{__name__ }.load() expected 'json_file' to be a string or a file, recieved type: '{type(json_file)}'."
            )
        if isinstance(json_file, str):
            #  pylint: disable=consider-using-with
            json_file = open(json_file, mode="r", encoding="utf-8")
            #  pylint: enable=consider-using-with
        HDR10Plus_DCT = json.load(json_file)
    return HDR10Plus_DCT


def export(dct, saveName):
    """Save the dct to a file.
    Keyword arguments:
    dct -- The dct to be saved.
    saveName -- The path to save, as a string.
    """
    with open(saveName, mode="w", encoding="utf-8") as jsonFile:
        json.dump(dct, jsonFile)
