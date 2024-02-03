import hashlib
import os
import time
import pyfiglet
import textwrap

banner_text = "SHA256 BENCHMARK"
wrapped_text = "\n".join(textwrap.wrap(banner_text, width=40))
banner = pyfiglet.figlet_format(wrapped_text)
print(banner)

print('Welcome to Sha256 Benchmark!')

def benchmark_sha256():
    start_time = time.time()
    total_hashes = 0
    while True:
        data = os.urandom(1024)  # Generate 1 KB of random data
        hashlib.sha256(data).hexdigest()
        total_hashes += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            break
        if elapsed_time >= 1:
            keys_per_second = total_hashes / elapsed_time
            units = ["Kkeys/s", "Mkeys/s", "Gkeys/s", "Tkeys/s", "Pkeys/s"]
            speed = keys_per_second
            unit = "keys/s"
            for u in units:
                if speed < 1000:
                    unit = u
                    break
                speed /= 1000
            print(f"Searching Speed:{keys_per_second:.2f} {unit}", end='\r')

if __name__ == "__main__":
    benchmark_sha256()