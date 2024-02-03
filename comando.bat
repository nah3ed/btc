python2 pywalletHD.py --dumpwallet --wallet=wallet.dat --passphrase=31247590635abe --reserve --importprivkey=KEY --importhex >>wallet.datdump.txt
python2 walletinfoHD.py wallet.dat >> wallet.datencrypted_master_key.txt
python2 bitcoin3jhon.py wallet.dat >> wallet.dat.dathash.txt
