import json
from log import logHandler as log
from binanceWrapper.client import Client
from session import Session
from time import sleep

BYE_TIME = 5
WAIT_TIME = 2

startStr = 'start'
print('\nPlease type "start" to run BotOne v0.1-alpha')
command = input(">")

print('\nPlease type your password if your data is encrypted, otherwise press Enter')
password = input(">")

if command == startStr:
    wait = WAIT_TIME
    #sleep(wait)
    print("\nBotOne-v0.1-alpha is running for the very first time.\n")
    sleep(wait)
    print("GOOD LUCK!\n")
    #sleep(wait)
    print("Ch'a Maronn t'accumpagn\n\n")
    #sleep(wait)
#startStrstart
log.event_log_append("An instance of ", "BotOne-v0.1-alpha ", "has been launched.")


while command.lower() == startStr.lower():
    newSession = Session("clientOne", password)

print('\nBye!\n')
sleep(BYE_TIME)







## keys0 API keys - remind to restrict the IPs after the bot is running
#myApiKey = 'vdBlDHNvNdjDyGq2OVOpAasIaw9KCuX64Tkyd8UMPBAKZt9iy0CI4NJsSo0Cugpd'
#mySecretKey = 'OQUD762C24JvzHzFqeWozndcWz4ykfkbQ6ViP8SAenpIRWejWN0zaXOX0y8iU4bc'

#client = Client(myApiKey, mySecretKey)



#session0 = client._init_session()

#orderParams = {'symbol': 'DOGEBNB', 'side': 'buy', 'type': 'limit', 'timeInForce': 'GTC', 'quantity': 1000, 'price': 0.0001}
# symbol = 'BNBETH', side = 'buy', type = 'limit', timeInForce = 'GTC', quantity = 0.1, price = 0.075
#order0 = client.create_order(**orderParams)
#print(order0)
#getmarketinfo = client.get_symbol_info("BNBBTC")
#print(getmarketinfo)
#getMyOrders = client.get_all_orders("BNBBTC")
#print(getMyOrders)
#print(client.get_account_status())
#test = client.get_exchange_info().get('rateLimits')
#oo=client.get_open_orders()
#print(oo)
#print(test[0].get('interval'))
#print(client.get_account())
#print(client.get_server_time())
#print(time.time())
#order1=client.create_order(symbol="BNBETH", side='buy', type='limit', timeInForce='GTC', quantity=1, price=.02)
#time.sleep(1)
#cancelorder1 = client.cancel_order(symbol="BNBETH", orderId=order1["orderId"])
#print(cancelorder1)
#oo=client.get_open_orders(symbol="BNBETH")
#print(oo)
#cancelall = client.cancel_all_open_orders(symbol="BNBETH")
#print(str(cancelall))
#oo=client.get_open_orders(symbol="BNBETH")
#print(oo)