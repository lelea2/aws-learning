# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest, warnings
import time, sys

import utils
import sns_publisher
import sqs_consumer

QUEUE_NAME = "MySQSQueue_A"
QUEUE_ATTR_NAME = "ApproximateNumberOfMessages"

SLEEP = 10

def Connect2sqs():
    #Connect to SQS service
    return utils.connect2Service('sqs')


class SqsSnsTest(unittest.TestCase):

    def test(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
            initialNumMessages = self.getNumberOfMessages()

            sns_publisher.main()
            numAfterSnsPublisher = self.getNumberOfMessages()

            thread1 = sqs_consumer.main()
            thread1.join()
            numAfterSQSConsumer = self.getNumberOfMessages()

            print("SqsSnsTest: initialNumMessages: {0}; numAfterSnsPublisher: {1}; numAfterSQSConsumer {2}".format(
                    initialNumMessages, numAfterSnsPublisher, numAfterSQSConsumer))

            if ((numAfterSnsPublisher <= initialNumMessages) or (initialNumMessages != numAfterSQSConsumer)):
                self.fail("SqsSnsTest failed. Number of messages in queue not as expected.")
        except Exception as err:
            print("Error Message {0}".format(err))
            sys.exit(1)

    def getQueue(self, sqsQueueName=QUEUE_NAME):
        #STUDENT TODO: Get the SQS queue using the SQS resource object and QUEUE_NAME
        queue = None
        try:
            sqs = Connect2sqs()
            queue = sqs.get_queue_by_name(QueueName=sqsQueueName)
        except Exception as err:
            print("Error Message {0}".format(err))
        return queue

    def getNumberOfMessages(self, sqsQueueName=QUEUE_NAME):
        numMessages = 0
        try:
            print("Thread sleeping for a few seconds")
            time.sleep(SLEEP)
            print("... Thread running.")
            queue = self.getQueue(sqsQueueName)
            if queue:
                attribs = queue.attributes
                numMessages = int(attribs.get(QUEUE_ATTR_NAME))
        except Exception as err:
            print("Error Message {0}".format(err))
        return numMessages

if __name__ == '__main__':
    unittest.main()
