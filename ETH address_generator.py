import hdwallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import EthereumMainnet
import blocksmith
from mnemonic import Mnemonic
import secrets

def generate_random_mnemonic() -> str:
    # Erzeuge ein zufälliges Mnemonik mit 12 Worten
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)  # 128 Bit Stärke für 12 Wörter
    return mnemonic

def generate_address_from_seed(mnemonic: str) -> str:
    try:
        # Erstelle eine BIP44-HD-Wallet für Ethereum
        wallet = hdwallet.BIP44HDWallet(cryptocurrency=EthereumMainnet)
        
        # Setze das Mnemonik und reinige die Derivation
        wallet.from_mnemonic(mnemonic=mnemonic, language="english", passphrase=None)
        wallet.clean_derivation()

        # Definiere die BIP44-Derivation
        derivation_path = BIP44Derivation(cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
        
        # Wende den Pfad auf die Wallet an
        wallet.from_path(path=derivation_path)

        # Erhalte die Adresse
        address_to_check = wallet.address()
        return address_to_check

    except Exception as e:
        print(f"Fehler beim Generieren der Adresse aus dem Mnemonik: {e}")
        return None

def generate_checksum_address_from_privkey(privkey: str) -> str:
    try:
        # Generiere eine Adresse aus dem privaten Schlüssel
        address = blocksmith.EthereumWallet.generate_address(privkey)
        
        # Erzeuge die Prüfziffernadresse
        checksum_address = blocksmith.EthereumWallet.checksum_address(address)
        return checksum_address

    except Exception as e:
        print(f"Fehler beim Generieren der Prüfziffernadresse aus dem privaten Schlüssel: {e}")
        return None

def write_to_file(filename: str, content: str):
    try:
        with open(filename, "a") as file:
            file.write(content + "\n")
        print(f"Daten erfolgreich in '{filename}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")

# Beispiel für die Verwendung
if __name__ == "__main__":
    while True:
        # Generiere ein zufälliges Mnemonik
        random_mnemonic = generate_random_mnemonic()
        print(f"Zufälliges Mnemonik: {random_mnemonic}")

        # Generiere eine Adresse aus dem zufälligen Mnemonik
        result_from_seed = generate_address_from_seed(random_mnemonic)
        
        if result_from_seed:
            print(f"Generierte Adresse aus dem zufälligen Mnemonik: {result_from_seed}")

            # Speichere die Daten in einer TXT-Datei
            data_to_save = f"Zufälliges Mnemonik: {random_mnemonic}\nGenerierte Adresse: {result_from_seed}"
            write_to_file("output.txt", data_to_save)

        # Generiere eine Adresse aus einem zufälligen privaten Schlüssel
        random_private_key = secrets.token_hex(32)
        result_from_privkey = generate_checksum_address_from_privkey(random_private_key)

        if result_from_privkey:
            print(f"Generierte Prüfziffernadresse aus dem zufälligen privaten Schlüssel: {result_from_privkey}")

            # Speichere die Daten in einer TXT-Datei
            data_to_save = f"Zufälliger privater Schlüssel: {random_private_key}\nGenerierte Prüfziffernadresse: {result_from_privkey}"
            write_to_file("output.txt", data_to_save)
