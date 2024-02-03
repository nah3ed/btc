import requests
from mnemonic import Mnemonic
from web3 import Web3
from eth_account import Account
from hdwallet import HDWallet
from hdwallet.symbols import ETH
from colorama import init, Fore
import time

# Colorama-Initialisierung
init()

Account.enable_unaudited_hdwallet_features()  # Enable Mnemonic features

mnemo = Mnemonic("english")

# Ethereum API-Endpunkte
ETH_API_ENDPOINTS = [
    "https://eth1.trezor.io/api/v2/address/",
    "https://api.etherscan.io/api?module=account&action=balance&tag=latest&address=",
    "https://api.mycryptoapi.com/eth",
    "https://api.covalenthq.com/v1/1/address/",
    "https://api.blockcypher.com/v1/eth/main/addrs/",
    "https://api.blockchair.com/ethereum/dashboards/address/",
    # Füge hier weitere ETH-API-Endpunkte hinzu, falls gewünscht
]

# API-Überprüfungsfunktion
def check_apis(api_endpoints, symbol):
    working_apis = []
    for endpoint in api_endpoints:
        try:
            # Verwende eine bekannte Adresse für den Test
            test_address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
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
                if symbol == "ETH":
                    balance = int(data.get('balance', 0)) / 10**18  # Umrechnung von Wei zu Ether
                    return balance
        except Exception as e:
            print(Fore.RED + f"Fehler bei der API-Anfrage an {endpoint}: {e}" + Fore.RESET)
    return None

# Funktion zum Speichern von Guthaben, Adresse und Seed in einer Datei
def save_balance_and_seed(number, mnemonic, address, balance):
    with open("Balance.txt", "a", encoding="utf-8") as file:
        formatted_balance = "{:.18f}".format(balance)  # Anzahl der Dezimalstellen anpassen
        file.write(f"Number: {number}, Mnemonic: {mnemonic}, Address: {address}, Balance: {formatted_balance}\n")

# Funktion zum Überprüfen des Internetstatus
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        print(Fore.CYAN + "Abfrage i.O." + Fore.RESET)
    except requests.ConnectionError:
        print(Fore.RED + "Keine Internetverbindung." + Fore.RESET)

# Hauptfunktion
def main():
    working_apis_eth = check_apis(ETH_API_ENDPOINTS, "ETH")

    if not working_apis_eth:
        print(Fore.RED + "Keine APIs sind derzeit verfügbar." + Fore.RESET)
        return

    counter = 0  # Zähler für generierter Wallets

    try:
        # Lese die Seeds aus der TXT-Datei (Mnemonics)
        with open("input.txt", "r", encoding="ISO-8859-1") as mnemonic_file:
            mnemonics = mnemonic_file.readlines()

        for number, mnemonic in enumerate(mnemonics, start=1):
            mnemonic = mnemonic.strip()  # Entferne Leerzeichen und Zeilenumbrüche
            if not mnemonic:
                continue  # Ignoriere leere Zeilen

            try:
                # Generate seed from mnemonic
                seed = mnemo.to_seed(mnemonic)

                # Derive Ethereum private key from mnemonic
                account = Account.from_mnemonic(mnemonic)
                private_key = account._key_obj._raw_key.hex()

                # Get Ethereum address from private key
                address = Account.from_key(private_key).address

                print(Fore.MAGENTA + f"Nummer: {number}, Mnemonic: {mnemonic}, Aktuelle Adresse: {address}" + Fore.RESET)

                # Ethereum Wallet
                eth_balance = get_balance(address, working_apis_eth, "ETH")
                print(Fore.BLUE + f"Ethereum Address: {address} - Balance: {eth_balance if eth_balance is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)

                # Überprüfen Sie den Internetstatus
                check_internet()

                # Speichern Sie Guthaben, Adresse und Mnemonic, wenn Guthaben gefunden wurde
                if eth_balance is not None and eth_balance > 0:
                    save_balance_and_seed(number, mnemonic, address, eth_balance)

                counter += 1
                print(Fore.CYAN + f"Anzahl generierter Adressen: {counter}" + Fore.RESET)

                # Eine Pause hinzufügen, um die Ausgabe zu sehen
                time.sleep(0.01)

            except KeyboardInterrupt:
                print(Fore.YELLOW + "Programm wurde manuell beendet." + Fore.RESET)
                break
            except Exception as e:
                print(Fore.RED + f"Unerwarteter Fehler im Hauptprogramm: {e}" + Fore.RESET)

    except FileNotFoundError:
        print(Fore.RED + "Die Datei 'WEAK_mnemonics.txt' wurde nicht gefunden." + Fore.RESET)

if __name__ == "__main__":
    main()

