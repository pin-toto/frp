#!/usr/bin/env python3

import asyncio
import random
import ipaddress
import argparse
import time
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

init(autoreset=True)

COLORS = {
    'red': Fore.RED,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
    'blue': Fore.BLUE,
    'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN,
    'white': Fore.WHITE,
    'reset': Style.RESET_ALL,
    'bold': Style.BRIGHT
}

COUNTRY_RANGES = {
    'iran': ['31.7.64.0/19', '46.36.80.0/20', '46.209.0.0/16', '51.143.0.0/17', '78.38.0.0/15', 
             '80.191.0.0/16', '81.12.0.0/16', '81.91.128.0/19', '82.99.128.0/17', '83.120.0.0/16',
             '84.241.0.0/17', '85.9.64.0/18', '85.15.0.0/16', '85.133.128.0/17', '85.185.0.0/16',
             '86.55.0.0/16', '87.107.0.0/16', '88.135.0.0/16', '89.144.128.0/17', '90.156.0.0/16',
             '91.98.0.0/15', '91.104.0.0/16', '91.106.0.0/16', '91.107.128.0/17', '92.42.48.0/20',
             '92.50.0.0/16', '92.242.0.0/16', '93.110.0.0/16', '94.101.128.0/18', '95.38.0.0/16',
             '95.82.0.0/16', '95.162.0.0/16', '109.108.160.0/19', '109.122.192.0/18', '109.125.128.0/17',
             '109.162.0.0/16', '109.201.0.0/16', '109.203.128.0/18', '109.225.128.0/17', '128.65.224.0/19',
             '130.185.0.0/16', '130.255.192.0/18', '131.116.0.0/15', '132.159.0.0/16', '134.141.0.0/16',
             '137.96.0.0/16', '142.4.188.0/22', '144.128.0.0/16', '145.12.224.0/19', '145.255.128.0/17',
             '146.19.212.0/22', '146.104.0.0/16', '147.128.0.0/16', '149.102.128.0/17', '149.242.0.0/16',
             '151.232.0.0/16', '151.240.0.0/15', '152.89.192.0/18', '155.94.128.0/17', '156.209.0.0/16',
             '157.55.0.0/16', '158.58.0.0/16', '159.20.0.0/16', '160.77.0.0/16', '161.16.0.0/16',
             '162.251.0.0/16', '164.138.0.0/16', '165.87.0.0/16', '167.243.0.0/16', '168.205.0.0/16',
             '169.239.0.0/16', '171.22.0.0/16', '172.17.0.0/16', '173.213.0.0/16', '174.140.0.0/16',
             '176.221.0.0/16', '176.236.0.0/16', '177.248.0.0/16', '178.131.0.0/16', '178.173.0.0/16',
             '178.248.0.0/16', '178.252.0.0/16', '179.156.0.0/16', '180.150.0.0/16', '181.45.0.0/16',
             '182.18.0.0/16', '182.142.0.0/16', '183.88.0.0/16', '184.149.0.0/16', '185.35.0.0/16',
             '185.70.0.0/16', '185.96.0.0/16', '185.105.0.0/16', '185.120.0.0/16', '185.147.0.0/16',
             '185.215.0.0/16', '185.230.0.0/16', '188.0.0.0/16', '188.95.0.0/16', '188.121.0.0/16',
             '188.210.0.0/16', '188.229.0.0/16', '188.245.0.0/16', '192.15.0.0/16', '193.108.0.0/16',
             '194.110.0.0/16', '195.146.0.0/16', '195.191.0.0/16', '196.200.0.0/16', '199.191.0.0/16',
             '212.16.0.0/16', '212.33.0.0/16', '212.50.0.0/16', '212.80.0.0/16', '212.110.0.0/16',
             '212.115.0.0/16', '212.120.0.0/16', '213.108.0.0/16', '213.144.0.0/16', '213.176.0.0/16',
             '213.217.0.0/16', '213.233.0.0/16', '217.146.0.0/16', '217.174.0.0/16', '217.218.0.0/16'],
    'us': ['8.0.0.0/8', '12.0.0.0/8', '13.0.0.0/8', '15.0.0.0/8', '16.0.0.0/8', '17.0.0.0/8',
           '18.0.0.0/8', '19.0.0.0/8', '20.0.0.0/8', '21.0.0.0/8', '22.0.0.0/8', '23.0.0.0/8',
           '24.0.0.0/8', '25.0.0.0/8', '26.0.0.0/8', '27.0.0.0/8', '28.0.0.0/8', '29.0.0.0/8',
           '30.0.0.0/8', '31.0.0.0/8', '32.0.0.0/8', '33.0.0.0/8', '34.0.0.0/8', '35.0.0.0/8',
           '36.0.0.0/8', '37.0.0.0/8', '38.0.0.0/8', '39.0.0.0/8', '40.0.0.0/8', '41.0.0.0/8',
           '42.0.0.0/8', '43.0.0.0/8', '44.0.0.0/8', '45.0.0.0/8', '46.0.0.0/8', '47.0.0.0/8',
           '48.0.0.0/8', '49.0.0.0/8', '50.0.0.0/8', '51.0.0.0/8', '52.0.0.0/8', '53.0.0.0/8',
           '54.0.0.0/8', '55.0.0.0/8', '56.0.0.0/8', '57.0.0.0/8', '58.0.0.0/8', '59.0.0.0/8',
           '60.0.0.0/8', '61.0.0.0/8', '62.0.0.0/8', '63.0.0.0/8', '64.0.0.0/8', '65.0.0.0/8',
           '66.0.0.0/8', '67.0.0.0/8', '68.0.0.0/8', '69.0.0.0/8', '70.0.0.0/8', '71.0.0.0/8',
           '72.0.0.0/8', '73.0.0.0/8', '74.0.0.0/8', '75.0.0.0/8', '76.0.0.0/8', '77.0.0.0/8',
           '78.0.0.0/8', '79.0.0.0/8', '80.0.0.0/8', '81.0.0.0/8', '82.0.0.0/8', '83.0.0.0/8',
           '84.0.0.0/8', '85.0.0.0/8', '86.0.0.0/8', '87.0.0.0/8', '88.0.0.0/8', '89.0.0.0/8',
           '90.0.0.0/8', '91.0.0.0/8', '92.0.0.0/8', '93.0.0.0/8', '94.0.0.0/8', '95.0.0.0/8',
           '96.0.0.0/8', '97.0.0.0/8', '98.0.0.0/8', '99.0.0.0/8', '100.0.0.0/8', '101.0.0.0/8',
           '102.0.0.0/8', '103.0.0.0/8', '104.0.0.0/8', '105.0.0.0/8', '106.0.0.0/8', '107.0.0.0/8',
           '108.0.0.0/8', '109.0.0.0/8', '110.0.0.0/8', '111.0.0.0/8', '112.0.0.0/8', '113.0.0.0/8',
           '114.0.0.0/8', '115.0.0.0/8', '116.0.0.0/8', '117.0.0.0/8', '118.0.0.0/8', '119.0.0.0/8',
           '120.0.0.0/8', '121.0.0.0/8', '122.0.0.0/8', '123.0.0.0/8', '124.0.0.0/8', '125.0.0.0/8',
           '126.0.0.0/8', '127.0.0.0/8', '128.0.0.0/8', '129.0.0.0/8', '130.0.0.0/8', '131.0.0.0/8',
           '132.0.0.0/8', '133.0.0.0/8', '134.0.0.0/8', '135.0.0.0/8', '136.0.0.0/8', '137.0.0.0/8',
           '138.0.0.0/8', '139.0.0.0/8', '140.0.0.0/8', '141.0.0.0/8', '142.0.0.0/8', '143.0.0.0/8',
           '144.0.0.0/8', '145.0.0.0/8', '146.0.0.0/8', '147.0.0.0/8', '148.0.0.0/8', '149.0.0.0/8',
           '150.0.0.0/8', '151.0.0.0/8', '152.0.0.0/8', '153.0.0.0/8', '154.0.0.0/8', '155.0.0.0/8',
           '156.0.0.0/8', '157.0.0.0/8', '158.0.0.0/8', '159.0.0.0/8', '160.0.0.0/8', '161.0.0.0/8',
           '162.0.0.0/8', '163.0.0.0/8', '164.0.0.0/8', '165.0.0.0/8', '166.0.0.0/8', '167.0.0.0/8',
           '168.0.0.0/8', '169.0.0.0/8', '170.0.0.0/8', '171.0.0.0/8', '172.0.0.0/8', '173.0.0.0/8',
           '174.0.0.0/8', '175.0.0.0/8', '176.0.0.0/8', '177.0.0.0/8', '178.0.0.0/8', '179.0.0.0/8',
           '180.0.0.0/8', '181.0.0.0/8', '182.0.0.0/8', '183.0.0.0/8', '184.0.0.0/8', '185.0.0.0/8',
           '186.0.0.0/8', '187.0.0.0/8', '188.0.0.0/8', '189.0.0.0/8', '190.0.0.0/8', '191.0.0.0/8',
           '192.0.0.0/8', '193.0.0.0/8', '194.0.0.0/8', '195.0.0.0/8', '196.0.0.0/8', '197.0.0.0/8',
           '198.0.0.0/8', '199.0.0.0/8', '200.0.0.0/8', '201.0.0.0/8', '202.0.0.0/8', '203.0.0.0/8',
           '204.0.0.0/8', '205.0.0.0/8', '206.0.0.0/8', '207.0.0.0/8', '208.0.0.0/8', '209.0.0.0/8',
           '210.0.0.0/8', '211.0.0.0/8', '212.0.0.0/8', '213.0.0.0/8', '214.0.0.0/8', '215.0.0.0/8',
           '216.0.0.0/8', '217.0.0.0/8', '218.0.0.0/8', '219.0.0.0/8', '220.0.0.0/8', '221.0.0.0/8',
           '222.0.0.0/8', '223.0.0.0/8', '224.0.0.0/8', '225.0.0.0/8', '226.0.0.0/8', '227.0.0.0/8',
           '228.0.0.0/8', '229.0.0.0/8', '230.0.0.0/8', '231.0.0.0/8', '232.0.0.0/8', '233.0.0.0/8',
           '234.0.0.0/8', '235.0.0.0/8', '236.0.0.0/8', '237.0.0.0/8', '238.0.0.0/8', '239.0.0.0/8'],
    'china': ['1.0.0.0/8', '14.0.0.0/8', '27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8', '42.0.0.0/8',
              '49.0.0.0/8', '58.0.0.0/8', '59.0.0.0/8', '60.0.0.0/8', '61.0.0.0/8', '101.0.0.0/8',
              '106.0.0.0/8', '110.0.0.0/8', '111.0.0.0/8', '112.0.0.0/8', '113.0.0.0/8', '114.0.0.0/8',
              '115.0.0.0/8', '116.0.0.0/8', '117.0.0.0/8', '118.0.0.0/8', '119.0.0.0/8', '120.0.0.0/8',
              '121.0.0.0/8', '122.0.0.0/8', '123.0.0.0/8', '124.0.0.0/8', '125.0.0.0/8', '126.0.0.0/8',
              '139.0.0.0/8', '140.0.0.0/8', '144.0.0.0/8', '146.0.0.0/8', '150.0.0.0/8', '152.0.0.0/8',
              '153.0.0.0/8', '156.0.0.0/8', '157.0.0.0/8', '158.0.0.0/8', '159.0.0.0/8', '160.0.0.0/8',
              '161.0.0.0/8', '162.0.0.0/8', '163.0.0.0/8', '164.0.0.0/8', '165.0.0.0/8', '166.0.0.0/8',
              '167.0.0.0/8', '168.0.0.0/8', '169.0.0.0/8', '170.0.0.0/8', '171.0.0.0/8', '172.0.0.0/8',
              '173.0.0.0/8', '174.0.0.0/8', '175.0.0.0/8', '176.0.0.0/8', '177.0.0.0/8', '178.0.0.0/8',
              '179.0.0.0/8', '180.0.0.0/8', '181.0.0.0/8', '182.0.0.0/8', '183.0.0.0/8', '184.0.0.0/8',
              '185.0.0.0/8', '186.0.0.0/8', '187.0.0.0/8', '188.0.0.0/8', '189.0.0.0/8', '190.0.0.0/8',
              '191.0.0.0/8', '192.0.0.0/8', '193.0.0.0/8', '194.0.0.0/8', '195.0.0.0/8', '196.0.0.0/8',
              '197.0.0.0/8', '198.0.0.0/8', '199.0.0.0/8', '200.0.0.0/8', '201.0.0.0/8', '202.0.0.0/8',
              '203.0.0.0/8', '204.0.0.0/8', '205.0.0.0/8', '206.0.0.0/8', '207.0.0.0/8', '208.0.0.0/8',
              '209.0.0.0/8', '210.0.0.0/8', '211.0.0.0/8', '212.0.0.0/8', '213.0.0.0/8', '214.0.0.0/8',
              '215.0.0.0/8', '216.0.0.0/8', '217.0.0.0/8', '218.0.0.0/8', '219.0.0.0/8', '220.0.0.0/8',
              '221.0.0.0/8', '222.0.0.0/8', '223.0.0.0/8']
}

