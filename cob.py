from coinbase.wallet.client import Client

api_key = 'XXXXXX'
api_secret = 'XXXXXX'
client = Client(api_key, api_secret)
account_id = client.get_primary_account()['id']
address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплты
print(address_for_tranz)