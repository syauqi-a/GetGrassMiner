'''
 # @ Author: Your name
 # @ Create Time: 2024-11-22 16:22:46
 # @ Modified by: Your name
 # @ Modified time: 2024-11-22 16:25:34
 # @ Description:
 '''

import asyncio
import ssl
import uuid
import json
import time
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent
from utils.Utility import load_config
from utils.Proxies import (
    remove_proxy_from_file, fetch_new_proxies, get_proxies_from_file
)


class WebSocketProxyConnector:
    def __init__(self, user_id, config_path="config.json"):
        self.user_id = user_id

        config = load_config(config_path)

        proxy_config = config["proxy"]
        self.proxy_path = proxy_config["filename"]
        self.auto_fetch = proxy_config["auto_fetch_new"]
        self.proxy_pool_list = proxy_config["pool_list"]

        conn_config = config["connection"]
        self.ws_url = conn_config["ws_url"]
        self.max_connections = conn_config["number_of_proxies"]
        self.max_retries = conn_config["max_retries"]
        self.retry_delay = conn_config["retry_delay"]
        self.interval_ping = conn_config["interval_ping"]
        self.max_timeout = conn_config["max_timeout"]

        ext_config = config["extension"]
        self.extension_id = ext_config["id"]
        self.extension_version = ext_config["version"]

        self.lock = asyncio.Lock()

    async def ping(self, websocket, proxy_str):
        while True:
            send_message = json.dumps({
                "id": str(uuid.uuid4()),
                "version": "1.0.0",
                "action": "PING",
                "data": {}
            })
            logger.opt(colors=True).info(
                f"<yellow>{proxy_str}</yellow> sent <green>ping</green>"
            )
            await websocket.send(send_message)
            await asyncio.sleep(self.interval_ping)

    async def connect_with_proxy(self, proxy_str, ws_url):
        device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, proxy_str))
        proxy = Proxy.from_url(proxy_str)
        retries = 0

        while True:
            try:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                user_agent = UserAgent().random
                custom_header = {
                    "Origin": "chrome-extension://" + self.extension_id,
                    "User-Agent": user_agent
                }
                async with proxy_connect(
                    ws_url,
                    proxy=proxy,
                    ssl=ssl_context,
                    extra_headers=custom_header,
                    proxy_conn_timeout=self.max_timeout
                ) as websocket:
                    send_ping_task = asyncio.create_task(
                        self.ping(websocket, proxy_str)
                    )
                    try:
                        while True:
                            response = await websocket.recv()
                            message = json.loads(response)
                            if message.get("action") == "AUTH":
                                auth_response = {
                                    "id": message["id"],
                                    "origin_action": "AUTH",
                                    "result": {
                                        "browser_id": device_id,
                                        "user_id": self.user_id,
                                        "user_agent": user_agent,
                                        "timestamp": int(time.time()),
                                        "device_type": "extension",
                                        "version": self.extension_version,
                                        "extension_id": self.extension_id
                                    }
                                }
                                await websocket.send(json.dumps(auth_response))

                            elif message.get("action") == "PONG":
                                pong_response = {
                                    "id": message["id"],
                                    "origin_action": "PONG"
                                }
                                logger.opt(colors=True).info(
                                    f"<yellow>{proxy_str}</yellow> sent <magenta>pong</magenta>"
                                )
                                await websocket.send(json.dumps(pong_response))
                    finally:
                        send_ping_task.cancel()

            except KeyboardInterrupt:
                send_ping_task.cancel()
                return False

            except Exception as e:
                retries += 1
                max_ret = self.max_retries
                logger.opt(colors=True).warning(
                    f"<yellow>{proxy_str}</yellow> Attempt {retries}/{max_ret} failed: {e}"
                )

                if any(error_msg in str(e) for error_msg in [
                    "Host unreachable",
                    "[SSL: WRONG_VERSION_NUMBER]",
                    "invalid length of packed IP address string",
                    "Empty connect reply",
                    "Device creation limit exceeded",
                    "sent 1011 (internal error) keepalive ping timeout; no close frame received"
                ]):
                    logger.opt(colors=True).debug(
                        f"<yellow>{proxy_str}</yellow> A blacklisted error "
                        + "occurred! <red>Removing from proxy list</red>."
                    )
                    async with self.lock:
                        remove_proxy_from_file(proxy_str, self.proxy_path)
                    return False

                ret_delay = self.retry_delay
                if retries < max_ret:
                    logger.opt(colors=True).warning(
                        f"<yellow>{proxy_str}</yellow> Retrying in {ret_delay} seconds..."
                    )
                    await asyncio.sleep(ret_delay)

                else:
                    logger.opt(colors=True).debug(
                        f"<yellow>{proxy_str}</yellow> Failed after {max_ret}"
                        + "attempts. <red>Removing from proxy list</red>."
                    )
                    async with self.lock:
                        remove_proxy_from_file(proxy_str, self.proxy_path)
                    return False

    async def worker(self, proxy_queue, semaphore):
        while True:
            proxy_str = await proxy_queue.get()

            async with semaphore:
                success = await self.connect_with_proxy(proxy_str, self.ws_url)
                if not success:
                    logger.opt(colors=True).warning(f"<yellow>{proxy_str}</yellow> Connection Failed.")

            if proxy_queue.empty():
                if self.auto_fetch == False:
                    proxy_queue.task_done()

                logger.info("Proxy queue is empty trying add from proxies file.")
                async with self.lock:
                    fetch_new_proxies(self.proxy_pool_list, self.proxy_path)
                    new_proxies = get_proxies_from_file(self.proxy_path)

                    if new_proxies == []:
                        proxy_queue.task_done()

                    for proxy in new_proxies:
                        if proxy:
                            await proxy_queue.put(proxy)

    async def start(self):
        proxies = get_proxies_from_file(self.proxy_path)
        if proxies == []:
            logger.warning(
                "Your proxies.txt file is empty, please add proxy data first."
            )
            return

        proxy_queue = asyncio.Queue()
        semaphore = asyncio.Semaphore(self.max_connections)

        for proxy in proxies:
            if proxy:
                await proxy_queue.put(proxy)

        tasks = [
            asyncio.create_task(self.worker(proxy_queue, semaphore))
            for _ in range(self.max_connections)
        ]

        if tasks == []:
            logger.warning("Your proxies.txt file is empty or does not"
                           + "have a valid proxy string.")

        try:
            await proxy_queue.join()
        except asyncio.CancelledError:
            pass
        finally:
            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

            logger.info("All workers have stopped and there are no more queues.")