class FastScanner:
    def __init__(self):
        self.results = []
        self.lock = asyncio.Lock()
        self.semaphore = None
        self.ports = []
        self.os_filter = None
        self.save_file = None
        self.executor = ThreadPoolExecutor(max_workers=200)

    def random_ip(self):
        return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    def get_country_ips(self, country):
        if country not in COUNTRY_RANGES:
            return None
        ip_list = []
        for cidr in COUNTRY_RANGES[country]:
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                for ip in network.hosts():
                    ip_list.append(str(ip))
                    if len(ip_list) > 500000:
                        break
                if len(ip_list) > 500000:
                    break
            except:
                continue
        return ip_list

    def check_port(self, ip, port, timeout=0.2):
        try:
            with socket.create_connection((ip, port), timeout=timeout) as sock:
                return True
        except:
            return False

    def get_os_from_ttl(self, ip):
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                output = result.stdout.lower()
                if 'ttl=64' in output or 'ttl=128' in output:
                    return 'linux'
                elif 'ttl=128' in output:
                    return 'windows'
            return 'unknown'
        except:
            return 'unknown'

    async def scan_port(self, ip, port):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, self.check_port, ip, port)
        return result

    async def scan_ip(self, ip):
        open_ports = []
        for port in self.ports:
            if await self.scan_port(ip, port):
                open_ports.append(port)
        
        if open_ports:
            os_type = 'unknown'
            if self.os_filter:
                os_type = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.get_os_from_ttl, ip
                )
                if os_type != self.os_filter:
                    return
            
            async with self.lock:
                self.results.append({'ip': ip, 'ports': open_ports, 'os': os_type})
                if len(open_ports) == 1:
                    print(f"{COLORS['green']}Found: {ip} - Port: {open_ports[0]} ({os_type})")
                else:
                    print(f"{COLORS['green']}Found: {ip} - Ports: {', '.join(map(str, open_ports))} ({os_type})")

    async def scan_batch(self, ips):
        async with self.semaphore:
            tasks = [self.scan_ip(ip) for ip in ips]
            await asyncio.gather(*tasks)

    async def main(self):
        parser = argparse.ArgumentParser(description='FRP - Fast Random Port Scanner')
        parser.add_argument('-g', '--generate', type=int, required=True, help='Number of IPs to generate')
        parser.add_argument('-p', '--ports', type=str, required=True, help='Comma-separated ports to check')
        parser.add_argument('-f', '--filter-country', type=str, help='Filter by country (iran, us, china)')
        parser.add_argument('-fs', '--file-save', type=str, help='Save results to file')
        parser.add_argument('-o', '--os-filter', type=str, choices=['win', 'linux'], help='Filter by OS')
        parser.add_argument('-t', '--threads', type=int, default=500, help='Number of concurrent connections')
        
        args = parser.parse_args()
        self.ports = [int(p.strip()) for p in args.ports.split(',')]
        self.save_file = args.file_save
        self.os_filter = args.os_filter
        self.semaphore = asyncio.Semaphore(args.threads)
        print(f"{COLORS['cyan']}==================================================")
        print(f"{COLORS['magenta']}  FRP - Find Random Port ")
        print(f"{COLORS['cyan']}==================================================\n")

        print(f"{COLORS['yellow']}Generating {args.generate} IPs...")
        if args.filter_country:
            print(f"{COLORS['blue']}Filtering by country: {args.filter_country}")
            country_ips = self.get_country_ips(args.filter_country)
            if country_ips:
                ip_pool = random.sample(country_ips, min(args.generate, len(country_ips)))
            else:
                print(f"{COLORS['red']}Country not found, using random IPs")
                ip_pool = [self.random_ip() for _ in range(args.generate)]
        else:
            ip_pool = [self.random_ip() for _ in range(args.generate)]

        if self.os_filter:
            print(f"{COLORS['blue']}Filtering by OS: {self.os_filter}")

        print(f"{COLORS['yellow']}Checking ports: {', '.join(map(str, self.ports))}")
        print(f"{COLORS['yellow']}Using {args.threads} concurrent connections")
        print(f"{COLORS['cyan']}Scanning...\n")

        start_time = time.time()
        batch_size = 50
        for i in range(0, len(ip_pool), batch_size):
            batch = ip_pool[i:i+batch_size]
            await self.scan_batch(batch)
            progress = (i + len(batch)) / len(ip_pool) * 100
            sys.stdout.write(f"\r{COLORS['yellow']}Progress: {progress:.1f}% - Found: {len(self.results)}")
            sys.stdout.flush()

        print(f"\n\n{COLORS['cyan']}==================================================")
        print(f"{COLORS['green']}Scan complete! Time: {time.time() - start_time:.2f}s")
        print(f"{COLORS['green']}Found {len(self.results)} open ports.")
        print(f"{COLORS['cyan']}==================================================\n")

        if self.save_file:
            with open(self.save_file, 'w') as f:
                for r in self.results:
                    f.write(f"{r['ip']}:{','.join(map(str, r['ports']))} ({r['os']})\n")
            print(f"{COLORS['green']}Results saved to {self.save_file}")

        if self.results and not self.save_file:
            print(f"{COLORS['white']}IPs found:")
            for r in self.results:
                if r['os'] == 'linux':
                    os_color = COLORS['blue']
                elif r['os'] == 'windows':
                    os_color = COLORS['cyan']
                else:
                    os_color = COLORS['white']
                print(f"  {os_color}{r['ip']} {COLORS['yellow']}Ports: {COLORS['green']}{', '.join(map(str, r['ports']))} {COLORS['white']}({r['os']})")

if __name__ == "__main__":
    scanner = FastScanner()
    asyncio.run(scanner.main())
