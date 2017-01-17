import boto3
import sys

from botocore.exceptions import NoCredentialsError,ClientError

#Before running the code, update ~/.aws/credentials file with your credentials.

def getAllBuckets():
    try:
        s3 = boto3.resource('s3')
        buckets = []
    except NoCredentialsError:
        print("No AWS Credentials file found or credentials were invalid")
        sys.exit()

    try:
        no_of_buckets = len(list(s3.buckets.all()))
        print("===============================================================")
        print("Developing on AWS Lab 1 - Python SDK! Ready, Set, Go!")
        print("===============================================================")
        print("Number of buckets: " + str(no_of_buckets) + "\n\n")
        return no_of_buckets
    except ClientError as ex:
        print(ex)
        return 0

if __name__ == '__main__':
    getAllBuckets()
