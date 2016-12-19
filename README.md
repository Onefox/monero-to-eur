# Monero to Euro converter with the lowest fees possible
This small python 3 script is for converting xmr (Monero) coins to EUR and withdrawing them to a bank accout.

I build it in order to change Monero for the lowes possible fee back to EUR and transfer them back to my bankaccount.

Normally this script takes about **~90 minutes**. 30 minutes for the Monero do confirm on poloniex
and another 60 minutes for the Bitcoin to confirm on kraken (Yes kraken still needs 6 confirmations)

If you have [Fidor](fidor.de) bank acount linked your will
have the Euros within 15 minutesin the account after the script is finish, thanks to Fidor even on weekends!

### Target user base
 - In this state the script is for developers and guys that understand the source code
 - It's meant as an help to get the most value back from your Monero

### Installation
 You need Python 3.3 or later.
 
 Install the two library's used.
 [KrakenAPI](https://github.com/veox/python3-krakenex#installation) and
 [PoloniexAPI](https://github.com/s4w3d0ff/python-poloniex#install)
 
 Download the script and add your api keys. 
 Adjust the amountToGet witin the script to the amount of Euros you want to have and
 just run it with python 3.
 

### This script is build on two libs

- [python-poloniex from s4w3d0ff](https://github.com/s4w3d0ff/python-poloniex) that is inspired by '[oipminer](http://pastebin.com/8fBVpjaj)'
- [python3-krakenex from veox](https://github.com/veox/python3-krakenex)

# What do you need?
- A [Kraken](kraken.com) account (Api key and secret)
- A bank account linked to your Kraken account as withdraw method
- A [Poloniex](Poloniex.com) account (Api key and secret)

# Development
Feel free to improve the scipt or add error handling.
It would also be great if the polo XMR payment Id would change once a day, there is an api for that but its not implemented here.

I welcome every pull request :)

# Missing

There is no Error handling. So if someting goes wrong your coins/euro will still be somewhere at polo or kraken, but you should log the script output somewhere!








