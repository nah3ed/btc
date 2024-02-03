from bloomfilter import BloomFilter
import time
from colorama import Fore, Style

try:
    with open('btc.bf', "rb") as fp:
        addfind = BloomFilter.load(fp)
except FileNotFoundError:
    print("Bloom filter file 'btc.bf' not found.")
    exit(1)

def notify_and_log(wallet):
    with open('found_wallets.txt', 'a') as result:
        result.write(wallet + '\n')

def check_wallet(address):
    if address in addfind:
        notify_and_log(address)
        print(f"{Fore.GREEN}FOUND WALLET!!! - {address}{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        with open('btc.txt') as file:
            addresses_to_check = file.read().split()

        total_wallets = len(addresses_to_check)
        checked_wallets = 0
        start_time = time.time()

        for address in addresses_to_check:
            check_wallet(address)
            checked_wallets += 1

            elapsed_time = time.time() - start_time
            wallets_per_second = checked_wallets / elapsed_time if elapsed_time > 0 else 0
            remaining_seconds = (total_wallets - checked_wallets) / wallets_per_second if wallets_per_second > 0 else 0
            
            remaining_hours = int(remaining_seconds // 3600)
            remaining_minutes = int((remaining_seconds % 3600) // 60)
            remaining_seconds = int(remaining_seconds % 60)

            print(f"{Fore.CYAN}Progress: {Fore.WHITE}{checked_wallets:,}/{total_wallets:,} {Fore.CYAN}wallets"
                f" {Fore.WHITE}| {wallets_per_second:,.2f} {Fore.CYAN}wallets/sec"
                f" {Fore.WHITE}| {Fore.CYAN}Time Remaining: {Fore.WHITE}{remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}{Style.RESET_ALL} ")

    except FileNotFoundError:
        print(f"{Fore.RED}BTC.txt file not found.{Style.RESET_ALL}")
