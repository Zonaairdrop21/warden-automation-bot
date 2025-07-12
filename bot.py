from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from eth_account import Account
from datetime import datetime, timezone
from colorama import *
import asyncio, random, uuid, json, os, pytz
import time # Import time for potential minor delays in animations

wib = pytz.timezone('Asia/Jakarta')

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

class Warden:
    def __init__(self) -> None:
        self.PRIVY_API = "https://auth.privy.io"
        self.BASE_API = "https://api.app.wardenprotocol.org/api"
        self.AGENTS_API = "https://warden-app-agents-prod-new-d1025b697dc25df9a5654bc047bbe875.us.langgraph.app"
        self.PRIVY_HEADERS = {}
        self.BASE_HEADERS = {}
        self.AGENTS_HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        self.clear_terminal() # Clear before displaying welcome
        print(f"{Fore.BLUE + Style.BRIGHT}")
        print("   _      _      _      _      _      _      _")
        print("  / \\    / \\    / \\    / \\    / \\    / \\    / \\")
        print(" ( W )  ( A )  ( R )  ( D )  ( E )  ( N )  ( ? )") # Placeholder for P
        print("  \\_/    \\_/    \\_/    \\_/    \\_/    \\_/    \\_/")
        print(f"{Fore.CYAN + Style.BRIGHT}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.GREEN + Style.BRIGHT}   ██████╗  ██████╗ ███████╗██╗   ██╗███████╗██████╗ ")
        print(f"{Fore.GREEN + Style.BRIGHT}  ██╔════╝ ██╔════╝ ██╔════╝██║   ██║██╔════╝██╔════╝ ")
        print(f"{Fore.GREEN + Style.BRIGHT}  ██║  ███╗██║  ███╗███████╗██║   ██║███████╗██║  ███╗")
        print(f"{Fore.GREEN + Style.BRIGHT}  ██║   ██║██║   ██║╚════██║██║   ██║╚════██║██║   ██║")
        print(f"{Fore.GREEN + Style.BRIGHT}  ╚██████╔╝╚██████╔╝███████║╚██████╔╝███████║╚██████╔╝")
        print(f"{Fore.GREEN + Style.BRIGHT}   ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝  ╚══════╝ ╚═════╝ ")
        print(f"{Fore.CYAN + Style.BRIGHT}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.WHITE + Style.BRIGHT}           Powered by Zonaairdrop{Style.RESET_ALL}")
        print(f"{Fore.YELLOW + Style.BRIGHT}           Telegram: @ZonaAirdr0p{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        time.sleep(1) # Small delay for better aesthetic


    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_question_lists(self):
        filename = "question_lists.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return []
            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found. Running without proxy.{Style.RESET_ALL}")
                return # No proxies, so essentially act as if "without proxy" was chosen

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Loaded : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}" # Default to http if no scheme specified

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            return address
        except Exception as e:
            return None
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account 
        except Exception as e:
            return None
    
    def generate_payload(self, account: str, address: str, nonce: str):
        try:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            message = f"app.wardenprotocol.org wants you to sign in with your Ethereum account:\n{address}\n\nBy signing, you are proving you own this wallet and logging in. This does not initiate a transaction or cost any fees.\n\nURI: https://app.wardenprotocol.org\nVersion: 1\nChain ID: 1\nNonce: {nonce}\nIssued At: {timestamp}\nResources:\n- https://privy.io"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "message":message,
                "signature":signature,
                "chainId":"eip155:1",
                "walletClientType":"metamask",
                "connectorType":"injected",
                "mode":"login-or-sign-up"
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")

    def generate_stream_payload(self, message: str):
        try:
            payload = {
                "input":{
                    "messages":[{
                        "id":str(uuid.uuid4()),
                        "type":"human",
                        "content":message
                    }]
                },
                "metadata":{
                    "addresses":[]
                },
                "stream_mode":[
                    "values",
                    "messages-tuple",
                    "custom"
                ],
                "stream_resumable":True,
                "assistant_id":"agent",
                "on_disconnect":"continue"
            }

            return payload
        except Exception as e:
            return None
        
    def print_question(self):
        while True:
            try:
                print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}┌──────────────────────────────────────────────┐{Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}│ {Fore.WHITE}1. Run With Private Proxy{Fore.LIGHTCYAN_EX}          │{Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}│ {Fore.WHITE}2. Run Without Proxy{Fore.LIGHTCYAN_EX}             │{Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}└──────────────────────────────────────────────┘{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}  Select an option [1/2] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2]:
                    proxy_type = (
                        "Private Proxy" if choose == 1 else 
                        "No Proxy"
                    )
                    self.log(f"{Fore.GREEN + Style.BRIGHT}Running with: {proxy_type}{Style.RESET_ALL}")
                    break
                else:
                    self.log(f"{Fore.RED + Style.BRIGHT}Invalid input. Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                self.log(f"{Fore.RED + Style.BRIGHT}Invalid input. Please enter a number (1 or 2).{Style.RESET_ALL}")

        rotate = False
        if choose == 1: # Only ask for rotation if private proxy is selected
            while True:
                rotate_input = input(f"{Fore.BLUE + Style.BRIGHT}  Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip().lower()

                if rotate_input in ["y", "n"]:
                    rotate = rotate_input == "y"
                    break
                else:
                    self.log(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, proxy=None):
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url="https://api.ipify.org?format=json", ssl=False) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Failed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
    
    async def init(self, address: str, proxy=None, retries=5):
        url = f"{self.PRIVY_API}/api/v1/siwe/init"
        data = json.dumps({"address":address})
        headers = {
            **self.PRIVY_HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Get Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def authenticate(self, account: str, address: str, nonce: str, proxy=None, retries=5):
        url = f"{self.PRIVY_API}/api/v1/siwe/authenticate"
        data = json.dumps(self.generate_payload(account, address, nonce))
        headers = {
            **self.PRIVY_HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def user_data(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/tokens/user/me"
        headers = {
            **self.BASE_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Balance :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Fetch Balance {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def send_checkin_activity(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/tokens/activity"
        data = json.dumps({
            "activityType":"LOGIN",
            "metadata":{
                "action":"user_login",
                "timestamp":datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            }
        })
        headers = {
            **self.BASE_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Send Activity Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def send_game_activity(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/tokens/activity"
        data = json.dumps({
            "activityType":"GAME_PLAY",
            "metadata":{
                "action":"user_game",
                "timestamp":datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            }
        })
        headers = {
            **self.BASE_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Games   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Send Activity Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def agent_threads(self, address: str, proxy=None, retries=5):
        url = f"{self.AGENTS_API}/threads"
        data = json.dumps({"metadata":{}})
        headers = {
            **self.AGENTS_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Agent Init Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None

    async def run_stream(self, address: str, thread_id: str, message: str, proxy=None, retries=5):
        url = f"{self.AGENTS_API}/threads/{thread_id}/runs/stream"
        data = json.dumps(self.generate_stream_payload(message))
        headers = {
            **self.AGENTS_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }

        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        result = ""

                        async for line in response.content:
                            line = line.decode("utf-8").strip()

                            if not line or line.startswith(":"):
                                continue

                            if line.startswith("data: "):
                                try:
                                    json_data = json.loads(line[6:])
                                    messages = json_data.get("messages", [])
                                    for msg in messages:
                                        if msg.get("type") == "ai":
                                            result += msg.get("content", "")
                                except json.JSONDecodeError:
                                    continue
                        
                        return result if result else None

            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Agent didn't Respond {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def send_chat_activity(self, address: str, msg_length: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/tokens/activity"
        data = json.dumps({
            "activityType":"CHAT_INTERACTION",
            "metadata":{
                "action":"user_chat",
                "message_length":msg_length,
                "timestamp":datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            }
        })
        headers = {
            **self.BASE_HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Send Activity Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
            
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy and self.proxies else None # Check if proxies exist
            display_proxy = proxy if proxy else "None"
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {display_proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if not is_valid:
                if rotate_proxy and use_proxy and self.proxies: # Only rotate if proxy is in use AND proxies are available
                    proxy = self.rotate_proxy_for_account(address)
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}Rotating proxy for {self.mask_account(address)}...{Style.RESET_ALL}")
                    await asyncio.sleep(5)
                    continue
                elif use_proxy and not self.proxies: # If using proxy but no proxies loaded
                    self.log(f"{Fore.RED + Style.BRIGHT}No proxies available, proceeding without proxy.{Style.RESET_ALL}")
                    return True # Proceed as if no proxy was chosen
                else: # If not using proxy or no more proxies to rotate
                    return False
            
            return True

    async def process_user_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            init = await self.init(address, proxy)
            if init:
                nonce = init["nonce"]

                login = await self.authenticate(account, address, nonce, proxy)
                if login:
                    self.access_tokens[address] = login["token"]

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Login Success {Style.RESET_ALL}"
                    )
                    return True

        return False

    async def process_accounts(self, account: str, address: str, questions: list, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_user_login(account, address, use_proxy, rotate_proxy)
        if logined:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            user = await self.user_data(address, proxy)
            if user:
                balance = user.get("token", {}).get("pointsTotal", 0)

                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Balance :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {balance} PUMPs {Style.RESET_ALL}"
                )

            checkin = await self.send_checkin_activity(address, proxy)
            if checkin:
                activity_id = checkin.get("activityId", None)

                if activity_id:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Send Activity Success {Style.RESET_ALL}"
                    )
                else:
                    message = checkin.get("message", "Unknown Status")
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {message} {Style.RESET_ALL}"
                    )

            games = await self.send_game_activity(address, proxy)
            if games:
                activity_id = games.get("activityId", None)
                if activity_id:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Games   :{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Send Activity Success {Style.RESET_ALL}"
                    )
                else:
                    message = games.get("message", "Unknown Status")
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Games   :{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {message} {Style.RESET_ALL}"
                    )

            self.log(f"{Fore.CYAN + Style.BRIGHT}AI Chat :{Style.RESET_ALL}")

            chat_success = False
            for _ in range(3): # Try chat interaction a few times
                thread = await self.agent_threads(address, proxy)
                if thread:
                    thread_id = thread.get("thread_id")
                    message = random.choice(questions)
                    msg_length = int(len(message))

                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}Question:{Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT} {message} {Style.RESET_ALL}"
                    )

                    response = await self.run_stream(address, thread_id, message, proxy)
                    if response:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                            f"{Fore.CYAN+Style.BRIGHT}Response:{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {response} {Style.RESET_ALL}"
                        )

                        submit = await self.send_chat_activity(address, msg_length, proxy)
                        if submit:
                            activity_id = submit.get("activityId", None)
                            if activity_id:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Send Activity Success {Style.RESET_ALL}"
                                )
                                chat_success = True
                                break # Break from retry loop if successful
                            else:
                                message = submit.get("message", "Unknown Status")
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} {message} {Style.RESET_ALL}"
                                )
                if not chat_success:
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}Retrying AI Chat...{Style.RESET_ALL}")
                    await asyncio.sleep(5) # Small delay before retrying chat

            if not chat_success:
                self.log(f"{Fore.RED + Style.BRIGHT}Failed to complete AI Chat activity after multiple attempts.{Style.RESET_ALL}")
                    
    async def main(self):
        init(autoreset=True) # Initialize colorama to reset colors after each print

        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            
            self.welcome() # Display welcome message at the start
            
            use_proxy_choice_raw, rotate_proxy = self.print_question()
            use_proxy = (use_proxy_choice_raw == 1) # True if private proxy is selected

            questions = self.load_question_lists()
            if not questions:
                self.log(f"{Fore.RED + Style.BRIGHT}No Questions Loaded. Please check 'question_lists.json'.{Style.RESET_ALL}")
                return

            if use_proxy:
                await self.load_proxies(use_proxy_choice_raw) # load_proxies will handle if no proxies found
                if not self.proxies and use_proxy_choice_raw == 1:
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}Warning: Private proxy selected, but no proxies found in proxy.txt. Running without proxy.{Style.RESET_ALL}")
                    use_proxy = False # Force to run without proxy if no proxies are found

            while True:
                self.clear_terminal() # Clear terminal for each full cycle
                self.welcome() # Re-display welcome header for each cycle
                self.log(f"{Fore.GREEN + Style.BRIGHT}Total Accounts: {Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}")
                self.log(f"{Fore.GREEN + Style.BRIGHT}Proxy Rotation: {Fore.WHITE + Style.BRIGHT}{'Enabled' if rotate_proxy and use_proxy else 'Disabled'}{Style.RESET_ALL}\n")

                for account in accounts:
                    if account:
                        address = self.generate_address(account)
                        
                        self.log(f"{Fore.CYAN + Style.BRIGHT}───────────────────────────────────────────────────{Style.RESET_ALL}")
                        self.log(f"{Fore.CYAN + Style.BRIGHT}Processing Account: {Fore.WHITE + Style.BRIGHT}{self.mask_account(address)}{Style.RESET_ALL}")
                        self.log(f"{Fore.CYAN + Style.BRIGHT}───────────────────────────────────────────────────{Style.RESET_ALL}")


                        if not address:
                            self.log(
                                f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            self.log(f"{Fore.CYAN + Style.BRIGHT}───────────────────────────────────────────────────{Style.RESET_ALL}\n")
                            continue

                        user_agent = random.choice(USER_AGENT)

                        self.PRIVY_HEADERS[address] = {
                            "Accept": "application/json",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Origin": "https://app.wardenprotocol.org",
                            "Privy-App-Id": "cm7f00k5c02tibel0m4o9tdy1",
                            "Privy-Ca-Id": str(uuid.uuid4()),
                            "Privy-Client": "react-auth:2.13.8",
                            "Referer": "https://app.wardenprotocol.org/", # Corrected typo "Refrer" to "Referer"
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "Sec-Fetch-Storage-Access": "active",
                            "User-Agent": user_agent
                        }

                        self.BASE_HEADERS[address] = {
                            "Accept": "*/*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Origin": "https://app.wardenprotocol.org",
                            "Referer": "https://app.wardenprotocol.org/", # Corrected typo "Refrer" to "Referer"
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-site",
                            "User-Agent": user_agent
                        }

                        self.AGENTS_HEADERS[address] = {
                            "Accept": "*/*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Origin": "https://app.wardenprotocol.org",
                            "Referer": "https://app.wardenprotocol.org/", # Corrected typo "Refrer" to "Referer"
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "User-Agent": user_agent,
                            "X-Api-Key": "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"
                        }

                        await self.process_accounts(account, address, questions, use_proxy, rotate_proxy)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}───────────────────────────────────────────────────{Style.RESET_ALL}\n")
                        await asyncio.sleep(5) # Small delay between accounts

                self.log(f"{Fore.GREEN + Style.BRIGHT}All accounts processed. Waiting for next cycle...{Style.RESET_ALL}")
                seconds = 24 * 60 * 60 # 24 hours
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Next cycle in{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}Press CTRL+C to exit.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1
                self.log(f"\n{Fore.GREEN + Style.BRIGHT}Starting next cycle...{Style.RESET_ALL}") # New line after countdown

        except FileNotFoundError:
            self.log(f"{Fore.RED}Error: 'accounts.txt' file not found. Please create this file with your private keys.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    init(autoreset=True) # Initialize colorama to reset colors

    try:
        bot = Warden()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"\n{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Warden Protocol Bot Terminated.{Style.RESET_ALL}                                       "                              
        )
    except Exception as e:
        print(
            f"\n{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}An error occurred outside main: {e}{Style.RESET_ALL}                                       "                              
        )