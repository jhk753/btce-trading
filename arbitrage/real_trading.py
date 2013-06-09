from __future__ import print_function
from time import strftime, gmtime
import time
import compute_opportunities
import sys

if len(sys.argv) < 2:
    print("Usage: print-trans-history.py <key file>")
    print("    key file - Path to a file containing key/secret/nonce data")
    sys.exit(1)

key_file = sys.argv[1]


f = open('sum_profit_' + str(strftime("%d-%b-%Y-%H-%M-%S", gmtime())) + '.txt','w')
i=0
sum_profit = 0

opportunities = {
        "btc -> eur -> usd -> btc": [["bid", "btc_eur"], ["bid", "eur_usd"], ["ask", "btc_usd"]],
        "btc -> usd -> eur -> btc": [["bid", "btc_usd"], ["ask", "eur_usd"], ["ask", "btc_eur"]],
        "btc -> ltc -> usd -> btc": [["ask", "ltc_btc"], ["bid", "ltc_usd"], ["ask", "btc_usd"]],
        "btc -> usd -> ltc -> btc": [["bid", "btc_usd"], ["ask", "ltc_usd"], ["bid", "ltc_btc"]],
        "btc -> rur -> usd -> btc": [["bid", "btc_rur"], ["ask", "usd_rur"], ["ask", "btc_usd"]],
        "btc -> usd -> rur -> btc": [["bid", "btc_usd"], ["bid", "usd_rur"], ["ask", "btc_rur"]],
        "btc -> rur -> ltc -> btc": [["bid", "btc_rur"], ["ask", "ltc_rur"], ["bid", "ltc_btc"]],
        "btc -> ltc -> rur -> btc": [["ask", "ltc_btc"], ["bid", "ltc_rur"], ["ask", "btc_rur"]]
    }

tax = float(0.998)
init_volume = 100


while True:
    p = compute_opportunities.start_trade(opportunities, tax, init_volume, True, key_file)
    sum_profit += p
    if p>0:
        print( str(strftime("%d-%b-%Y-%H-%M-%S", gmtime())) + "  " + str(p) + " " + str(sum_profit), file = f)
    time.sleep(1)