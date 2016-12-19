import krakenex
from poloniex import Poloniex
import time
import datetime

# could be that this needs to be changed! Check your XMR Deposit address on polo!!!
#poloXMRAddress = '47sghzufGhJJDQEbScMCwVBimTuq6L5JiRixD8VeGbpjCTA12noXmi4ZyBZLc99e66NtnKff34fHsGRoyZk3ES1s1V4QVcB'
poloXMRAddress = 'Insert polo XMR deposit address'

k = krakenex.API()
k.load_key('kraken.key')
#load polo key
f = open("polo.key", "r")
poloKey = f.readline().strip()
poloSecret = f.readline().strip()
# build polo api object
polo = Poloniex(poloKey, poloSecret)

#amount in EUR you want to have on your bank account(This can be less since the proess takes so long)
amountToGet = 100
# change this to your withdraw key
krakenWithdrawBankAccountName = 'Fidor'



def getBTCBalanceKraken():
    return float(k.query_private('Balance', {})['result']['XXBT'])
def getEURBalanceKraken():
    return float(k.query_private('Balance', {})['result']['ZEUR'])
def getXMRPrice( neededBTC ):
    depth = 0
    xmrBids = polo.returnOrderBook('BTC_XMR')['bids']
    for orderIndex, order in enumerate(xmrBids):
        depth += (float(order[0]) * float(order[1]))
        if depth > (neededBTC*2):
            break
    return float(order[0])
def getBTCPrice():
    depth = 0
    orderbook = k.query_public('Depth', {'pair': 'XBTEUR'})
    btcBids = orderbook['result']['XXBTZEUR']['bids']
    for orderIndex, order in enumerate(btcBids):
        depth += (float(order[0]) * float(order[1]))
        if depth > (amountToGet*2):
            break
    return float(order[0])
def getXMRBalance():
    poloBalance = polo.returnBalances()
    return float(poloBalance['XMR'])

def getBTCBalance():
    poloBalance = polo.returnBalances()
    return float(poloBalance['BTC'])


btcPrice = getBTCPrice()
btcNeeded = 1/float(btcPrice) * amountToGet
xmrPrice = getXMRPrice(btcNeeded)
newXMRBalance = poloOldBalanceXMR = getXMRBalance()
poloXMRPaymentId = polo.returnDepositAddresses()['XMR'];
neededXmr = btcNeeded/xmrPrice

print ('The btc price is ', float(btcPrice), 'so you need', btcNeeded, 'BTC or(', neededXmr,'XMR)for ', amountToGet, 'EUR')
print ('Send', neededXmr, 'to "', poloXMRAddress, '" with paymentId "', poloXMRPaymentId,'"')
print ('Polo XMR balance', poloOldBalanceXMR)

x = input("Did you send the xmr(y/n)? (this will start the waiting loop on polo)")
print (x)
if (x != 'y'):
    print('User about!')
    exit()

print(datetime.datetime.now())
# loop for checking if the xmr is there
minute = 0
while (True):
    print ('Waiting for XMR to be credited to polo', minute, 'Min waiting')
    newXMRBalance = getXMRBalance()
    if (newXMRBalance > poloOldBalanceXMR):
        print ('New incomming XMR detected.. trade it now to BTC')
        break
    time.sleep(60)
    minute += 1

# get the btc_xmr price again
xmrPrice = getXMRPrice(btcNeeded)

newNeededXmr = btcNeeded/xmrPrice
print('Old needed XMR:', neededXmr, 'new need XMR', newNeededXmr, 'for ', amountToGet, 'EUR')

# try to get the needed BTC or the max
xmrToSell = newXMRBalance
if (newXMRBalance > newNeededXmr):
    xmrToSell = newNeededXmr

print('Polo got a deposit of', newXMRBalance-poloOldBalanceXMR, 'XMR')
print('Selling',xmrToSell ,'XMR now at', xmrPrice)

print(polo('sell', {'currencyPair': 'BTC_XMR', 'rate': str(xmrPrice), 'amount': str(xmrToSell), 'fillOrKill': str(1)}))

krakenBTCAddress = k.query_private('DepositAddresses', {'asset': 'XBT', 'method': 'Bitcoin'})['result'][0]['address']

print ('Got Kraken deposit BTC address', krakenBTCAddress)

newBTCBalance = oldBTCBalance = getBTCBalanceKraken()
print ('Polo start withdraw')
print (polo.withdraw('BTC',getBTCBalance(), krakenBTCAddress))

# loop for checking if the xmr is there
minute = 0
while (True):
    print ('Waiting for BTC from polo to be credited to kraken', minute, 'Min waiting')
    newBTCBalance = getBTCBalanceKraken()
    if (newBTCBalance > oldBTCBalance):
        print ('New incoming BTC detected.. trade it now to EUR')
        break
    time.sleep(60)
    minute += 1

print('Kraken got a deposit of', newBTCBalance-oldBTCBalance, 'BTC')

btcPrice = getBTCPrice()
btcNeeded = 1/float(btcPrice) * amountToGet

btcToSell = newBTCBalance
if (newBTCBalance > btcNeeded):
    btcToSell = btcNeeded
print ('Buying EUR for ', newBTCBalance, 'BTC')

print('Selling',btcToSell ,'BTC now at market price ~', btcPrice)

print (k.query_private('AddOrder', {'trading_agreement' : 'agree', 'pair': 'XBTEUR', 'type': 'sell','ordertype': 'market', 'volume': newBTCBalance}))

print ('Withdrawing EUR from kraken')
print (k.query_private('Withdraw', {'asset': 'EUR', 'key': krakenWithdrawBankAccountName, 'amount': getEURBalanceKraken()}))

print(datetime.datetime.now())





