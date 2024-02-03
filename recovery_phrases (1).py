import requests
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

def get_address_balance(address):
    try:
        url = f"https://blockchain.info/balance?active={address}"
        response = requests.get(url)
        data = response.json()
        return data[address]['final_balance']
    except Exception as e:
        print(f"Eroare la obținerea balanței: {e}")
        return 0

def main():
    mnemo = Mnemonic("english")
    with open("recovery_phrases.txt", "r") as file, open("addresses_with_balances.txt", "w") as output_file:
        for line in file:
            phrase = line.strip()
            if not phrase:
                continue
            print(f"Procesez fraza: {phrase}")
            if mnemo.check(phrase):
                seed = Bip39SeedGenerator(phrase).Generate()
                bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
                address = bip44_wallet.PublicKey().ToAddress()
                balance = get_address_balance(address)
                output_file.write(f"Balance: {balance}, Address: {address}, Phrase: {phrase}, Seed: {seed.hex()}\n")
                print(f"Adresa: {address}, Balanță: {balance}")
            else:
                print("Fraza de recuperare este invalidă sau incompletă.")

if __name__ == "__main__":
    main()
