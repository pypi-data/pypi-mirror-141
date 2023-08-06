from tkinter import SEL
from ib_insync import *
import pandas as pd


class ib:
    def __init__(self, settingParameter) -> None:
        self.IB = IB()
        self.SettingModel = settingParameter
        self.initib()

    def initib(self):
        connectMsg = None
        try:
            connectMsg = self.IB.connect(
                self.SettingModel['ip'], self.SettingModel['port'], clientId=self.SettingModel['clientId'])
        except Exception as ex:
            print('connect error:', ex)
        return connectMsg

    def accountSummary(self):
        try:
            account_summary = self.IB.accountSummary(
                account=self.SettingModel['account'])
        except Exception as ex:
            print('get accountSummary data error:', ex)

        account_summary_df = pd.DataFrame(account_summary).set_index('tag')
        return account_summary_df

    def getAvailableFunds(self):
        availableFunds = None
        try:
            availableFunds = self.accountSummary().loc['AvailableFunds']
        except Exception as ex:
            print('getAvailableFunds error:', ex)
        return availableFunds

    def getGrossPositionValue(self):
        grossPositionValue = None
        try:
            grossPositionValue = self.accountSummary(
            ).loc['GrossPositionValue']
        except Exception as ex:
            print('getGrossPositionValue error:', ex)
        return grossPositionValue

    def getNetLiquidation(self):
        netLiquidation = None
        try:
            netLiquidation = self.accountSummary().loc['NetLiquidation']
        except Exception as ex:
            print('getNetLiquidation error:', ex)
        return netLiquidation

    def createOrder(self, contractParameters, orderParameters):
        placeOrderData = None
        try:
            contract = Contract()
            contract.symbol = contractParameters['symbol']
            contract.secType = contractParameters['secType']
            contract.exchange = contractParameters['exchange']
            contract.currency = contractParameters['currency']

            order = Order()
            order.action = orderParameters['action']
            order.totalQuantity = orderParameters['totalQuantity']
            order.orderType = orderParameters['orderType']
            if'orderType' in orderParameters and orderParameters['orderType'] == 'LMT':
                if 'lmtPrice' in orderParameters:
                    order.lmtPrice = orderParameters['lmtPrice']

            if 'orderId' in orderParameters:
                order.orderId = orderParameters['orderId']
            print(order)
            placeOrderData = self.IB.placeOrder(contract, order)
        except Exception as ex:
            print('create_order error', ex)
        return placeOrderData

    def getOrderSatus(self):
        orderStatusDF = None
        try:
            orderStatusList = self.IB.executions()
            if len(orderStatusList) != 0:
                orderStatusDF = pd.DataFrame(orderStatusList)
        except Exception as ex:
            print('getorderSatus error:', ex)
        return orderStatusDF

    def getNotDealOrderStauts(self):
        notDealOrderStatusDF = None
        try:
            notDealOrderStatusList = self.IB.openTrades()
            print('notDealOrderStatusList', notDealOrderStatusList)
            if len(notDealOrderStatusList) != 0:
                notDealOrderStatusDF = pd.DataFrame(notDealOrderStatusList)
        except Exception as ex:
            print('getnotdealorderstauts error:', ex)
        return notDealOrderStatusDF

    def cancelOrder(self, orderId):
        try:
            order = Order(
                orderId=orderId
            )
            response = self.IB.cancelOrder(order)
        except Exception as ex:
            print('cancel_order error :', ex)
        return response
