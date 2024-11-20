'''
 # @ Author: CuteBearrr
 # @ Create Time: 2024-11-20 13:04:23
 # @ Modified by: CuteBearrr
 # @ Modified time: 2024-11-20 14:37:57
 # @ Filename: Utility.py
 '''

import sys
import json
from loguru import logger


def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
        level="DEBUG"
    )

def load_config(config_path="config.json"):
    with open(config_path, "r") as file:
        config = json.load(file)
    return config

def convert_to_array(data):
    if isinstance(data, list):
        return data
    elif isinstance(data, set):
        return list(data)
    elif isinstance(data, str):
        return [data]
    else:
        logger.error("Conversion to array failed. Input must be a string, set or list")
