import argparse
import time
import datetime

# Interactive Brokers API
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *

from logger import Logger

logger = Logger('log/ibclient.out')

class IBClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        self.done = False

class IBWrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

class IBClientApp(IBWrapper, IBClient):
    def __init__(self):
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)
        self.lastHour = 0

    def setTickManager(self, tickManager):
        self.tickManager = tickManager

    def create_contract(this, symbol):
        contract = Contract()
        contract.secType = "FUT"
        contract.exchange = "NYMEX"
        contract.currency = "USD"
        contract.localSymbol = symbol
        return contract

    def requestMarketData(self, symbol):
        contract = self.create_contract( symbol )
        self.reqMktData( 1000, contract, "", False, None )
        time.sleep(1)

    @iswrapper
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        # From TickTypeEnum
        # 0 	BID_SIZE
        # 1 	BID
        # 2 	ASK
        # 3 	ASK_SIZE
        # 4 	LAST
        # 5 	LAST_SIZE
        # 8 	VOLUME

        if (tickType == 1):
            logger.debug("BID = %s" % str(price))
        elif (tickType == 2):
            logger.debug("ASK = %s" % str(price))
        elif (tickType == 4):
            logger.debug("LAST = %s" % str(price))

    @iswrapper
    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)

        # From TickTypeEnum - TODO: Anyway to get value from enum?
        # 0 	BID_SIZE
        # 1 	BID
        # 2 	ASK
        # 3 	ASK_SIZE
        # 4 	LAST
        # 5 	LAST_SIZE
        # 8 	VOLUME

        if (tickType == 5):
            logger.debug("LAST_SIZE = %s" % str(size))
        elif (tickType == 8):
            logger.debug("VOLUME = %s" % str(size))

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        super().error(reqId, errorCode, errorString)
        logger.error("Error msg: %s" % errorString)

    @iswrapper
    def updateAccountTime(self, timeStamp:str):
        super().updateAccountTime(timeStamp)
        logger.debug("updateAccountTime: %s" % timeStamp)

    @iswrapper
    def connectAck(self):
        logger.debug("connectAck")

    @iswrapper
    def disconnect(self):
        super().disconnect()
        logger.debug("disconnect")

def main():
    logger.debug("Start time is %s" % datetime.datetime.now())

    try:
        app = IBClientApp()
        app.connect("127.0.0.1", 4001, clientId=0)
        if( app.isConnected() ):
            logger.debug("ServerVersion:%s connectionTime:%s" % (app.serverVersion(), app.twsConnectionTime()))

            # Request tick data for WTI Crude futures contract (May 2017)
            symbol = 'CLK7'

            app.requestMarketData(symbol)
            app.run()
        else:
            logger.error("App failed to connect to IB gateway")

    except:
        raise

if __name__ == "__main__":
    main()
