import requests
from tqdm import tqdm

# Read Bitcoin addresses from address.txt
addresses = []
with open("address.txt", 'r') as file:
    addresses = [line.strip() for line in file]

# Create or overwrite output.txt
with open('Address_with_Balance.txt', 'w') as output_file:
    for addr in tqdm(addresses, desc="Checking Balances", unit=" address"):
        req = requests.get("https://blockchain.info/balance?active=" + addr).json()
        balance = req.get(addr, {}).get('final_balance', 0)
        balance_in_btc = balance / 100000000.0  # Convert satoshis to BTC
        output_file.write(f"Address: {addr} - Balance: {balance_in_btc:.8f} BTC\n")
