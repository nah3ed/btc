import os
import time
import random
import binascii
import ecdsa
from bitcoinlib.keys import Key
from concurrent.futures import ProcessPoolExecutor

def get_file_name(prefix, part):
    return f"{prefix}_part{part}.txt"

def generate_address(start_int, end_int, generate_randomly, max_file_size):
    current_value = start_int
    file_handles = {}
    file_parts = {}
    addresses_generated = 0
    start_time = time.time()
    flush_interval = 100  # Numărul de adrese generate înainte de a face flush

    while True:
        private_key_int = random.randint(start_int, end_int) if generate_randomly else current_value
        current_value += 1 if not generate_randomly else 0

        private_key_hex = hex(private_key_int)[2:]

        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex.zfill(64)), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key

        public_key_uncompressed = b'\04' + vk.to_string()
        key_uncompressed = Key(public_key_uncompressed)
        address_uncompressed = key_uncompressed.address()

        public_key_compressed = (b'\02' if vk.pubkey.point.y() % 2 == 0 else b'\03') + vk.to_string()[:32]
        key_compressed = Key(public_key_compressed)
        address_compressed = key_compressed.address()

        for address in [address_compressed, address_uncompressed]:
            prefix = address[:3]
            file_parts[prefix] = file_parts.get(prefix, 1)
            file_name = get_file_name(prefix, file_parts[prefix])
            if file_name not in file_handles:
                file_handles[file_name] = open(file_name, 'w')

            file_handle = file_handles[file_name]
            file_handle.write(f"{address} {private_key_hex}\n")

            if addresses_generated % flush_interval == 0:
                file_handle.flush()
                current_time = time.time()
                speed = addresses_generated / (current_time - start_time)
                print(f"Generated {addresses_generated} addresses at {speed:.2f} addresses per second")

            if os.path.getsize(file_name) >= max_file_size:
                file_handle.close()
                file_parts[prefix] += 1
                file_name = get_file_name(prefix, file_parts[prefix])
                file_handles[file_name] = open(file_name, 'w')

        addresses_generated += 1

def main():
    start_range = int('1A838B13505B26867', 16)
    end_range = int('9A838B13505B26867', 16)
    max_file_size = 4 * 1024 * 1024 * 1024  # 4 GB

    print("Select generation mode: (1) Random, (2) Sequential")
    choice = input("Enter choice (1 or 2): ")
    generate_randomly = choice == '1'

    with ProcessPoolExecutor(max_workers=12) as executor:
        for _ in range(12):
            executor.submit(generate_address, start_range, end_range, generate_randomly, max_file_size)

if __name__ == "__main__":
    main()
