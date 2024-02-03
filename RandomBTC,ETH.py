import requests
import logging
from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH
from colorama import init, Fore
from hdwallet.utils import generate_mnemonic
import time

# Initialisierung von Colorama
init()

# Bitcoin API-Endpunkte
BTC_API_ENDPOINTS = [
    "https://btc4.trezor.io/api/v2/address/",
    "https://blockstream.info/api/address/",
]

# Ethereum API-Endpunkte
ETH_API_ENDPOINTS = [
    "https://eth1.trezor.io/api/v2/address/",
    "https://api.etherscan.io/api?module=account&action=balance&tag=latest&address=",
]

# API-Überprüfungsfunktion
def check_apis(api_endpoints, symbol):
    working_apis = []
    for endpoint in api_endpoints:
        try:
            # Verwende eine bekannte Adresse für den Test
            test_address = "1BoatSLRHtKNngkdXEeobR76b53LETtpyT" if symbol == BTC else "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
            url = f"{endpoint}{test_address}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                print(Fore.GREEN + f"API {endpoint} funktioniert." + Fore.RESET)
                working_apis.append(endpoint)
            else:
                print(Fore.RED + f"API {endpoint} hat mit Statuscode {response.status_code} geantwortet." + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"Fehler bei der Überprüfung der API {endpoint}: {e}" + Fore.RESET)
    return working_apis

# Saldoabfragefunktion
def get_balance(address, apis, symbol):
    for endpoint in apis:
        try:
            url = f"{endpoint}{address}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                data = response.json()
                if symbol == BTC:
                    balance = int(data.get('balance', 0)) / 100000000
                elif symbol == ETH:
                    balance = int(data.get('balance', 0)) / 1000000000000000000  # Umrechnung von Wei zu Ether
                return balance
        except Exception as e:
            logging.error(Fore.RED + f"Fehler bei der API-Anfrage an {endpoint}: {e}" + Fore.RESET)
    return None

# Funktion zum Speichern von Guthaben und Seed in einer Datei
def save_balance_and_seed(seed, address, balance):
    with open("Balance.txt", "a") as file:
        file.write(f"Seed: {seed}, Address: {address}, Balance: {balance}\n")

# Funktion zum Überprüfen des Internetstatus
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        print(Fore.CYAN + "Internetverbindung vorhanden." + Fore.RESET)
    except requests.ConnectionError:
        print(Fore.RED + "Keine Internetverbindung." + Fore.RESET)

# Hauptfunktion
def main():
    working_apis_btc = check_apis(BTC_API_ENDPOINTS, BTC)
    working_apis_eth = check_apis(ETH_API_ENDPOINTS, ETH)

    if not (working_apis_btc or working_apis_eth):
        print(Fore.RED + "Keine APIs sind derzeit verfügbar." + Fore.RESET)
        return

    counter = 0  # Zähler für generierte Wallets

    while True:
        try:
            mnemonic = generate_mnemonic(language="english", strength=128)
            print(Fore.MAGENTA + f"Mnemonic-Phrase: {mnemonic}" + Fore.RESET)

            # Bitcoin Wallet
            hd_wallet_btc = HDWallet(symbol=BTC)
            hd_wallet_btc.from_mnemonic(mnemonic=mnemonic)
            btc_address = hd_wallet_btc.p2pkh_address()
            btc_balance = get_balance(btc_address, working_apis_btc, BTC)
            print(Fore.YELLOW + f"Bitcoin Address: {btc_address} - Balance: {btc_balance if btc_balance is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)

            # Ethereum Wallet
            hd_wallet_eth = HDWallet(symbol=ETH)
            hd_wallet_eth.from_mnemonic(mnemonic=mnemonic)
            eth_address = hd_wallet_eth.p2pkh_address()
            eth_balance = get_balance(eth_address, working_apis_eth, ETH)
            print(Fore.BLUE + f"Ethereum Address: {eth_address} - Balance: {eth_balance if eth_balance is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)

            # Überprüfen Sie den Internetstatus
            check_internet()

            # Speichern Sie Guthaben und Seed, wenn Guthaben gefunden wurde
            if btc_balance is not None and btc_balance > 0:
                save_balance_and_seed(mnemonic, btc_address, btc_balance)
            if eth_balance is not None and eth_balance > 0:
                save_balance_and_seed(mnemonic, eth_address, eth_balance)

            counter += 1
            print(Fore.CYAN + f"Anzahl generierter Wallets: {counter}" + Fore.RESET)

            # Eine Pause hinzufügen, um die Ausgabe zu sehen
            time.sleep(0.1)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "Programm wurde manuell beendet." + Fore.RESET)
            break
        except Exception as e:
            logging.error(Fore.RED + f"Unerwarteter Fehler im Hauptprogramm: {e}" + Fore.RESET)

if __name__ == "__main__":
    main()
