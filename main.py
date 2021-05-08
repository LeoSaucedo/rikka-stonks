import robin_stocks.robinhood as rh
import json
import crypto

try:
  with open("config.json") as f:
    config = json.load(f)
  username = config["robinhood"]["user"]
  password = config["robinhood"]["password"]
except:
  username = input("Robinhood username: ")
  password = input("Robinhood password: ")
login = rh.login(username, password)
option = int(input(
    "Welcome to rikka-bot trading bot. Please choose from the following:\n1) Crypto Trailing Stop Loss\n\n> "))
if(option == 1):
  crypto.trailing_stop_loss()
