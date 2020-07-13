from log import logHandler as log
import math

MAX_DECIMALS = 8
REL_SPENDABLE_AMOUNT = 0.006
SAFETY_CORRECTION = 0.04
OVERLAP_CHECK_MULT = 1.8

"""
# OLD pyexp_rounding
def default_pyexp_rounding(number):
    print(number)
    numberExpString = str("{:+e}".format(float(number)))
    print(numberExpString)
    return float(numberExpString)
"""

"""
# another OLD pyexp_rounding
def custom_pyexp_rounding(number):
    # pls don't change it because it seems to be working
    numberExpString = str("{:+e}".format(float(number)))
    exp = int(numberExpString[-2:])
    n = float(numberExpString[0:-5])
    #print('nexp: ' + str(n))
    if exp == 0:
        return n
    elif numberExpString[-3] == '+':
        for i in range(exp):
            n *= 10
    elif numberExpString[-3] == '-':
        for i in range(exp):
            n /= 10
    else:
        raise Exception("custom_pyexp_rounding didn't work properly.")
    return n
"""

def ulterior_rounding_to_n_significant_digits(number, n=5):
    int_part_len = int(math.log10(number) + 1)
    n_digits = n - int_part_len  # a negative result is also ok
    number = round(number, ndigits=n_digits)
    return number

def filter_rounding(number, digit_filter, floor_or_ceil='floor'):
    #print(digit_filter)
    multHelper = 1
    for i in range(MAX_DECIMALS):
        multHelper *= 10
    minFilter = 1 / multHelper
    try:
        digit_filter = float(digit_filter)
    except:
        raise TypeError("Unable to represent digit_filter as a float number.")
    if digit_filter < minFilter:
        raise ValueError(f"filter_rounding first argument needs to be positive and greater than {minFilter}.")
    if floor_or_ceil not in ['floor', 'ceil']:
        raise ValueError("Invalid floor_or_ceil argument in filter_rounding.")
    remainder = number % digit_filter
    # print(number)
    # print(remainder)
    # remainder = int(remainder * multHelper)
    # print(remainder)
    # remainder /= multHelper
    # print(remainder)
    # print(number - remainder)
    filtered_number = number - remainder
    number = ulterior_rounding_to_n_significant_digits(filtered_number)
    #print(number)
    # print(number)
    ## The following rounding system is rather bad... let's leave it out !!!
    #number = int(number * multHelper)
    #print(number)
    ## print(number)
    #number = number / multHelper
    ##print(number)
    if floor_or_ceil == 'ceil' and remainder > minFilter:
        number = int((number + digit_filter) * multHelper) / multHelper
        number = ulterior_rounding_to_n_significant_digits(number)
    # print(f'number = {number}')
    return number


# restrictions and limits still need to be implemented (e.g. max absolute tradable amount and expiring date).
# the cases in which the exchange only allows less than 8 decimals have not been implemented yet.
# also consider the cases in which you can't buy or sell more than a certain amount of a\
#    traded currency (e.g. I have 1000 BTC and I wanna buy 1 billion something).
# what about flipped buy cases?
# tasks different than buy and sell new orders have not been implemented (e.g. cancel orders and so on...)

# the tradable amounts have already been multiplied by the relativeTradableBalance


