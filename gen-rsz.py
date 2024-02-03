from ecdsa import SigningKey, SECP256k1, util
import hashlib
import random

# Prompt the user to enter the private key
private_key_hex = input("Enter your private key in hexadecimal format: ")
private_key = bytes.fromhex(private_key_hex)

# Create a signing key from the private key
signing_key = SigningKey.from_string(private_key, curve=SECP256k1)

# Prompt the user to enter the public key
public_key_hex = input("Enter the public key in uncompressed format: ")
public_key_bytes = bytes.fromhex(public_key_hex)
public_key = util.string_to_number(public_key_bytes)

# Generate 20 sets of random R, S, and H values
for i in range(1, 80):
    # Generate a random message
    random_message = str(random.getrandbits(256)).encode('utf-8')

    # Calculate the hash of the random message
    message_hash = hashlib.sha256(random_message).digest()

    # Sign the random message
    signature = signing_key.sign_digest(message_hash, sigencode=util.sigencode_string)

    # Extract the components of the signature
    R, S = util.sigdecode_string(signature, signing_key.curve.order)

    # Print the generated values
    print(f"\nSet {i}:")
    print(f"Generated R: {hex(R)}")
    print(f"Generated S: {hex(S)}")
    print(f"Generated H: {hex(int.from_bytes(message_hash, byteorder='big'))}")