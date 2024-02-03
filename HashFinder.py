import re
import clipboard
import pyfiglet
import textwrap

banner_text = "Hash Finder"
wrapped_text = "\n".join(textwrap.wrap(banner_text, width=40))
banner = pyfiglet.figlet_format(wrapped_text)
print(banner)

# Prompt the user to input the hash
hash_format = input("Please enter the hash: ")

# If the input is empty, try to get input from clipboard
if not hash_format:
    try:
        hash_format = clipboard.paste()
    except Exception as e:
        print("Failed to get input from clipboard:", e)
        exit(1)

# Extract mkey length, mkey, salt length, salt, iterations from the hash format
match = re.match(r"\$bitcoin\$(\d+)\$([a-fA-F0-9]+)\$(\d+)\$([a-fA-F0-9]+)\$(\d+)", hash_format)
if match:
    mkey_length = int(match.group(1))
    mkey = match.group(2)
    salt_length = int(match.group(3))
    salt = match.group(4)
    iterations = int(match.group(5))

    # Print the extracted information
    print(f"mkey: {mkey}")
    print(f"salt: {salt}")
    print(f"iterations: {iterations}")

    # Write extracted information to walletinfo.txt
    with open("walletinfo.txt", "w") as f:
        f.write(f"mkey: {mkey}\n")
        f.write(f"salt: {salt}\n")
        f.write(f"iterations: {iterations}\n")

    print("Extracted information written to walletinfo.txt.")
else:
    print("Invalid hash format.")