#@pv081079

import base58
import hashlib
import sys


compress_pubkey = False


def hash160(hex_str):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(hex_str)
    rip.update( sha.digest() )
    return rip.hexdigest()

def pubkeys_to_address(filein, fileout):
    with open(filein) as inf, open(fileout, 'w') as outf:
        count = 0
        skip = 0
        for x in inf.readlines():
            x = x.strip()
            if (compress_pubkey):
                if (ord(bytearray.fromhex(x[-2:])) % 2 == 0):
                    pubkey_compressed = '02'
                else:
                    pubkey_compressed = '03'
                pubkey_compressed += x[2:66]
                hex_str = bytearray.fromhex(pubkey_compressed)
            else:
                hex_str = bytearray.fromhex(x)

            key_hash = '00' + hash160(hex_str)
            sha = hashlib.sha256()
            sha.update( bytearray.fromhex(key_hash) )
            checksum = sha.digest()
            sha = hashlib.sha256()
            sha.update(checksum)
            checksum = sha.hexdigest()[0:8]
            try:
                outf.write(base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) ).decode('utf-8'))
                outf.write("\n")
                count += 1
            except:
                skip += 1
                print("skipped pubkey:", x)
        print('processed :', count, 'pubkeys', '\nskipped   :', skip, 'pubkeys', )
    outf.close()

argc = len(sys.argv)
argv = sys.argv

if argc == 1 or argc != 3:
    print('Usage:')
    print('\tpython3 ' + argv[0].replace('\\', '/').split('/')[-1] + ' pubkeys_in.txt address_out.txt')
elif argc == 3:
    pubkeys_to_address(argv[1], argv[2])