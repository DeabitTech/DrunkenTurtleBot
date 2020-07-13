from time import time
from time import sleep
from datetime import datetime

from status import Status
from helpers.idHandler import *
from log import logHandler as log




class MarketManager:

    def __init__(self):

        """
        #old code:
        with open(paths.clientConfig, 'r') as f:
            jsonClientConfig = json.load(f)
        self.clientData = jsonClientConfig[client_name]
        """

        try:
            self._get_markets_buffer_from_json()
            self._markets_buffer_format_check()
            self._remove_inactive_markets_from_buffer()
            self._make_all_first_of_the_session()
            self._markets_buffer_amounts_splitting()
        except Exception as err:
            raise err.__repr__()

        #?# RESTRICTIONS TO BE IMPLEMENTED MAYBE HERE? MAYBE IN STATUS?

        #?# statuses = [] # [ID, runningOrClosed, crashingInfo, *args]

        self.len = len(self.marketsBuffer)
        self.cursorPosition = 0

        self.current = self.CurrentMarket()

    class CurrentMarket:

        def __init__(self):
            self.marketData = MarketManager().marketsBuffer[MarketManager().cursorPosition]

            self.tradedAssetSymbol = self.marketData["tradedCurrency"]["symbol"]
            self.mainAssetSymbol = self.marketData["mainCurrency"]["symbol"]
            self.tradedAssetTradablePortion = self.marketData["tradedCurrency"]["tradablePortion"]
            self.mainAssetTradablePortion = self.marketData["mainCurrency"]["tradablePortion"]

            self.symbolString = self.tradedAssetSymbol + self.mainAssetSymbol
            self.symbolD = {'symbol': self.symbolString}

            self.needsRestart = self.marketData["needsRestart"]
            self.isFirstOfTheSession = self.marketData["isFirstOfTheSession"]

    def set_next_to_current(self):
        self.cursorPosition = (self.cursorPosition + 1) % self.len
        self.current = self.CurrentMarket()

    def _get_markets_buffer_from_json(self):
        with open(paths.marketsConfig, 'r') as f:
            self.marketsBuffer = json.load(f)
        #for key in jsonConfigKeysToOverride:
        #    jsonSessionConfig[key] = jsonConfigKeysToOverride[key]

    def _markets_buffer_format_check(self):
        if type(self.marketsBuffer) is not list:
            raise TypeError("marketsBuffer must be a list.")
        tc, mc = "tradedCurrency", "mainCurrency"
        sym, rta = "symbol", "tradablePortion"
        for m in self.marketsBuffer:
            if not 0 <= m[tc][rta] <= 1 \
                    or not 0 <= m[mc][rta] <= 1:
                err = "tradablePortion numbers must be int or float between 0 and 1"
                log.event_log_append("Session crashed.\n", log.tab, err)
                raise ValueError(err)
        log.event_log_append("markets_buffer_format_check OK.")

    def _remove_inactive_markets_from_buffer(self):
        newMarketsBuffer = []
        for m in self.marketsBuffer:
            if m["isActive"]:
                newMarketsBuffer.append(m)
        log.event_log_append("Inactive markets removed from buffer. The current marketsBuffer is:\n", log.tab, newMarketsBuffer)
        self.marketsBuffer = newMarketsBuffer

    def _make_all_first_of_the_session(self):
        for m in self.marketsBuffer:
            m["isFirstOfTheSession"] = True

    def _markets_buffer_amounts_splitting(self):
        tc, mc = "tradedCurrency", "mainCurrency"
        sym, rta = "symbol", "tradablePortion"
        tmpDict0 = {}
        for m in self.marketsBuffer:
            tmpDict0[m[tc][sym]] = 0
            tmpDict0[m[mc][sym]] = 0
        tmpDict1 = tmpDict0.copy()
        for m in self.marketsBuffer:
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
        for i in range(0, len(self.marketsBuffer)):
            if self.marketsBuffer[i][tc][rta] == 0:
                self.marketsBuffer[i][tc][rta] = tmpDict1[self.marketsBuffer[i][tc][sym]]
            if self.marketsBuffer[i][mc][rta] == 0:
                self.marketsBuffer[i][mc][rta] = tmpDict1[self.marketsBuffer[i][mc][sym]]
        #print(marketsBuffer)
        log.event_log_append("After splitting the tradablePortion, marketBuffer is:\n", log.tab, self.marketsBuffer)


