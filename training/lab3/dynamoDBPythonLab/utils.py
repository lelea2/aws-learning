# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import boto3, botocore
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError

# 'EU'|'eu-west-1'|'us-west-1'|'us-west-2'|'ap-southeast-1'|'ap-southeast-2'|'ap-northeast-1'|'sa-east-1'|'cn-north-1'|'eu-central-1'
LAB_S3_BUCKET_NAME = "us-west-2-aws-training"
LAB_S3_BUCKET_REGION = "us-west-2"

LAB_S3_INFECTIONS_DATA_FILE_KEY = "awsu-ilt/developing/v2.0/lab-3-dynamodb/static/SampleInputFiles/InfectionsData.csv"
LAB_S3_PATIENT_REPORT_PREFIX = "awsu-ilt/developing/v2.0/lab-3-dynamodb/static/SampleInputFiles/PatientReports/PatientRecord"
LAB_S3_FILE_KEY = "InfectionsData.csv"
LAB_S3_INFECTIONS_TABLE_NAME = "Infections"

def connect2Service(service, region=None):
    #Returns connection to AWS service client
    try:
        if region:
            return boto3.resource(service, region_name=region)
        return boto3.resource(service)
    except botocore.exceptions.BotoCoreError as e:
        if isinstance(e, botocore.exceptions.NoCredentialsError):
            print("No AWS Credentials file found or credentials were invalid")
    return None

def isTableActive(tableName=LAB_S3_INFECTIONS_TABLE_NAME):
    #Check if the given table exists and active
    try:
        resource = connect2Service('dynamodb')
        table = resource.Table(tableName)
        if table.table_status == 'ACTIVE':
            return True
    except ClientError as err:
        if (err.response.get('Error').get('Code') == 'ResourceNotFoundException'):
            print("{0} Table not found".format(tableName))
    except Exception as err:
        print("Error Message:: {0}".format(err))
    return False
