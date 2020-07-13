class MarketSymbol:

    def __init__(self, tradedCurrency, mainCurrency, tcRelativeTradableAmount, mcRelativeTradableAmount, needsRestart=False, isActive=True):
        self.tradedCurrency = tradedCurrency
        self.mainCurrency = mainCurrency
        self.tcRelativeTradableAmount = tcRelativeTradableAmount
        self.mcRelativeTradableAmount = mcRelativeTradableAmount
        self.needsRestart = needsRestart
        self.isActive = isActive
        pass