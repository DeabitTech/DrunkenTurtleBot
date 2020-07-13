from time import time
from time import sleep
from datetime import datetime

from managers.marketsManager import MarketManager
from status import Status
from helpers.idHandler import *
from log import logHandler as log


DEFAULT_WAIT = 36
MAX_WAIT = 10000
WAIT_MULTIPLIER_0 = 1.2

"""
def markets_buffer_format_check(marketsBuffer):
    if type(marketsBuffer) is not list:
        raise TypeError("marketsBuffer must be a list.")
    tc, mc = "tradedCurrency", "mainCurrency"
    sym, rta = "symbol", "tradablePortion"
    for m in marketsBuffer:
        if not 0 <= m[tc][rta] <= 1 \
                or not 0 <= m[mc][rta] <= 1:
            err = "tradablePortion numbers must be int or float between 0 and 1"
            log.event_log_append("Session crashed.\n", log.tab, err)
            raise ValueError(err)
    log.event_log_append("markets_buffer_format_check OK.")

def remove_inactive_markets_from_buffer(marketsBuffer):
    newMarketsBuffer = []
    for m in marketsBuffer:
        if m["isActive"]:
            newMarketsBuffer.append(m)
    log.event_log_append("Inactive markets removed from buffer. The current marketsBuffer is:\n", log.tab, newMarketsBuffer)
    return newMarketsBuffer

def marketsBufferAmountsSplitting(marketsBuffer):
    tc, mc = "tradedCurrency", "mainCurrency"
    sym, rta = "symbol", "tradablePortion"
    tmpDict0 = {}
    for m in marketsBuffer:
        tmpDict0[m[tc][sym]] = 0
        tmpDict0[m[mc][sym]] = 0
    tmpDict1 = tmpDict0.copy()
    for m in marketsBuffer:
        if m[tc][rta] == 0:
            tmpDict0[m[tc][sym]] += 1
        else:
            tmpDict1[m[tc][sym]] += m[tc][rta]
        if m[mc][rta] == 0:
            tmpDict0[m[mc][sym]] += 1
        else:
            tmpDict1[m[mc][sym]] += m[mc][rta]
    for tm in tmpDict0:
        try:
            tmpDict1[tm] = int((1 - tmpDict1[tm]) / tmpDict0[tm] * 1000) / 1000
        except ZeroDivisionError:
            pass
    for tm in tmpDict1:
        if tmpDict1[tm] < 0:
            err = "The sum of the of all the tradablePortions related to a symbol of an active "\
                    "market must not be greater than 1."
            log.event_log_append('Session crashed.\n', log.tab, err)
            raise ValueError(err)
    #print(tmpDict1)
    #print(tmpDict1[marketsBuffer[0][tc][sym]])
    for i in range(0, len(marketsBuffer)):
        if marketsBuffer[i][tc][rta] == 0:
            marketsBuffer[i][tc][rta] = tmpDict1[marketsBuffer[i][tc][sym]]
        if marketsBuffer[i][mc][rta] == 0:
            marketsBuffer[i][mc][rta] = tmpDict1[marketsBuffer[i][mc][sym]]
    #print(marketsBuffer)
    log.event_log_append("After splitting the tradablePortion, marketBuffer is:\n", log.tab, marketsBuffer)
    return marketsBuffer
"""


class Session:

    def __init__(self, clientName, run=True):

        self.clientName = clientName
        self.isrunning = run
        self.localTimestamp = time()
        self.localDateTime = datetime.fromtimestamp(self.localTimestamp)

        logMessage = f'\n\n{self.localDateTime}\nSession created with "{self.clientName}" credentials and run = {run}'
        log.event_log_append(logMessage)
        log.raw_log_append(logMessage)

        # RESTRICTIONS TO BE IMPLEMENTED... WHERE?

        # statuses = [] # [ID, runningOrClosed, crashingInfo, *args]

        self.market = MarketManager()
        self.wait = DEFAULT_WAIT

        if self.isrunning:
            self.sessionID = ID("session")
            logMessage = f'Session has started with session ID: {self.sessionID.partialID}.\n'
            log.event_log_append(logMessage)
            log.raw_log_append(logMessage)

        while self.isrunning:
            log.event_log_append('\nCurrent marketsBuffer = ', self.market.marketsBuffer)
            try:
                self.newStatus = Status(self.clientName, self.market.current())
                self.wait = DEFAULT_WAIT
            except IDOverflowError or IndexError:
                self.statusIDReset = ID("status", getNew=False, reset=True)
                self.isrunning = False
                logMessage = f'\nSession terminated for statusID overflow.\n'
                log.event_log_append(logMessage)
                log.raw_log_append(logMessage)
                break
            """
            except Exception as err:
                if self.wait < MAX_WAIT: self.wait *= WAIT_MULTIPLIER_0
                logMessage = f'\nStatus crashed with error:\n    {err.__repr__()}\n'
                log.event_log_append(logMessage)
                log.raw_log_append(logMessage)
            """

            self.market.set_next_to_current()

            """
            #if newStatus.getMarketData() is different from marketData, update sessionConfig.json
            try: self.lastMarket = newStatus.getMarketData()
            except: self.lastMarket = self.marketsBuffer[0]
            if len(self.marketsBuffer) > 1:
                self.marketsBuffer = self.marketsBuffer[1:]
                self.marketsBuffer.append(self.lastMarket)
            """

            sleep(self.wait)