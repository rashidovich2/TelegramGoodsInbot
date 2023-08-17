from tronpy import Tron

# connect to the Tron blockchain
client = Tron()

# create a Tron wallet and print out the wallet address & private key
def create_wallet(): 
    wallet = client.generate_address()
    print("Wallet address:  %s" % wallet['base58check_address'])
    print("Private Key:  %s" % wallet['private_key'])

create_wallet()