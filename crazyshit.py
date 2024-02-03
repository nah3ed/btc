#!/usr/bin/env python3

import ecdsa
from sympy import mod_inverse

def egcd(a, b):
    "Euclidean greatest common divisor"
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    "Modular inverse"
    # in Python 3.8 you can simply return pow(a,-1,m)
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def mulmod(x,y,m):
    "Modular multiplication"
    return x*y % m

def bigendian_hex2int(hm):
    "Take a little endian hex number, make it big endian and convert it to int" 
    revstr = bytearray.fromhex(hm)
    revstr.reverse()
    bigend = int("".join([hex(a)[2:] for a in revstr]), 16)
    return bigend
 
def main():
    "This gets the Private Key given two ECDSA signatures with successive nonces"
    print("Enter all inputs as hex, without leading 0x")
    s1 = int(" hex value ", 16)
    r1 = int(" hex value ", 16)
    hm1 = " hex value "
    s2 = int(" hex value ", 16)
    r2 = int(" hex value ", 16)
    hm2 = " hex value "
    n = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16)

    
    e1 = bigendian_hex2int(hm1)
    e2 = bigendian_hex2int(hm2)
    dU = mulmod(1 - modinv(s2, n)*e2 + modinv(s1,n)*e1, modinv(modinv(s2,n)*r2 - modinv(s1,n)*r1, n), n)
    print("Private key: " + hex(dU))

if __name__ == "__main__":
    main()


