# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import time, csv
import utils

BUCKET_REGION        = utils.LAB_8_BUCKET_REGION
BUCKET_NAME         = utils.LAB_8_BUCKET_NAME
PHARMA_DATA_FILE_KEY= utils.LAB_8_PHARMA_DATA_FILE_KEY
FILE_NAME             = utils.LAB_8_FILE_KEY
TABLE_NAME            = utils.LAB_8_PHARMA_TABLE_NAME
DELIMITER            = ","    #separate csv values by comma.

#Welcome to the AWS Python SDK! Let's build a Pharmaceutical drug listing!
#Connection.

def getPharmaInfo(drugName, tableName=TABLE_NAME):
    #Query the PharmaInfo table on the given region for a specific drug name.
    try:
        dynamodb = utils.connect2Service('dynamodb')
        myTable = dynamodb.Table(tableName)
        rec = myTable.get_item(Key={'drugName': drugName})
        #Retrieves from the records object returned by the query.
        if rec.get('Item'):
            return rec['Item'].get('usage')
    except Exception as err:
        print("Error message: {0}".format(err))

def loadData(tableName=TABLE_NAME, bucket=BUCKET_NAME, region=BUCKET_REGION, fKey=PHARMA_DATA_FILE_KEY, fName=FILE_NAME):
    #Add items (DrugName, usage) to the given PharmaInfo table available in the given region
    try:
        #Check if the File Key is present in the bucket
        S3 = utils.connect2Service('s3', region)
        dynamodb = utils.connect2Service('dynamodb')
        myTable = dynamodb.Table(tableName)
        try:
            S3.meta.client.head_bucket(Bucket=bucket)
            myBucket = S3.Bucket(bucket)
        except ClientError as err:
            print("Bucket Not Available")
            print("Error message: {0}".format(err))
            return False
        except Exception as err:
            print("Error message: {0}".format(err))
            return False
        #Connects to S3 and get the CSV file from the given bucket
        try:
            myBucket.download_file(fKey, fName)
        except Exception as err:
            print("Error message: {0}".format(err))
            print("Downloading failed from S3 bucket")
            return False
        print("Loading pharmaceutical data from csv file to DynamoDB")
        with open(fName, newline='') as fh:
            reader = csv.DictReader(fh, delimiter=DELIMITER)
            print("Begin loading items ...")
            for row in reader:
                try:
                    resp = myTable.put_item(
                            Item={
                                'drugName': row['DrugName'],
                                'usage': row['Usage']})
                except Exception as err:
                    print("Error message: {0}".format(err))
                    numFailures += 1
            print("End loading items")
    except Exception as err:
        print("Failed creating item {0}".format(tableName))
        print("Error message: {0}".format(err))
        return False
    return True

def pharmaDataExists(tableName=TABLE_NAME):
    #Check if the given tableName exists and active.
    try:
        pharmaDataExists = False
        pharmaDataExists = utils.isTableActive(tableName)
    except Exception as err:
        print("Error message:: {0}".format(err))
    return pharmaDataExists

def createPharmaTable(tableName=TABLE_NAME):
    #Create PharmaceuticalUsage table with the given name in the given region with the following fields.
    rval =False
    dynamodb = utils.connect2Service('dynamodb')
    try:
        print("Creating Table")
        table = dynamodb.create_table(TableName=tableName,
                    KeySchema=[{'AttributeName':'drugName', 'KeyType':'HASH'}],
                    AttributeDefinitions=[{'AttributeName':'drugName', 'AttributeType':'S'}],
                    ProvisionedThroughput={'ReadCapacityUnits':5, 'WriteCapacityUnits':5}
                )
        #Table creation takes a little time. Please wait.
        time.sleep(5)
        #Checks if the given PharmaInfo table exists
        if pharmaDataExists(tableName):
            rval = True
    except Exception as err:
        print("{0} Table creation failed.".format(tableName))
        print("Error message: {0}".format(err))
    return rval

def setup():
    #Setting up DynamoDB:
    print("Begin DynamoDB Setup, Creating table")
    #Checks if the given PharmaInfo table exists
    rval = True
    if (not pharmaDataExists()):
        rval = createPharmaTable()
    print("Table created")
    if not rval:
        print("Loading failed since Table creation failed.")
        return False
    rval = loadData()
    if not rval:
        return False
    print("DynamoDB setup completed")
    return True

if __name__ == '__main__':
    setup()
