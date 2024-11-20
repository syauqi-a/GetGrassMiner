# GetGrassMiner
Automate Grass point mining by running a Python script built to handle connections to WebSocket. You can use multiple devices and IP addresses to maximize earnings. This program was tested on Windows OS using Python version 3.10.

# Table of Contents
- [GetGrassMiner](#getgrassminer)
- [Table of Contents](#table-of-contents)
- [Warnings and Notes](#warnings-and-notes)
- [Features](#features)
- [Registration](#registration)
- [How to Use Locally](#how-to-use-locally)
- [Setting up .env file](#setting-up-env-file)
- [Setting up config.json file](#setting-up-configjson-file)
- [Proxies](#proxies)
  - [Generate Proxies](#generate-proxies)
- [Discussion Forum](#discussion-forum)
- [Support](#support)
- [Thank You](#thank-you)

# Warnings and Notes

All risks remain with the user! This program only supports one account.

# Features
- Connects to a WebSocket server using proxies.
- Allow multiple proxies.
- Handles all kinds of Error such a Dead proxy/ SSL: WRONG_VERSION_NUMBER / invalid length of packed IP address / Empty connect reply / sent 1011 (internal error) keepalive.
- Automatically removes the dead proxy from the File!
- Automatically fetch data from API or proxy sources.

# Registration

If you haven't registered for grass yet, please use the following URL: [Click here](https://app.getgrass.io/register/?referralCode=n_3jaZkKdDJnEcS)

# How to Use Locally

1. Make sure your computer has Python and Git installed
   
2. Open terminal on your device (CMD/Powershell/Terminal)

3. Clone this repository. You can use the command below:
   ```shell
   git clone https://github.com/syauqi-a/GetGrassMiner.git
   ```

4. Enter the GetGrassMiner folder:
   ```shell
   cd GetGrassMiner
   ```

5. Generate `.env` file manually from example file.
   ```shell
   cp .env.example .env
   ```
   Follow the [instructions](#setting-up-env-file) to setup the generated `.env` file.

6. If necessary, set the `config.json` file following the [instructions](#setting-up-configjson-file) as desired.

7. **(Optional)** It is recommended to create a virtual environment.
   ```shell
   python -m venv .venv
   ```
   Then activate the virtual environment that has been created. Adjust it to the operating system you are using.
   ```shell
   # on Unix/macOS:
   source .venv/bin/activate

   # on Windows:
   .venv\Scripts\activate
   ```

8. Then install the required libraries:
   ```shell
   python -m pip install -r requirements.txt
   ```

9. Fill in your proxies in the `proxies.txt` file according to the examples provided in [Proxies](#proxies). If you do not complete the `proxies.txt` file, the program will stop. To automatically generate proxies from the API, see [here](#generate-proxies).

10. Run the `main.py` file:
   
   ```shell
   python main.py
   ```

# Setting up .env file

In the `.env` file you have to set the user id with yours. If you don't know your user id, do the following steps.
1. Open the link and log in https://app.getgrass.io/dashboard.
2. Press F12 on the page to open the console and enter the code (Ctrl + Shift + i) inspect.
3. Copy following code to the console:
   ```javascript
   copy(JSON.parse(localStorage.getItem("userId")))
   ```
   If you see the warning "Warning: Don't paste code into the DevTools Console that you don't" when pasting the JavaScript code above, type `allow pasting` and press enter first.

4. The code above automatically copies the user id to your clipboard, so you just need to paste it into the `.env` file.

# Setting up config.json file

For usage examples, see the `config.json.example` file. Here's an explanation of the contents of the config.json file:

| key | value | description |
| --- | --- | --- |
| proxy | dictionary ||
| proxy.filename | string | proxy.txt file path |
| proxy.auto_fetch_new | bool | Whether to perform a fetch if the proxy queue has run out |
| proxy.pool_list | array ||
| proxy.pool_list.{}.response_format | string | The response returned when performing a fetch to a url |
| proxy.pool_list.{}.url | string | URL for fetching proxy data. It could be an API url |
| proxy.pool_list.{}.proxy_list_key | string | If the response format is JSON, tell which key stores the proxy list |
| proxy.pool_list.{}.proxy_key | string | If the response format is JSON, tell which key stores the proxy string in the proxy list |
| proxy.pool_list.{}.proxy_row | string | If the response format is CSV, tell which row stores the proxy string. |
||||
| connection | dictionary ||
| connection.ws_url | string | websocket url |
| connection.number_of_proxies | integer | The number of proxies running concurrently |
| connection.max_retries | integer | Maximum limit of attempts to make connections to websockets |
| connection.retry_delay | integer | The retry time delay establishes a connection to the websockets |
| connection.interval_ping | integer | Delay time sends ping messages to websocket |
| connection.max_timeout | integer | Timeout when establishing connection to websocket |
||||
| extension | dictionary ||
| extension.id | string ||
| extension.version | string ||


# Proxies

Save the proxy list in the [proxies file](proxies.txt). The format used follows the following example:

Example formats:
```
http://host:port
socks5://host:port
http://user:password@host:port
socks5://user:password@host:port
```

## Generate Proxies
If you have added the proxy pool list to your `config.json` (see the guide to setting up `config.json` [here](#setting-up-configjson-file)). You can automate fetching proxy data directly from the API to a `proxies.txt` file.
```shell
python UpdateProxiesFile.py
```

# Discussion Forum

If you have any questions, don't hesitate to ask [me](https://t.me/cutebearrr) or discuss [here](https://github.com/syauqi-a/GetGrassMiner/discussions).

# Support

If you like my project, you can buy me a coffee through the websites below:
  
- USDT (BNB Smart Chain (BEP20)) Address: `0x5389781e243db1c3bb5b3e734a17d8c5eb963106`
- TON Address: `EQD5mxRgCuRNLxKxeOjG6r14iSroLF5FtomPnet-sgP5xNJb` (`136075219`)
- SOLANA Address: `Hn4G1XZmKcdWRPWTS4UX59wRA2cuDZ3uQE28fCjQ6sRb`

# Thank You
Thank you for taking the time to check out my repository! This project is inspired by two amazing individuals, [@Solana0x](https://github.com/Solana0x) and [@akasakaid](https://github.com/akasakaid). You guys are awesome!
