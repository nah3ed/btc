from web3 import Web3
from time import sleep
from eth_utils import to_checksum_address

infura_url = 'https://mainnet.infura.io/v3/ API KEY'
w3 = Web3(Web3.HTTPProvider(infura_url))

def read_addresses_from_file(file_path):
    addresses = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                address = line.strip().split(" ")[0]
                addresses.append(address)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading addresses: {e}")
    return addresses

def check_balance(address):
    try:
        checksum_address = to_checksum_address(address)
        balance = w3.eth.get_balance(checksum_address)
        return balance
    except Exception as e:
        print(f"Error for {address}: {e}")
        return None

if __name__ == "__main__":
    input_file_path = "ETH-ADDRESS.txt"
    addresses = read_addresses_from_file(input_file_path)

    if addresses:
        for address in addresses:
            balance = check_balance(address)
            if balance is not None:
                print(f"Address: {address}, Balance: {balance} Balance")
            sleep(0.1)  # Adjust the delay as needed to comply with rate limits
    else:
        print("No valid addresses to check.")
