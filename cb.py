from aiohttp import ClientConnectorCertificateError
from async_class import AsyncClass
#from yoomoney import Client
from coinbase.wallet.client import Client


api_key = 'QUmnMHJ7OrOJnIM4'
api_secret = 'gQr0L7ypPQXTpYRDzXJFILcAARRjBynH'
client = Client(api_key, api_secret)
account_id = client.get_primary_account()['id']
        #sum = int(sum) + 10 #прибавляется комиссия в btc
        #btc_price = round(float((client.get_buy_price(currency_pair='BTC-RUB')["amount"])))
        #print(btc_price)
        #sum = float(str(sum / btc_price)[:10]) #сколько сатох нужно юзеру оплатить
address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплты
print(address_for_tranz)