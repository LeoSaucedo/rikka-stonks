import robin_stocks.robinhood as rh
import datetime
from time import sleep


def trailing_stop_loss():
  ticker = input(
      "Enter your desired crypto ticker to perform the trailing stop loss on.\n> ")
  for holding in rh.get_crypto_positions():
    if ticker.upper() == holding["currency"]["code"]:
      crypto = holding
  if crypto == None:
    print("You do not own any of the specified crypto. Please place an order on Robinhood, then run this program.")
  else:
    amount = input("You currently own " + str(crypto["cost_bases"][0]["direct_quantity"]
                                              ) + " " + ticker + ". Please enter your desired sell amount.\n> ")
    stopAmt = 1.0 - float(input(
        "Please enter the trailing stop loss percentage (as a decimal) (ex 0.25 for 25% stop loss).\n> "))
    cost_basis = float(crypto["cost_bases"][0]["direct_cost_basis"]) / \
        float(crypto["cost_bases"][0]["direct_quantity"])

    # Set default strike price
    crypto_price = float(rh.crypto.get_crypto_quote(ticker)["mark_price"])
    if(crypto_price * stopAmt > cost_basis):
      strike_price = crypto_price * stopAmt
    else:
      strike_price = cost_basis * stopAmt

    counter = 60
    while True:
      try:
        crypto_price = float(rh.crypto.get_crypto_quote(ticker)["mark_price"])
      except:
        counter += 1
        continue
      if(counter >= 60):
        print(str(datetime.datetime.now()) + ":")
        print("CURRENT DOGE PRICE: " + str(crypto_price))
        print("COST BASIS: " + str(cost_basis))
        print("STRIKE PRICE: " + str(strike_price) + "\n")
        counter = 0
      if crypto_price < strike_price:
        # Sell all crypto
        print("CURRENT DOGE PRICE: " + str(crypto_price))
        print("COST BASIS: " + str(cost_basis))
        print("STRIKE PRICE: " + str(strike_price))
        print("SELLING " + amount + " " + ticker.upper())
        # rh.order_sell_crypto_by_quantity(crypto["quantity"])
        break
      # Increase cost basis if price goes up
      elif crypto_price > cost_basis:
        cost_basis = crypto_price
        strike_price = cost_basis * stopAmt
      counter += 1
      sleep(1)
