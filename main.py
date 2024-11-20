'''
 # @ Author: CuteBearrr
 # @ Create Time: 2024-11-20 13:04:23
 # @ Modified by: CuteBearrr
 # @ Modified time: 2024-11-20 14:37:12
 # @ Filename: main.py
 '''

import os
import sys
from dotenv import load_dotenv
import asyncio
import signal
from loguru import logger
from utils import setup_logger, WebSocketProxyConnector


load_dotenv()

def exit_signal_handler():
    logger.critical(
        "Program forcibly terminated. Waiting for worker to finish..."
    )

    sys.exit()

def main():
    logger.info("Running main function...")

    config_path="config.json"
    user_id = os.getenv("USER_ID")
    connector = WebSocketProxyConnector(user_id, config_path)

    if sys.platform == "win32":
        logger.info("Windows detected. Signal handling may not be supported fully.")
        try:
            asyncio.run(connector.start())
        except (KeyboardInterrupt, SystemExit):
            logger.warning("Main function was cancelled.")
            exit_signal_handler()
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for signame in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(signame, exit_signal_handler)

        try:
            loop.run_until_complete(connector.start())
        except Exception as e:
            logger.warning(f"An error occurred while executing the loop. {e}")
        finally:
            logger.info(
                "Closing the event loop and canceling the running task..."
            )
            loop.close()

if __name__ == "__main__":
    setup_logger()

    main()
