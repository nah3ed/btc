# Open the input file for reading and output file for writing
with open('btcwalleterster.txt', 'r') as input_file, open('output_file.txt', 'w') as output_file:
    # Read the input file line by line
    lines = input_file.readlines()
    
    # Loop through the lines in the input file
    for line in lines:
        # Check if the line starts with "P2PKH Address"
        if line.startswith("P2PKH Address: "):
            # Extract the P2PKH Address from the line
            p2pkh_address = line.split(": ")[1].strip()
            
            # Write the P2PKH Address to the output file
            output_file.write(p2pkh_address + '\n')

print("P2PKH Addresses extracted and saved to 'output_file.txt'.")
