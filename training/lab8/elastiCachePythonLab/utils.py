# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import botocore, boto3
from botocore.exceptions import ClientError

LAB_8_PHARMA_TABLE_NAME = "PharmaceuticalUsage"
LAB_8_BUCKET_REGION     = "us-west-2"
LAB_8_BUCKET_NAME       = "us-west-2-aws-training"
LAB_8_PHARMA_DATA_FILE_KEY      = "awsu-ilt/developing/v2.0/lab-8-elasticache/static/SampleInputFiles/PharmaListings.csv"
LAB_8_FILE_KEY = "PharmaListings.csv"
#STUDENT TODO: Set the endpoint for the Elasticache node cluster
LAB_8_CLUSTER_CONFIG_ENDPOINT = "qls-el-47u74s0qqd7w.e32klj.cfg.usw2.cache.amazonaws.com:11211"


def connect2Service(service, region=None):
    #Returns connection to AWS service s3.
    try:
        if region:
            return boto3.resource(service, region_name=region)
        return boto3.resource(service)
    except botocore.exceptions.BotoCoreError as e:                                         
        if isinstance(e, botocore.exceptions.NoCredentialsError):
            print("Invalid Creadentials")
    return None

def isTableActive(tableName=LAB_8_PHARMA_TABLE_NAME):
    #Is table active
    try:
        resource = connect2Service('dynamodb')
        table = resource.Table(tableName)
        if table.table_status == 'ACTIVE':
            return True
    except ClientError as err:
        if (err.response.get('Error').get('Code') == 'ResourceNotFoundException'):
            print("{0} Table is not found here".format(tableName))
    except Exception as err:
        print("Error message:: {0}".format(err))
    return False
