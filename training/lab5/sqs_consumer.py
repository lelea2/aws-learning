# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import threading
import time
import order
import utils

QUEUE_NAME = "MySQSQueue_A"
QUEUE_ATTR_NAME = "ApproximateNumberOfMessages"
SLEEP = 10

def Connect2sqs():
    #Connect to SQS service
    return utils.connect2Service('sqs')

#The SQSConsumer class retrieves messages from an SQS queue.
class SQSConsumer (threading.Thread):
    sqs = Connect2sqs()

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("SQSConsumer Thread running!")
        maxRetry = 5
        numMsgs = 0
        maxMsgs = self.getNumberOfMessages()
        count = 0
        print("No. of Messages to consume:", maxMsgs)
        while numMsgs < maxMsgs or count < maxRetry:
            time.sleep(SLEEP)
            numMsgs += self.consumeMessages()
            count += 1
            print("Iteration No.:", count, numMsgs)
        print("SQSConsumer Thread Stopped")

    def getQueue(self, sqsQueueName=QUEUE_NAME):
        queue = None
        try:
            #STUDENT TODO: Get the SQS queue using the SQS resource object and QUEUE_NAME
            queue = self.sqs.get_queue_by_name(QueueName=sqsQueueName)
        except Exception as err:
            print("Error Message {0}".format(err))
        return queue

    def getNumberOfMessages(self):
        numMessages = 0
        try:
            queue = self.getQueue()
            if queue:
                attribs = queue.attributes
                numMessages = int(attribs.get(QUEUE_ATTR_NAME))
        except Exception as err:
            print("Error Message {0}".format(err))
        return numMessages

    def consumeMessages(self, sqsQueueName=QUEUE_NAME):
        numMsgs = 0
        try:
            queue = self.getQueue()
            if queue:
                #STUDENT TODO: Receive messages from the SQS queue by using the receive_messages API method.
                #STUDENT TODO: Enable long polling and set maximum number of messages to 10.
                mesgs = queue.receive_messages(AttributeNames=['All'], MaxNumberOfMessages=10, WaitTimeSeconds=20)
                if not len(mesgs):
                    print("There are no messages in Queue to display")
                    return numMsgs
                for mesg in mesgs:
                    #STUDENT TODO: Retrieve the Attributes of a message.
                    attributes = mesg.attributes
                    senderId = attributes.get('SenderId')
                    sentTimestamp = attributes.get('SentTimestamp')

                    bd = mesg.body
                    orderDict = eval(bd)
                    porder = order.Order(orderDict)
                    #Adds message metadata to Order object.
                    porder.setSenderId(senderId)
                    porder.setSentTimestamp(sentTimestamp)
                    print(porder)

                    self.deleteMessage(queue, mesg)
                    time.sleep(1)
                numMsgs = len(mesgs)
        except Exception as err:
            print("Error Message {0}".format(err))
        return numMsgs

    def deleteMessage(self, queue, mesg):
        try:
            #STUDENT TODO: Delete Message from the SQS queue
            print("Message deleted from Queue")
            mesg.delete()
            return True
        except Exception as err:
            print("Error Message {0}".format(err))
        return False

def main():
    try:
        thread1 = SQSConsumer(1, "Thread-1", 1)
        thread1.start()
    except Exception as err:
        print("Error Message {0}".format(err))
    thread1.join()
    return thread1

if __name__ == '__main__':
    main()
