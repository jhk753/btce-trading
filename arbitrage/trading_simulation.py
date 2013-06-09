from __future__ import print_function
from time import strftime, gmtime
import time
import compute_opportunities

f = open('sum_profit_' + str(strftime("%d-%b-%Y-%H-%M-%S", gmtime())) + '.txt','w')
i=0
sum_profit = 0
while True:
    p = compute_opportunities.detect_opportunity()
    sum_profit += p
    print( str(strftime("%d-%b-%Y-%H-%M-%S", gmtime())) + "  " + str(p) + " " + str(sum_profit), file = f)
    time.sleep(1)