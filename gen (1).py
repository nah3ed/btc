import ecdsa
import random
from bitcoin import privkey_to_address

def is_probable_prime(n, k=10):
    """ Test probabilistic Miller-Rabin pentru primalitate """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_private_keys(start):
    value = start
    while True:
        if is_probable_prime(value):
            private_key_hex = value.to_bytes(32, 'big').hex()
            address = privkey_to_address(private_key_hex)
            yield private_key_hex, address
        value += 1

# Exemplu de utilizare
start_value = 36893488147419103232

for private_key, address in generate_prime_private_keys(start_value):
    print(f"Cheie Privată: {private_key}, Adresă Bitcoin: {address}")