class BotOneAlgo():

    def __init__(self, simplified_status, market_info):
        self.filters = self.get_filters(market_info)
        self.simplifiedStatus = simplified_status
        self.tasks = []
        self.mandatory_quantity = 0  # PLS NOTICE THAT THE BUY TASK WILL CHANGE IT NO MATTER WHAT
        self.tasks.append(self.get_buy_task(simplified_status))  # THE SELF PART NEEDS TO BE HANDLED CORRECTY
        #try:
        #    self.mandatory_quantity = self.tasks[0]['quantity']
        #except Exception as err:
        #    self.mandatory_quantity = 0
        #    log.raw_log_append(f'Mandatory Quantity not fetched from buy order because not found:\n\t{err.__repr__()}')
        ### Notice that mandatory_quantity has been set by the buy_order task, whether it can be deployed or not.
        self.tasks.append(self.get_sell_task(simplified_status, mandatory_quantity=self.mandatory_quantity))
        log.raw_log_append("Tasks created but not yet performed:")
        for task in self.tasks:
            log.raw_log_append(f'\t{task}')

    def get_tasks(self):
        return self.tasks

    def get_filters(self, market_info):
        filters = {}
        for f in market_info['filters']:
            if f['filterType'] == 'PRICE_FILTER':
                filters['min_price_filter'] = float(f['minPrice'])
            elif f['filterType'] == 'LOT_SIZE':
                filters['min_lot_size'] = float(f['minQty'])
            elif f['filterType'] == 'MIN_NOTIONAL':
                filters['min_notional'] = float(f['minNotional'])
        # print(filters)
        return filters

    def get_buy_task(self, simplified_status, mandatory_quantity=0):
        numOfSellOrders = len(simplified_status["sellOpenOrders"])
        safetyBuyFactor = (1 + SAFETY_CORRECTION * numOfSellOrders)
        amountToBeSpent = float(REL_SPENDABLE_AMOUNT * float(simplified_status["tradableAmounts"][1]) * safetyBuyFactor)
        lastFilledOrderPrice = float(simplified_status["lastFilledOrder"]["price"])  # AS SOON AS YOU EDIT THE CODE, USE SELF.LASTFILLED... IN ORDER TO USE IT EVERYWHERE
        finalBuyAmount = REL_SPENDABLE_AMOUNT * safetyBuyFactor
        price = filter_rounding(
            lastFilledOrderPrice * (1 - finalBuyAmount),
            self.filters['min_price_filter'], 'floor')
        priceIncludingOverlapCheckMult = filter_rounding(
            lastFilledOrderPrice * (1 - finalBuyAmount * OVERLAP_CHECK_MULT),
            self.filters['min_price_filter'], 'floor')
        if mandatory_quantity == 0:
            quantity = filter_rounding(amountToBeSpent / price, self.filters['min_lot_size'], 'floor')
            # THE FOLLOWING IF IS VERY DANGEROUS! DITCH IT IF POSSIBLE
            if price * quantity < self.filters['min_notional']:
                # plan B in case the floor rounding doesn't meet the minimum requirements
                quantity = filter_rounding(amountToBeSpent / price, self.filters['min_lot_size'], 'ceil')
        else:
            quantity = mandatory_quantity
        self.mandatory_quantity = quantity  # PLS NOTICE THIS LINE!!! THERE IS A SELF!!! IT WILL BE USED IN THE SELL TASK ORDER AS WELL!!!
        for boo in simplified_status["buyOpenOrders"]:
            if float(boo["price"]) >= priceIncludingOverlapCheckMult:
                return {"taskType": "nullTask"}
        task = {"taskType": "createOrder", "side": "buy", "price": price, "quantity": quantity}
        return task

    def get_sell_task(self, simplified_status, mandatory_quantity=0):
        numOfBuyOrders = len(simplified_status["buyOpenOrders"])
        safetySellFactor = (1 + SAFETY_CORRECTION * numOfBuyOrders)
        amountToBeSpent = float(REL_SPENDABLE_AMOUNT * float(simplified_status["tradableAmounts"][0]) * safetySellFactor)
            # PLS NOTICE THAT THE LINE ABOVE IS USELESS BECAUSE THE MANDATORY QUANTITY IS ALWAYS FORCED IN THIS CODE
        lastFilledOrderPrice = float(simplified_status["lastFilledOrder"]["price"])
        finalSellAmount = REL_SPENDABLE_AMOUNT * safetySellFactor
        price = filter_rounding(
            lastFilledOrderPrice / (1 - finalSellAmount),
            self.filters['min_price_filter'], 'ceil')
        priceIncludingOverlapCheckMult = filter_rounding(
            lastFilledOrderPrice / (1 - finalSellAmount * OVERLAP_CHECK_MULT),
            self.filters['min_price_filter'], 'ceil')
        for soo in simplified_status["sellOpenOrders"]:
            if float(soo["price"]) <= priceIncludingOverlapCheckMult:
                return {"taskType": "nullTask"}
        if mandatory_quantity == 0:
            quantity = filter_rounding(amountToBeSpent, self.filters['min_lot_size'], 'floor')
        else:
            quantity = mandatory_quantity
        # all the parts with quantity, mandatory quantity and self.quantitystuff needs to be rewritten!!!!!!!!
        # quantity = filter_rounding(amountToBeSpent, self.filters['min_lot_size'], 'floor')
        # quantity = round_to_n_decimals(amountToBeSpent * price, 'ceil')
        task = {"taskType": "createOrder", "side": "sell", "price": price, "quantity": quantity}
        return task


"""
    Alternative implementation with flipped buy statuses
    
    def get_flipped_buy_task(self, simplified_status):
        ...

    def get_flipped_simplified_status(self, simplified_status):
        flippedSimplifiedStatus = {}
        flippedSimplifiedStatus["tradableAmounts"] = simplified_status["tradableAmounts"].reverse()
        flippedSimplifiedStatus["buyOpenOrders"] = []
        flippedSimplifiedStatus["sellOpenOrders"] = []
        for oo in simplified_status["buyOpenOrders"]:
            flippedSimplifiedStatus["sellOpenOrders"].append()
            
    def get_sell_task(self, simplified_status):
        flippedSimplifiedStatus = self.get_flipped_simplified_status(simplified_status)
        flippedBuyTask = self.get_buy_task(flippedSimplifiedStatus)
        sellTask = self.get_flipped_buy_task(flippedBuyTask)
        return sellTask
"""
