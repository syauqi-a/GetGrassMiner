'''
 # @ Author: CuteBearrr
 # @ Create Time: 2024-11-20 13:04:23
 # @ Modified by: CuteBearrr
 # @ Modified time: 2024-11-20 14:38:22
 # @ Filename: Proxies.py
 '''

import requests
import csv
import io
import re
from loguru import logger
from utils.Utility import convert_to_array


def format_url(input_string: str):
    if input_string.startswith("#"):
        return None

    protocol_pattern = re.compile(r'(\w+)://')
    ip_port_pattern = re.compile(r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}):([\d]{1,5})')

    ip_port_match = ip_port_pattern.search(input_string)
    if ip_port_match == None:
        return None

    protocol_match = protocol_pattern.match(input_string)

    if protocol_match:
        protocol = protocol_match.group(1)
        ip = ip_port_match.group(1)
        port = ip_port_match.group(2)
        return f"{protocol}://{ip}:{port}"
    else:
        ip = ip_port_match.group(1)
        port = ip_port_match.group(2)
        return f"http://{ip}:{port}"

def fetch_data(**kwargs):
    data_array = []

    try:
        url = kwargs['url']
        response_format = kwargs['response_format']

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if response_format.lower() == "json":
            data = response.json()

            if isinstance(data, list):
                data_array = [format_url(proxy) for proxy in data
                              if format_url(proxy) is not None]
            elif isinstance(data, dict):
                proxy_list_key = kwargs["proxy_list_key"]
                proxy_key = kwargs["proxy_key"]

                proxies = data[proxy_list_key]
                data_array = [format_url(proxy[proxy_key]) for proxy in proxies
                              if format_url(proxy[proxy_key]) is not None]

        elif response_format.lower() == "text":
            data = response.text.splitlines()
            data_array = [format_url(proxy) for proxy in data
                          if format_url(proxy) is not None]

        elif response_format.lower() == "csv":
            proxy_row = kwargs["proxy_row"]

            csv_reader = csv.DictReader(io.StringIO(response.text))
            if proxy_row in csv_reader.fieldnames:
                data_array = [format_url(row[proxy_row]) for row in csv_reader
                              if format_url(row[proxy_row]) is not None]

        else:
            logger.info(
                "Response format is not recognized. Use 'json', 'text', or 'csv'."
            )

    except KeyError as e:
        logger.error(f"Error: Parameter '{e.args[0]}' is required but not given.")

    except requests.exceptions.RequestException as e:
        logger.error("Error when making a request:", e)

    return data_array

def get_proxies(proxy_pool_list):
    proxies = []
    for pool in proxy_pool_list:
        try:
            # Mengambil daftar proxy
            proxies += fetch_data(**pool)
        except Exception as e:
            logger.error(f"Failed to fetch proxy pool from url. {e}")

    return proxies

def save_data_to_file(data, file_path="proxies.txt"):
    try:
        data = convert_to_array(data)

        with open(file_path, "w") as file:
            for item in data:
                _item = item.strip()
                if _item:
                    file.write(f"{_item}\n")

    except Exception as e:
        logger.error(f"An error occurred while saving data to file: {e}")

def append_data_to_file(new_data, file_path="proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            existing_data = file.readlines()

        if isinstance(new_data, str):
            new_data = [new_data]
        elif isinstance(new_data, set):
            new_data = list(new_data)
        merged_data = existing_data + new_data

        merged_data = set(merged_data)

        save_data_to_file(merged_data, file_path)

        return True

    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return False
    except Exception as e:
        logger.error(f"An error occurred while adding data to the file: {e}")
        return False

def fetch_new_proxies(proxy_pool_list, file_path="proxies.txt"):
    proxies = get_proxies(proxy_pool_list)

    append_data_to_file(proxies, file_path)

def get_proxies_from_file(file_path="proxies.txt"):
    proxies = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                proxy = line.strip()
                if proxy and ":" in proxy and not proxy.startswith("#"):
                    proxies.append(proxy)
        return proxies
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return []
    except Exception as e:
        logger.error(f"An error occurred while reading the file: {e}")
        return []

def remove_proxy_from_file(proxy_to_remove, file_path="proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        updated_lines = [line.strip() for line in lines
                         if proxy_to_remove not in line]

        if len(updated_lines) == len(lines):
            return False

        save_data_to_file(updated_lines, file_path)

        return True

    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return False
    except Exception as e:
        logger.error(f"An error occurred while removing data from the file: {e}")
        return False
