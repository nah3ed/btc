def compare_lines(file1_lines, file2_lines):
    common_lines = set(file1_lines) & set(file2_lines)
    
    if common_lines:
        print("Same lines in both files:")
        for line in common_lines:
            print(line)
    else:
        print("There are no identical lines in both files.")

def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# Text file paths
file1_path = 'file1.txt' # File with public addresses with balance
file2_path = 'file2.txt' # File with the generated addresses waiting for verification

# Reading lines from files
file1_lines = read_file_lines(file1_path)
file2_lines = read_file_lines(file2_path)

# Calling the comparison function
compare_lines(file1_lines, file2_lines)

input("Press Enter to exit...")
