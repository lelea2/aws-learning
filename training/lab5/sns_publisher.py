# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import json
import utils
import order

#The SNSPublisher class publishes messages to SNS topics.

#STUDENT TODO: Set ARN for SNS topic for email messages.
TOPIC_ARN_EMAIL = "arn:aws:sns:us-west-2:973435289726:EmailSNSTopic"
#STUDENT TODO: Set ARN for SNS topic for order messages.
TOPIC_ARN_ORDER = "arn:aws:sns:us-west-2:973435289726:OrderSNSTopic"

EMAIL_SUBJECT = "Status of pharmaceuticals order."
EMAIL_MESSAGE = "Your pharmaceutical supplies will be shipped 5 business days from the date of order."
ORDER_DETAILS = "Ibuprofen, Acetaminophen"

def Connect2sns():
    #Connects to the SNS service
    return utils.connect2Service('sns')

def publishEmailMessage(topicArn=TOPIC_ARN_EMAIL, emailMesg=EMAIL_MESSAGE, emailSubj=EMAIL_SUBJECT):
    sns = Connect2sns()
    #STUDENT TODO: Retrieve the topic instance on the sns resource object using the TOPIC_ARN_EMAIL
    topic = sns.Topic(topicArn)
    #STUDENT TODO: Publish a message to the SNS topic for email messages. Use the EMAIL_MESSAGE and EMAIL_SUBJECT constants as email content.
    topic.publish(Message=emailMesg, Subject=emailSubj)
    print("Email topic published")

def publishOrderMessages(topicArn=TOPIC_ARN_ORDER, orderDetails=ORDER_DETAILS):
    sns = Connect2sns()
    for i in range(1, utils.NUM_MESSAGES + 1):
        orderDict = {'orderId': i, 'orderDate': "2015/10/%d" % i,  'orderDetails': orderDetails}
        porder = order.Order(orderDict)
        print("Publishing order to SNS topic:", repr(porder))
        #STUDENT TODO: Invoke the dumps method from json module to convert the Order object to a JSON string.
        jsonStr = json.dumps(porder, default=order.jdefault, indent=4)

        #STUDENT TODO: Retrieve the topic instance on the sns resource object using the TOPIC_ARN_ORDER
        #STUDENT TODO: Publish the JSON-formatted order to the SNS topic for orders.
        topic = sns.Topic(topicArn)
        topic.publish(Message=jsonStr)

        print("Order topic published")

def publishMessages():
    publishEmailMessage()
    publishOrderMessages()

def main():
    try:
        publishMessages()
    except Exception as err:
        print("Error Message {0}".format(err))

if __name__ == '__main__':
    main()
