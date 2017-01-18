# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import time, csv
from botocore.exceptions import ClientError
import utils

BUCKET_NAME = utils.LAB_S3_BUCKET_NAME
BUCKET_REGION = utils.LAB_S3_BUCKET_REGION

INFECTIONS_DATA_FILE_KEY = utils.LAB_S3_INFECTIONS_DATA_FILE_KEY
FILE_NAME = utils.LAB_S3_FILE_KEY
INFECTIONS_TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME
DELIMITER=","    #Delimiter character to separate CSV values
HTTP_STATUS_SUCCESS = 200

def loadInfectionsData(
        tableName=INFECTIONS_TABLE_NAME, bucketRegion=BUCKET_REGION,
        bucket=BUCKET_NAME, fKey=INFECTIONS_DATA_FILE_KEY, FName=FILE_NAME):
    #Use the Python csv module to read the contents and add items to the given Infections table
    numFailures = 0
    try:
        S3 = utils.connect2Service('s3', bucketRegion)
        dynamodb = utils.connect2Service('dynamodb')
        myTable = dynamodb.Table(tableName)
        try:
            S3.meta.client.head_bucket(Bucket=bucket)
            myBucket = S3.Bucket(bucket)
        except ClientError as err:
            print("Bucket Not Available")
            print("Error Message: {0}".format(err))
            numFailures = 9999
            return numFailures
        except Exception as err:
            print("Error Message: {0}".format(err))
            numFailures = 9999
            return numFailures
        #Connect to S3 and get the sample CSV file from the given bucket
        try:
            myBucket.download_file(fKey, FName)
        except Exception as err:
            print("Error Message: {0}".format(err))
            print("Failed downloading from S3 bucket.")
            numFailures = 9999
            return numFailures
        print("Loads infection data from the sample CSV file.")
        with open(FName, newline='') as fh:
            reader = csv.DictReader(fh, delimiter=DELIMITER)
            #STUDENT TODO: Add items PatientId, City, Date read from the CSV file to the tableName and region given as input
            print("Uploading items ...")
            for row in reader:
                try:
                    resp = myTable.put_item(
                        Item= {
                            'PatientId': row['PatientId'],
                            'City': row['City'],
                            'Date': row['Date']
                        })
                except Exception as err:
                    print("Error Message: {0}".format(err))
                    numFailures += 1
            print("Uploaded items")
    except FileNotFoundError as err:
        print("Failed to add item in {0}".format(tableName))
        print("Error Message: {0}".format(err))
        numFailures = 9999
    except OSError as err:
        print("Failed to add item in {0}".format(tableName))
        print("Error Message: {0}".format(err))
        numFailures = 9999
    except Exception as err:
        print("Failed to add item in {0}".format(tableName))
        print("Error Message: {0}".format(err))
        numFailures = 9999
    return numFailures


if __name__ == '__main__':
    print('===============================================================')
    print('Lab 3 DynamoDB - Add infections data from the CSV file to Infections table')
    print('===============================================================')
    loadInfectionsData()
