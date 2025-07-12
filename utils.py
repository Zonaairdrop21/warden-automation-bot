import os
import json
import random
from datetime import datetime
from eth_account import Account
from colorama import Fore, Style
import pytz

display_timezone = pytz.utc

USER_AGENT = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/557.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_message(message):
    print(
        f"{Fore.CYAN}>> {Style.RESET_ALL}{message}",
        flush=True
    )

def format_time_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def load_json_data(filename):
    try:
        if not os.path.exists(filename):
            log_message(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
            return []
        with open(filename, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        log_message(f"{Fore.RED}Error decoding JSON from {filename}. Ensure it's valid JSON.{Style.RESET_ALL}")
        return []
    except Exception as e:
        log_message(f"{Fore.RED}Failed to load {filename}: {e}{Style.RESET_ALL}")
        return []

def get_masked_address(account_key):
    try:
        eth_account = Account.from_key(account_key)
        address = eth_account.address
        return address, address[:4] + '****' + address[-4:]
    except Exception as e:
        log_message(f"{Fore.RED}Invalid Private Key: {e}{Style.RESET_ALL}")
        return None, None

def check_proxy_format(proxy_url):
    schemes = ["http://", "https://", "socks4://", "socks5://"]
    if any(proxy_url.startswith(scheme) for scheme in schemes):
        return proxy_url
    return f"http://{proxy_url}"

def get_random_user_agent():
    return random.choice(USER_AGENT)