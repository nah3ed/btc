import numpy as np
import matplotlib.pyplot as plt
import gmpy2
import scipy.fftpack
import random

# Define some parameters
k = 256  # Bit length of private key and nonce
m = 100  # Number of signatures to observe
t = 100  # Number of traces to generate per signature
noise = 0.01  # Noise level in timing traces

# Generate a random private key (hypothetical) as a bit string
private_key = ''.join(random.choice('01') for _ in range(k))

# Generate a list of random messages to sign
msg_list = [random.getrandbits(k) for _ in range(m)]

# Define a function to generate a random nonce with a given bit value at a given position
def generate_nonce(bit, pos):
    mask = 1 << (k - pos - 1)
    if bit == '0':
        return random.getrandbits(k) & ~mask
    else:
        return random.getrandbits(k) | mask

# Define a function to simulate the timing of extended GCD algorithm for projective to affine conversion
def simulate_timing(x, y, z):
    timing = 0
    while z != 0:
        timing += 1
        x, y, z = (y % z), (z % x), (x % y)
    return timing

# Define a function to add noise to a timing trace
def add_noise(timing, noise):
    n = np.random.normal(0, noise)
    noisy_timing = timing + n
    return noisy_timing

# Define a function to perform a LadderLeak attack
def ladderleak_attack(private_key, k, t, noise):
    key_bits = []
    for i in range(k):
        print(f"Recovering bit {i}...")
        zero_timings = []
        one_timings = []
        for msg in msg_list:
            for _ in range(t):
                nonce = generate_nonce('0', i)
                # Simulate signing without ecdsa library
                # Here, you can add your own logic to simulate signing
                timing = random.randint(1, 100)  # Simulated timing trace
                timing = add_noise(timing, noise)
                zero_timings.append(timing)

            nonce = generate_nonce('1', i)
            # Simulate signing without ecdsa library
            # Here, you can add your own logic to simulate signing
            timing = random.randint(1, 100)  # Simulated timing trace
            timing = add_noise(timing, noise)
            one_timings.append(timing)

        zero_mean = np.mean(zero_timings)
        one_mean = np.mean(one_timings)

        plt.hist(zero_timings, bins=50, alpha=0.5, label="Zero bit")
        plt.hist(one_timings, bins=50, alpha=0.5, label="One bit")
        plt.axvline(zero_mean, color="blue", linestyle="--", label="Zero mean")
        plt.axvline(one_mean, color="orange", linestyle="--", label="One mean")
        plt.xlabel("Timing")
        plt.ylabel("Frequency")
        plt.legend()
        plt.title(f"Timing values for bit {i}")
        plt.show()

        N = len(zero_timings) + len(one_timings)
        L = gmpy2.next_prime(N)
        omega = gmpy2.powmod(2, (L - 1) // N, L)
        c_zero = [gmpy2.powmod(omega, -int(t), L) for t in zero_timings]
        c_one = [gmpy2.powmod(omega, -int(t), L) for t in one_timings]
        c_zero.extend([0] * (N - len(c_zero)))
        c_one.extend([0] * (N - len(c_one)))

        c_zero_fft = scipy.fftpack.fft(c_zero)
        c_one_fft = scipy.fftpack.fft(c_one)
        c_prod_fft = [x * y for x, y in zip(c_zero_fft, c_one_fft)]
        c_prod = scipy.fftpack.ifft(c_prod_fft)
        c_prod = [gmpy2.powmod(int(np.round(x.real)), 1, L) for x in c_prod]
        lsb = gmpy2.invert(2 * (k - i), L) * max(c_prod) % L
        lsb >>= (L - 1).bit_length() // 2 + 1

        key_bits.append(lsb)

    recovered_key = sum((bit << i) for i, bit in enumerate(key_bits))

    return key_bits, bin(recovered_key)[2:].zfill(k)

recovered_bits, recovered_private_key = ladderleak_attack(private_key, k, t, noise)

print("Recovered Private Key:", recovered_private_key)
print("Recovered Bits:", recovered_bits)
