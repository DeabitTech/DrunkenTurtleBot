from binanceWrapper.client import *
from helpers import customEncrypter
from helpers import paths
from helpers.idHandler import ID
from botOneAlgo import BotOneAlgo
from log import logHandler as log

from datetime import datetime
from time import sleep
from time import time
import json
from operator import itemgetter


"""
old code....
    __slots__ = [accountID, statusID, connectionCheck = False,
                 timestampAsLocalUTC, timestampAsBinanceUTC,
                 runningBots, mainCurrencySymbol, secondaryCurrencySymbol,
                 mainCurrencyAvailableBalance, secondaryCurrencyAvailableBalances,
                 equivalentCoupleCurrenciesBalanceInBTC,
                 currentOpenOrders, attemptedNewOrders, newOrdersPlacingSuccess = False,
                 errors = 'None']
                #runinningBots takes as value an array of botIDs
"""

class LastFilledOrderError(Exception):
    pass


DEFAULT_WAIT = 0.3


class Status:

    def __init__(self, client_name, market_data, run=True, allow_order_placing=True, password='', *args):
        self.clientName = client_name
        self.run = run
        self.allow_order_placing = allow_order_placing
        logMessage = f'\n\nStatus called with "{self.clientName}" credentials and run = {run}'
        log.event_log_append(logMessage)
        log.raw_log_append(logMessage)
        #self.rawLogHeader = ['status full ID', 'status partial ID']
        if self.run:
            self.statusID = ID("status")
            self.market = market_data()
            """
            self.marketData = market_data
            self.tradedCurrency = market_data["tradedCurrency"]["symbol"]
            self.mainCurrency = market_data["mainCurrency"]["symbol"]
            self.marketSymbol = self.tradedCurrency + self.mainCurrency
            self.marketSymbolDict = {'symbol': self.marketSymbol}
            """

            self.localTimestamp = int(time())
            self.localDateTime = datetime.fromtimestamp(self.localTimestamp)

            logMessage = f'{self.localDateTime}\tstatus started with status ID: {self.statusID.partialID}.\n{self.market.symbolString}\t{self.statusID.fullID}'
            log.event_log_append(logMessage)
            log.raw_log_append(logMessage)

            self.wait = DEFAULT_WAIT

            with open(paths.clientConfig, 'r') as f:
                client_data = json.load(f)
            client_data = client_data['clientNames'][self.clientName]
            if client_data["api_key"]["isEncrypted"]:
                api_key = customEncrypter.decrypt(client_data["api_key"]["value"], password)
            else:
                api_key = client_data["api_key"]["value"]
            if client_data["api_key"]["isEncrypted"]:
                api_secret = customEncrypter.decrypt(client_data["api_secret"]["value"], password)
            else:
                api_secret = client_data["api_secret"]["value"]

            self.client = Client(api_key, api_secret)

            logMessage = f'{self.localDateTime}\t-\t{self.localTimestamp}\t-\tapi keys successfully fetched.'
            log.event_log_append(logMessage)
            log.raw_log_append(logMessage)

            self.serverTime = int(int(self.getServerTime()["serverTime"]) / 1000)
            sleep(self.wait)

            logMessage = f'ServerTime:\t{self.serverTime}'
            log.event_log_append(logMessage)
            log.raw_log_append(logMessage)

            if self.market.needsRestart == True:
                self.openOrders = self.cancelAllOpenOrders()
                self.market.needsRestart = False
                log.event_log_append("NEEDS_RESTART WAS TRUE BUT THE CODE ISN'T READY FOR THAT!!!!")
                # check the whole code and remember to update marketsBuffer.. it probably doesn't work now.
                # print log stuff
                # restore log config file
                return

            self.openOrders = []
            self.get_open_orders(fromServer=True)
            sleep(self.wait)

            self.lastFilledOrder = self.getLastFilledOrder()
            sleep(self.wait)

            self.accountInfo = self.client.get_account()
            self.freeBalances = self.getFreeBalances()
            self.totalBalances = self.getTotalBalances()
            sleep(self.wait)

            self.market_info = self.client.get_symbol_info(self.market.symbolString)
            sleep(self.wait)

            logMessage = f'MarketData:\t{self.market.marketData}\nFree Balances:\t{self.freeBalances}\nTotalBalances:\t{self.totalBalances}'
            log.raw_log_append(logMessage)

            self.simplifiedStatus = self.getSimplifiedStatus()
            log.raw_log_append("Simplified Status:\n", self.getPrintableSimplifiedStatus())

            botOneProcessor = BotOneAlgo(self.simplifiedStatus, self.market_info)
            self.tasksList = botOneProcessor.get_tasks()

            log.raw_log_append("New Orders:")
            print(f'TasksList: {self.tasksList}')
            for task in self.tasksList:
                if self.allow_order_placing:
                    try:
                        if task["taskType"] == "createOrder":
                            self.client.create_order(**self.market.symbolD,  type='limit', timeInForce='GTC', side=task["side"], quantity=task["quantity"], price=task["price"])
                            log.new_orders_log_csv_append(self.get_list_of_new_orders_log_csv_variables(task))
                            log.raw_log_append(f'\tprice:\t{task["price"]}\tquantity:\t{task["quantity"]}')
                    except Exception as err:
                        log.raw_log_append(f'Task not found or incorrectly formatted. Skipping this step...\n\t{err.__repr__()}')

            sleep(self.wait)

            log.raw_log_append(f'Total Balance in Main Currency:\t\t', self.getTotalEquivalentBalanceInMainCurrency())

            sleep(self.wait)


    def getServerTime(self):
        return self.client.get_server_time()

    def getMarketData(self):
        return self.market.marketData

    def get_open_orders(self, fromServer=False):
        if fromServer:
            self.openOrders = self.client.get_open_orders(**self.market.symbolD)
        return self.openOrders

    def cancelAllOpenOrders(self):
        try:
            self.client.cancel_all_open_orders(**self.market.symbolD)
        except:
            oos = self.client.get_open_orders(**self.market.symbolD)
            for oo in oos:
                self.client.cancel_order(**self.market.symbolD, orderId=oo["orderId"])
                sleep(self.wait)
        self.openOrders = self.client.get_open_orders(**self.market.symbolD)

    def getLastFilledOrder(self):
        allOrders = self.client.get_all_orders(**self.market.symbolD)
        lastOrder = {}
        if len(allOrders) != 0:
            for order in allOrders:
                if order.get("status") == 'FILLED':
                    if lastOrder.get("updateTime") == None:
                        lastOrder = order
                    elif float(lastOrder.get("updateTime")) < float(order.get("updateTime")):
                        lastOrder = order
        if lastOrder == {}:
            raise LastFilledOrderError("Unable to fetch a last filled order. In order for the bot to work properly, "
                                       "at least 1 among the last 500 orders must belong to this market symbol and "
                                       "must be completely filled.")
        return lastOrder

    def getFreeBalances(self):
        fb = [0, 0]
        for a in self.accountInfo["balances"]:
            if a["asset"] == self.tradedCurrency:
                fb[0] = float(a["free"])
            elif a["asset"] == self.mainCurrency:
                fb[1] = float(a["free"])
        return fb

    def getTotalBalances(self):
        tb = [0, 0]
        for a in self.accountInfo["balances"]:
            if a["asset"] == self.tradedCurrency:
                tb[0] = float(a["free"]) + float(a["locked"])
            elif a["asset"] == self.mainCurrency:
                tb[1] = float(a["free"]) + float(a["locked"])
        return tb

    def getSimplifiedStatus(self):
        simpStat = {"tradableAmounts": [0, 0], "buyOpenOrders": [], "sellOpenOrders": [], "lastFilledOrder": {}}
        simpStat["tradableAmounts"][0] = float(self.marketData["tradedCurrency"]["tradablePortion"]) * float(self.freeBalances[0])
        simpStat["tradableAmounts"][1] = float(self.marketData["mainCurrency"]["tradablePortion"]) * float(self.freeBalances[1])
        for oo in self.openOrders:
            if oo["side"] == "BUY":
                simpStat["buyOpenOrders"].append({"price": oo["price"], "origQty": oo["origQty"]})
                print(simpStat["buyOpenOrders"])
            if oo["side"] == "SELL":
                simpStat["sellOpenOrders"].append({"price": oo["price"], "origQty": oo["origQty"]})
                print(simpStat["sellOpenOrders"])
        simpStat["buyOpenOrders"] = sorted(simpStat["buyOpenOrders"], key=itemgetter("price"))
        simpStat["sellOpenOrders"] = sorted(simpStat["sellOpenOrders"], key=itemgetter("price"))
        simpStat["lastFilledOrder"] = {"price": self.lastFilledOrder["price"], "origQty": self.lastFilledOrder["origQty"]}
        return simpStat

    def getPrintableSimplifiedStatus(self):
        string = ''
        string += f'\tTradable amounts:\n'
        for ik in self.simplifiedStatus["tradableAmounts"]:
            string += f'\t\t{ik}\n'
        string += f'\tBuy Open Orders:\n'
        for ik in self.simplifiedStatus["buyOpenOrders"]:
            string += f'\t\t{ik}\n'
        string += f'\tLast Filled Order:\n'
        string += f'\t\t{self.simplifiedStatus["lastFilledOrder"]}\n'
        string += f'\tSell Open Orders:\n'
        for ik in self.simplifiedStatus["sellOpenOrders"]:
            string += f'\t\t{ik}'
        return string

    def getTotalEquivalentBalanceInMainCurrency(self):
        tickerPrice = float(self.client.get_ticker(**self.marketSymbolDict)["lastPrice"])
        return self.totalBalances[0] * tickerPrice + self.totalBalances[1]

    def get_list_of_new_orders_log_csv_variables(self, task):
        list = []
        list.append(self.localDateTime)
        list.append(self.statusID.fullID)
        list.append(self.marketSymbol)
        list.append(task["side"])
        list.append(task["quantity"])
        list.append(task["price"])
        list.append(self.freeBalances[0])
        list.append(self.freeBalances[1])
        list.append(self.totalBalances[0])
        list.append(self.totalBalances[1])
        list.append(self.getTotalEquivalentBalanceInMainCurrency())
        list.append(len(self.simplifiedStatus["buyOpenOrders"]))
        list.append(len(self.simplifiedStatus["sellOpenOrders"]))
        return list

"""
STUFF TO IMPLEMENT LATE ON !!!!!!!!
get_account_status
get_symbol_info ... MIN_NOTIONAL and stuff...
"""
