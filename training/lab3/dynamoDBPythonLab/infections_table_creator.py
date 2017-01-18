# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import time
import utils
from botocore.exceptions import EndpointConnectionError


INFECTIONS_TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME
CITY_DATE_INDEX_NAME = "InfectionsByCityDate"
HTTP_STATUS_SUCCESS = 200

def removeTable(tableName=INFECTIONS_TABLE_NAME):
    #Removes the tableName from the region given as input
    rval = True
    if utils.isTableActive(tableName):
        print("{0} Table exists and will be removed.".format(tableName))
        try:
            rval = False
            dynamoDB = utils.connect2Service('dynamodb')
            table = dynamoDB.Table(tableName)
            resp = table.delete()
            time.sleep(15)
            if resp['ResponseMetadata']['HTTPStatusCode'] == HTTP_STATUS_SUCCESS:
                rval = True
                print("{0} Table has been deleted.".format(tableName))
        except Exception as err:
            print("Error Message: {0}".format(err))
            rval = False
    return rval

def createInfectionsTable(tableName=INFECTIONS_TABLE_NAME):
    rval = False
    dynamoDB = utils.connect2Service('dynamodb')
    #removeTable method is provided to clean up the created DynamoDB tables every time you run the code.
    if removeTable(tableName):
        try:
            #STUDENT TODO: Create Infections table with the fields, 'PatientId', 'City', and 'Date'
            #Specify the GlobalAllIndex name in the query
            table = dynamoDB.create_table(TableName=tableName,
                        KeySchema=[{'AttributeName':'PatientId', 'KeyType':'HASH'}],  #patientId hashkey
                        AttributeDefinitions=[
                                {'AttributeName':'PatientId', 'AttributeType':'S'},
                                {'AttributeName':'City', 'AttributeType':'S'},
                                {'AttributeName':'Date', 'AttributeType':'S'}
                            ],
                        GlobalSecondaryIndexes=[
                                {'IndexName': CITY_DATE_INDEX_NAME,
                                 'KeySchema':[
                                         {'AttributeName': 'City', 'KeyType': 'HASH'},
                                         {'AttributeName': 'Date', 'KeyType': 'RANGE'}
                                     ],
                                'Projection':{'ProjectionType': 'ALL'},
                                'ProvisionedThroughput':{'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10} }
                            ],
                        ProvisionedThroughput={'ReadCapacityUnits':5, 'WriteCapacityUnits':10}
                )
            #Wait for the table creation and the status to become active.
            time.sleep(15)
            if utils.isTableActive(tableName):
                rval = True
        except Exception as err:
            print("{0} Table could not be created".format(tableName))
            print("Error Message: {0}".format(err))
    return rval

if __name__ == '__main__':
    print('===============================================================')
    print('Lab 3 DynamoDB - Infections Table creation')
    print('===============================================================')
    isTableCreated = createInfectionsTable()
    print(INFECTIONS_TABLE_NAME + " Table created")


# ===============================================================


# Lab 3 DynamoDB - Infections Table creation
# ===============================================================
# Infections Table not found
# Infections Table created
