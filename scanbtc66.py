from bit import Key
from bit.format import bytes_to_wif
import random
import atexit
from time import time
from datetime import timedelta, datetime
import colorama
from colorama import Fore, Style
import logging
from multiprocessing import Process

colorama.init()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def seconds_to_str(elapsed=None):
    if elapsed is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        return str(timedelta(seconds=elapsed))

def log(txt, elapsed=None):
    logging.info(txt)
    if elapsed:
        logging.info("Elapsed time: %s", elapsed)

def end_log():
    end = time()
    elapsed = end - start
    return str(timedelta(seconds=elapsed))

def process_range(start, end):
    for _ in range(start, end):
        ran = random.randint(30000488147419103260, 70000000000000000000)
        key = Key.from_int(ran)
        seed = str(ran)
        wif = bytes_to_wif(key.to_bytes(), compressed=False)
        wif2 = bytes_to_wif(key.to_bytes(), compressed=True)
        key1 = Key(wif)
        caddr = key.address
        uaddr = key1.address
        bal = key.get_balance('btc')
        bal1 = key1.get_balance('btc')

        logging.info('<== Current PrivateKey (dec) ==> %s', seed)
        logging.info('<================================= Bitcoin Addresses Checked for Cash =================================>')
        logging.info('%s : %s : %s : %s', caddr, key.to_hex(), wif2, bal)
        logging.info('%s : %s : %s : %s', uaddr, key1.to_hex(), wif, bal1)
        logging.info('Scan Number: %d, Total Wallets Checked: %d', count, total)
        logging.info('---scanbtc66.py--- Random Scan That shit ---Weatose ---scanbtc66.py--- %s', seconds_to_str())

        if float(bal) or float(bal1) > 0:
            logging.info('<================================= WINNER Weatose WINNER WINNER =================================>')
            logging.info('Congrats, you have found a wallet with a balance: %s : Balance: %s', caddr, bal)
            logging.info('Congrats, you have found a wallet with a balance: %s : Balance: %s', uaddr, bal1)
            logging.info('PrivateKey (wif) Compressed: %s', wif2)
            logging.info('PrivateKey (wif) UnCompressed: %s', wif)
            logging.info('Matching Key ==== Found!!!\n PrivateKey  (hex): %s', key.to_hex())
            logging.info('Matching Key ==== Found!!!\n PrivateKey  (dec): %s', seed)
            logging.info('Weatose Donations bc1qsxs2eudlfgstfrnssn5l2athagfjp0zwrqvszs')
            logging.info('<================================= WINNER WINNER WINNER WINNER =================================>')
            with open("Weatose.txt", "a") as f:
                f.write('\n=============Bitcoin Address with Total Received Amount=====================\n')
                f.write('PrivateKey (hex): ' + key.to_hex() + '\n')
                f.write('Bitcoin Address Compressed: ' + caddr + '\n')
                f.write('Bitcoin Address UnCompressed: ' + uaddr + '\n')
                f.write('PrivateKey (wif) Compressed: ' + wif2 + '\n')
                f.write('PrivateKey (wif) UnCompressed: ' + wif + '\n')
                f.write('=============Bitcoin Address with Total Received Amount=====================\n')
                f.write('Weatose Donations bc1qsxs2eudlfgstfrnssn5l2athagfjp0zwrqvszs\n')

x = 1
y = 115792089237316195423570985008687907852837564279074904382605163141518161494336

logging.info(Fore.GREEN + "Starting search... Please Wait ")
logging.info("=====================================================")

count = 0
total = 0
num_processes = 9  # Number of processes to run concurrently
chunk_size = (y - x) // num_processes

start = time()
atexit.register(end_log)
log("Start Program")

def main():
    processes = []

    for i in range(num_processes):
        start_range = x + i * chunk_size
        end_range = x + (i + 1) * chunk_size if i < num_processes - 1 else y
        p = Process(target=process_range, args=(start_range, end_range))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_log()

if __name__ == '__main__':
    main()
