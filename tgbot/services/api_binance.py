from binance.spot import Spot

client = Spot()

# Get server timestamp
print(client.time())
# Get klines of BTCUSDT at 1m interval
print(client.klines("BTCUSDT", "1m"))
# Get last 10 klines of BNBUSDT at 1h interval
print(client.klines("BNBUSDT", "1h", limit=10))

# API key/secret are required for user data endpoints
client = Spot(api_key='XXXXXXXXX', api_secret='XXXXXXXXX')

# Get account and balance information
print(client.account())




# Post a new order
params = {
    'coin': 'USDT',
    'status': '1',
    'recvWindow': 5000
}

#response = client.new_order(**params)
response = client.deposit_history(**params)
print(response)

# Post a new order
params = {
    'coin': 'USDT',
    'network': 'TRX',
    'recvWindow': 5000
}

#response = client.new_order(**params)
response2 = client.deposit_address(**params)
print(response2)