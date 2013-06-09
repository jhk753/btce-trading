import sys
import pylab
import numpy as np
import time
from time import strftime, gmtime

import btceapi

def start_trade():

    pairs = ["btc_usd", "btc_eur", "btc_rur", "ltc_btc", "ltc_usd", "ltc_rur", "eur_usd", "usd_rur"]

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


    t = str(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

    prices, volumes = get_prices_and_volumes(pairs)

    sum_profit = test_all_opportunities(opportunities, prices, volumes, t)

    return sum_profit


def get_prices_and_volumes(pairs):

    prices = {"bid": {}, "ask": {}}
    volumes ={"bid": {}, "ask": {}}

    for pair in pairs:
        asks, bids = btceapi.getDepth(pair)

        a_p, a_v = zip(*asks)
        b_p, b_v = zip(*bids)

        prices["ask"][pair] = a_p[0]
        volumes["ask"][pair] = a_v[0]
        prices["bid"][pair] = b_p[0]
        volumes["bid"][pair] = b_v[0]

    return prices, volumes

def test_all_opportunities(opportunities, prices, volumes, t):
    num = 0
    sum_profit = 0
    for name, opportunity in opportunities.items():
        profit = float(1.)
        tax = float(0.998)
        init_volume = 100

        max_volume, profit = compute_profit_and_volume_for_one_opportunity(opportunity, tax, init_volume, profit, prices, volumes)

        if profit-1>0:
            num+=1
            print name + " " + t
            print "profit: " + str(round(profit-1, 3) * 100) + "%"
            print "absolute BTC volume in the end: "+ str(round(max_volume, 3))
            print ""
            sum_profit += (profit-1) * max_volume
    return sum_profit


def compute_profit_and_volume_for_one_opportunity(opportunity, tax, max_volume, profit, prices, volumes):
    for operation in opportunity:
            profit *= tax
            price = float(prices[operation[0]][operation[1]])
            volume = float(volumes[operation[0]][operation[1]])
            if operation[0] == "bid":
                profit *= price
                max_volume = min(volume, max_volume) * price * tax
            if operation[0] == "ask":
                profit /= price
                max_volume = min(volume, max_volume) / price * tax

    max_volume /= (tax * tax * tax)
    return max_volume, profit