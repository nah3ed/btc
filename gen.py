import ecdsa
import hashlib
import binascii
import math

# Configurarea numărului de adrese pentru fiecare tip de număr
num_addresses_per_category = 10

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_repdigit(n):
    str_n = str(n)
    return len(set(str_n)) == 1

def to_duodecimal(n):
    digits = '0123456789AB'
    res = ''
    while n > 0:
        res = digits[n % 12] + res
        n //= 12
    return res if res else '0'

def decimal_to_hex(number):
    return format(number, '064x')

def private_to_public(private_key_hex):
    private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1).verifying_key
    public_key = '04' + private_key.to_string().hex()
    return public_key

def public_to_address(public_key_hex):
    public_key_bytes = bytes.fromhex(public_key_hex)
    sha256 = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    address = '00' + binascii.hexlify(ripemd160).decode('utf-8')
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(address)).digest()).digest()[:4]
    bitcoin_address = base58(address + binascii.hexlify(checksum).decode('utf-8'))
    return bitcoin_address

def base58(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    value = int(address_hex, 16)
    result = ''
    while value >= 58:
        value, mod = divmod(value, 58)
        result = alphabet[mod] + result
    result = alphabet[value] + result
    n_pad = 0
    for char in address_hex:
        if char == '0':
            n_pad += 1
        else:
            break
    return '1' * n_pad + result

def generate_irrational_number_address(irrational_number, digit_index):
    irrational_str = f"{irrational_number:.15f}"
    number_str = irrational_str[digit_index + 1]  # +1 pentru a sări peste punctul zecimal
    
    # Verifică dacă number_str este o cifră și folosește 0 dacă nu este
    number = int(number_str) if number_str.isdigit() else 0

    # Asigură-te că numărul este în intervalul valid pentru o cheie privată Bitcoin
    min_private_key = 1
    max_private_key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    number = (number % (max_private_key - min_private_key)) + min_private_key

    hex_private_key = decimal_to_hex(number)
    public_key = private_to_public(hex_private_key)
    bitcoin_address = public_to_address(public_key)
    return f"Irațional ({number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}"



# Generarea adresei într-o buclă infinită pentru diferite categorii de numere
number = 1
category_index = 0
address_count = 0
irrational_digit_index = 0  # Index pentru cifrele din numerele iraționale

while True:
    hex_private_key = decimal_to_hex(number)
    public_key = private_to_public(hex_private_key)
    bitcoin_address = public_to_address(public_key)

    duodecimal_number = to_duodecimal(number)

    if category_index == 0 and number % 2 == 0:  # Numere pare
        print(f"Par ({number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}")
    elif category_index == 1 and number % 2 != 0:  # Numere impare
        print(f"Impar ({number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}")
    elif category_index == 2 and is_prime(number):  # Numere prime
        print(f"Prim ({number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}")
    elif category_index == 3 and is_repdigit(number):  # Numere repdigit
        print(f"Repdigit ({number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}")
    elif category_index == 4 and to_duodecimal(number):  # Numere duodecimale
        print(f"Duodecimal ({duodecimal_number}) -> Cheie Privată: {hex_private_key} -> Adresă Bitcoin: {bitcoin_address}")
    elif category_index == 5:  # Numere iraționale
        pi_address = generate_irrational_number_address(math.pi, irrational_digit_index)
        e_address = generate_irrational_number_address(math.e, irrational_digit_index)
        print(pi_address)
        print(e_address)

    address_count += 1
    if address_count >= num_addresses_per_category:
        category_index = (category_index + 10) % 6  # Trecem la următoarea categorie
        address_count = 0
        if category_index == 5:  # Resetare index pentru cifrele iraționale
            irrational_digit_index = (irrational_digit_index + 1) % 15

    number += 1  # Incrementăm numărul pentru a continua bucla
