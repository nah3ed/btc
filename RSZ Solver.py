import ecdsa
import hashlib

# Define the curve and order
curve = ecdsa.SECP256k1
order = curve.order

# Define a function to calculate the inverse modulo N
def inv(a):
    return pow(a, order - 2, order)

# Define a function to get the private key from (r, s, z) values and a public key
def get_private_key(r_values, s_values, z_values, pub_key):
    num_pairs = len(r_values)
    
    # Convert s values to integers
    s_values_int = [int(s, 16) for s in s_values]
    
    # Calculate the differences of k values for all pairs
    diffs = [(s_values_int[i] - s_values_int[j]) % order for i in range(num_pairs) for j in range(i+1, num_pairs)]
    
    for i in range(num_pairs):
        for j in range(i+1, num_pairs):
            if i != j:
                num = (s_values_int[j] * (int(z_values[i], 16) - int(z_values[j], 16)) - s_values_int[i] * (int(z_values[j], 16) - int(z_values[i], 16))) % order
                den = (int(r_values[i], 16) * s_values_int[j] - int(r_values[j], 16) * s_values_int[i]) % order
                diffs.append((num * inv(den)) % order)
    
    # Calculate k using the differences
    k_values = [s_values_int[0] - diff for diff in diffs]
    
    # Check if any of the calculated k values results in a valid private key
    for k in k_values:
        private_key = (k - int(r_values[0], 16)) * inv(s_values_int[0]) % order
        if private_key >= 1 and private_key <= order - 1:
            #Calculate the corresponding public key
            public_key_point = private_key * curve.generator
            public_key_bytes = public_key_point.to_bytes()
            recovered_pub_key_hex = "04" + public_key_bytes[:32].hex() + public_key_bytes[32:].hex()
            # Check if the recovered public key matches the provided public key
            if recovered_pub_key_hex == pub_key:
                return private_key
    
    return None

# Insert the (r, s, z) values for each index
# Index 0
r0 = "008816aaa5c06502a135f04923334808e2e96f3003b5e649d3d4acf1d67f771d46"
s0 = "479721e5d843f56de0d4b53f066536166a2d51f73ebe37d2784f11785c6135c6"
z0 = "b7ab1420c15d44c5bee9cbde67e1ba2afd5dd764cfbf5ccab3aa19224c5bf700"

# Index 1
r1 = "2887cb4fd0943608f49baf6c376e39ef0e94f3092672dc8aa0010622d88fe7da"
s1 = "226955518a1f9ccf7bd4c36dea903c9f55f4e34f6d1d4328966b0a20bb217cb8"
z1 = "4a723fd29687d5b33ba3ac3a393f52cd2a72a24afd7c3222ef1489f78fbf038f"

# Index 2
r2 = "28222e58a94b23b1a6ef2b1a3c56f9db48c974eea154379b50943c0fd1f775b1"
s2 = "32e2545ecdcf944349d2078cc234ec487aae2d9c4dd552ed9624663ec97b2d17"
z2 = "7e64ca068beb949f17adfed26ee600f57b0297e5ce64eb44219a5eec57543e8a"

# Index 3
r3 = "00b2361d8947652124a657adf1d5407d7172728b5e7d09309f3fe91f00c1c87858"
s3 = "1459637208faae2651cc6f4f0ca5b8078a5b8565c713a1a4789da83bc5f5abfa"
z3 = "193f13c15c02ce3c0cc99b2d8dbb4086ef192b89ec7440c6a1aadbb64c93e9ab"

# Index 4
r4 = "008b544bd8fb7c99d397757564b099940fbabc46c9822d041588f1bb9acf66c9af"
s4 = "2f31853696d202ff802c3210918b4998a4125b83508ac2252a977d50406355d8"
z4 = "e24aab1de5aea1ef6bef0aa3e4c0495caaf5098b587dc9dd931f9728ef9a911a"

# Specify the existing public key
existing_public_key_hex = "04cb2a2a074b80ef6827b60c58f291bb32a032a5bb863c9e5e6e309d6f5b7e8df9d6ba0d1af28178c263e9e9b4c60912ba2318100eb19f7d3ba974ff5e31fa21d6"

# Call the function to get the private key
private_key = get_private_key([r0, r1, r2, r3, r4], [s0, s1, s2, s3, s4], [z0, z1, z2, z3, z4], existing_public_key_hex)

if private_key:
    print(f'Extracted Private Key: {hex(private_key)}')
else:
    print('Private key not found.')
