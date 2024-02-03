import os
import random
import requests
import colorama
from colorama import Fore, Style
from mnemonic import Mnemonic
from bip_utils import Bip44, Bip44Coins

colorama.init()  # Inițializează colorama

# Lista limbilor
languages = ["english", "japanese", "korean", "spanish", "chinese_simplified", "chinese_traditional", "french", "italian", "czech", "portuguese"]

def get_address_balance(address):
    try:
        url = f"https://chain.api.btc.com/v3/address/{address}"
        response = requests.get(url)
        data = response.json()
        balance = data['data']['balance']
        return balance
        data = response.json()
        return data[address]['Total Received']
    except Exception as e:
        print(f"Eroare la obținerea balanței: {e}")
        return 0

def generate_modified_seed_and_address(original_phrase, lang):
    mnemo = Mnemonic(lang)
    words = original_phrase.split()
    random_index = random.randint(0, len(words) - 1)
    new_words = mnemo.wordlist  # Lista de cuvinte
    words[random_index] = random.choice(new_words)  # Înlocuiește un cuvânt aleatoriu
    new_phrase = ' '.join(words)
    seed = mnemo.to_seed(new_phrase)
    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    address = bip44_wallet.PublicKey().ToAddress()
    return new_phrase, address, seed

def process_seed(phrase, seed, address, output_file, status):
    balance = get_address_balance(address)
    seed_hex = seed.hex() if isinstance(seed, bytes) else seed
    output_str_console = f"{Fore.LIGHTGREEN_EX}Balance: {balance}{Style.RESET_ALL}, " \
                         f"{Fore.BLUE}Address: {address}{Style.RESET_ALL}, " \
                         f"{Fore.LIGHTYELLOW_EX}Phrase: {phrase}{Style.RESET_ALL}, " \
                         f"Status: {status}\n"

    output_str_file = f"Balance: {balance}, Address: {address}, Phrase: {phrase}, Seed: {seed_hex}, Status: {status}\n"
    output_file.write(output_str_file)
    print(output_str_console)

def main():
    max_recovery_seeds = 2

    with open("recovery_phrases.txt", "r", encoding='utf-8') as file, open("addresses_with_balances.txt", "w", encoding='utf-8') as output_file:
        for line in file:
            phrase = line.strip()
            if not phrase:
                continue
            print(f"Procesez fraza: {phrase}")

            phrase_valid = False
            for lang in languages:
                mnemo = Mnemonic(lang)
                if mnemo.check(phrase):
                    seed = mnemo.to_seed(phrase)
                    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
                    address = bip44_wallet.PublicKey().ToAddress()
                    process_seed(phrase, seed, address, output_file, "Seed valid")
                    phrase_valid = True
                    break
            
            if not phrase_valid:
                print("Fraza de recuperare este invalidă. Încerc să generez noi seed-uri.")
                recovery_seed_count = 0
                while recovery_seed_count < max_recovery_seeds:
                    new_phrase, new_address, new_seed = generate_modified_seed_and_address(phrase, lang)
                    process_seed(new_phrase, new_seed, new_address, output_file, "Seed generat pentru recuperare")
                    recovery_seed_count += 1

if __name__ == "__main__":
    main()


def get_balance_btc_com_v3(address):
    try:
        url = 'https://chain.api.btc.com/v3/address/' + address
        response = requests.get(url)
        data = response.json()
        return data['data']['final_balance'], data[address]['total_received']
    except Exception as e:
        print(f"Eroare la obținerea balanței de la BTC.COM V3: {e}")
        return 0, 0

def get_balance_blockcypher(address):
    try:
        url = 'https://api.blockcypher.com/v1/btc/main/addrs/' + address
        response = requests.get(url)
        data = response.json()
        return data['final_balance']
    except Exception as e:
        print(f"Eroare la obținerea balanței de la BlockCypher: {e}")
        return 0


def get_balance_bitflyer(address):
    try:
        url = 'https://chainflyer.bitflyer.jp/v1/address/' + address
        response = requests.get(url)
        data = response.json()
        return data['confirmed_balance']
    except Exception as e:
        print(f"Eroare la obținerea balanței de la BitFlyer: {e}")
        return 0

def get_balance_blockcypher_v1(address):
    try:
        url = 'https://api.blockcypher.com/v1/btc/main/addrs/' + address
        response = requests.get(url)
        data = response.json()
        return data['balance']
    except Exception as e:
        print(f"Eroare la obținerea balanței de la BlockCypher V1: {e}")
        return 0


def get_random_api_balance(address):
    api_function = random.choice(list(api_functions.values()))
    return api_function(address)

def main():
    # Presupunând că avem o listă de adrese Bitcoin generate anterior
    generated_addresses = ["adresa1", "adresa2", "adresa3", ...]  # Completează cu adresele reale

    for address in generated_addresses:
        balance = get_random_api_balance(address)
        print(f"Address: {address}, Balance: {balance}")

if __name__ == "__main__":
    main()
