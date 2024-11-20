'''
 # @ Author: CuteBearrr
 # @ Create Time: 2024-11-20 13:04:23
 # @ Modified by: CuteBearrr
 # @ Modified time: 2024-11-20 14:36:23
 # @ Filename: UpdateProxiesFile.py
 '''

from loguru import logger
from utils import setup_logger, load_config, get_proxies, append_data_to_file


if __name__ == "__main__":
    setup_logger()

    config_path = 'config.json'
    config = load_config(config_path)
    proxy_pool_list = config["proxy"]["pool_list"]

    if proxy_pool_list == []:
        logger.warning("You have not added the proxy pool list to config.json.")
        exit(0)

    try:
        logger.info(f"Fetching the proxy pool from the url")
        proxies = get_proxies(proxy_pool_list)
    except Exception as e:
        logger.error(f"Failed to fetch proxy pool from url. {e}")

    try:
        proxies_path = 'proxies.txt'
        append_data_to_file(proxies, proxies_path)
        logger.info(f"{proxies_path} updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update {proxies_path}. {e}")
    
