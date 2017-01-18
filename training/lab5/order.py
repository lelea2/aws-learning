# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

#The Order class is a simple Python class used to hold order information.
class Order:
    def __init__(self, orderDict=None):
        self.orderId, self.orderDate, self.orderDetails = 0, "", ""
        self.senderId, self.sentTimestamp = "", ""
        if orderDict:
            if orderDict.get('orderId') and orderDict.get('orderDate') and orderDict.get('orderDetails'):
                self.orderId = orderDict['orderId']
                self.orderDate = orderDict['orderDate']
                self.orderDetails = orderDict['orderDetails']

    def getOrderId(self):
        return self.orderId

    def setOrderId(self, orderId):
        self.orderId = orderId

    def getOrderDate(self):
        return self.orderDate

    def setOrderDate(self, orderDate):
        self.orderDate = orderDate

    def getOrderDetails(self):
        return self.orderDetails

    def setOrderDetails(self, orderDetails):
        self.orderDetails = orderDetails

    def getSenderId(self):
        return self.senderId

    def setSenderId(self, senderId):
        self.senderId = senderId

    def getSentTimestamp(self):
        return self.sentTimestamp

    def setSentTimestamp(self, sentTimestamp):
        self.sentTimestamp = sentTimestamp

    def __repr__(self):
        rval = " orderId: %d,\n senderId: %s,\n sentTimestamp: %s,\n orderDate: %s,\n orderDetails: %s\n" %(
                    self.orderId, self.senderId, self.sentTimestamp, self.orderDate, self.orderDetails
                    )
        return rval

def jdefault(obj):
    return obj.__dict__
