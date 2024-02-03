import hashlib
import itertools
import string
import time
import pyfiglet
import textwrap

banner_text = "SHA256 CRACKER"
wrapped_text = "\n".join(textwrap.wrap(banner_text, width=40))
banner = pyfiglet.figlet_format(wrapped_text)
print(banner)

# Define the minimum and maximum length of the strings to be hashed
min_length = int(input("Enter the minimum length of the strings to generate: "))
max_length = int(input("Enter the maximum length of the strings to generate: "))

# Prompt the user for the target SHA256 hash value to match
target_hash = input("Enter the target SHA256 hash value to match: ")

# Define the characters to be used in the strings to be hashed
characters = input("Enter the charset to use: ")

# Define the SHA256 function to be used
sha256 = hashlib.sha256

# Loop through all possible combinations of strings within the minimum and maximum length
start_time = time.time()
for length in range(min_length, max_length+1):
    for combination in itertools.product(characters, repeat=length):
        plaintext = ''.join(combination).encode('utf-8')
        sha256_hash = sha256(plaintext).hexdigest()
        print(f"Generated hash: {sha256_hash}")

# Check if the hash matches the target hash
        if sha256_hash == target_hash:
            end_time = time.time()
            print(f"\nHash found: {sha256_hash} corresponds to plaintext {plaintext.decode('utf-8')}")
            print(f"Total time: {end_time - start_time} seconds")
            exit()

print("Hash not found within the specified range.")