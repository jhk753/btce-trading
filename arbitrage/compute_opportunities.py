import sys
from objc._objc import NULL
import pylab
import numpy as np
import time
from time import strftime, gmtime

import btceapi

def start_trade(opportunities, tax, init_volume, real_trade, key_file=NULL):
    init_profit = float(1.)
    sum_profit = 0
    for name, opportunity in opportunities.items():
        pairs = [opportunity[0][1], opportunity[1][1], opportunity[2][1]]
        prices, volumes = get_prices_and_volumes(pairs)
        t = str(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
        max_volume, profit = compute_profit_and_volume_for_one_opportunity(opportunity, tax, init_volume, init_profit, prices, volumes)
        if profit-1>0:
            if real_trade:
                trade(opportunity, max_volume, key_file, prices, volumes, tax)
                print "traded: "
            print name + " " + t
            print "profit: " + str(round(profit-1, 3) * 100) + "%"
            print "absolute BTC volume in the end: "+ str(round(max_volume, 3))
            print ""
            sum_profit += (profit-1) * max_volume
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


def trade(opportunity, max_volume, key_file, prices, volumes, tax):
    handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)
    volume = max_volume
    for key in handler.getKeys():
        t = btceapi.TradeAPI(key, handler=handler)
        for operation in opportunity:
            pair = operation[1]
            price = float(prices[operation[0]][operation[1]])
            if operation[0] == "bid":
                results = t.trade(pair, "sell", price, volume)
                volume *= price * tax
            if operation[0] == "ask":
                volume = volume /price
                results = t.trade(pair, "buy", price, volume)
                volume *= tax
