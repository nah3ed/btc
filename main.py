import os
import time
import random
import binascii
import ecdsa
from bitcoinlib.keys import Key
from concurrent.futures import ProcessPoolExecutor

def generate_address(start_int, end_int, current_value, generate_randomly):
    if generate_randomly:
        private_key_int = random.randint(start_int, end_int)
    else:
        private_key_int = current_value

    private_key_hex = hex(private_key_int)[2:]

    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex.zfill(64)), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key

    public_key_compressed = (b'\02' if vk.pubkey.point.y() % 2 == 0 else b'\03') + vk.to_string()[:32]
    key_compressed = Key(public_key_compressed)
    address_compressed = key_compressed.address()

    return address_compressed, private_key_hex, private_key_int

def main():
    start_range = int('1A838B13505B26867', 16)
    end_range = int('9A838B13505B26867', 16)
    current_value = start_range
    addresses_generated = 0
    start_time = time.time()
    file_part = 1
    max_file_size = 4 * 1024 * 1024 * 1024  # 4 GB
    file_name = f"partea_{file_part}.txt"
    file = open(file_name, 'w')

    print("Select generation mode: (1) Random, (2) Sequential")
    choice = input("Enter choice (1 or 2): ")
    generate_randomly = choice == '1'

    with ProcessPoolExecutor(max_workers=12) as executor:
        while True:
            future = executor.submit(generate_address, start_range, end_range, current_value, generate_randomly)
            address, private_key, last_value = future.result()

            # Scriem în fișier și verificăm dimensiunea
            file.write(f"{address} {private_key}\n")
            if os.path.getsize(file_name) >= max_file_size:
                file.close()
                file_part += 1
                file_name = f"partea_{file_part}.txt"
                file = open(file_name, 'w')

            addresses_generated += 1
            current_value = last_value + 1 if not generate_randomly else current_value

            # Afișează viteza de generare la fiecare 10 adrese generate
            if addresses_generated % 10 == 0:
                current_time = time.time()
                speed = addresses_generated / (current_time - start_time)
                print(f"Generated {addresses_generated} addresses at {speed:.2f} addresses per second")

    file.close()

if __name__ == "__main__":
    main()
