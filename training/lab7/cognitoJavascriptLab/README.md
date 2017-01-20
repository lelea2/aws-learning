Developing on AWS: Lab 7 - Amazon Cognito

==================================================================================================================

Using this command reference.

==================================================================================================================


1. Locate the section you need. Each section in this file matches a section in the lab instructions.

2. Replace items in angle brackets - < > - with appropriate values. For example, in this command you would replace the value - <JobFlowID> - (including the angle brackets) with the parameter indicated in the lab instructions:

elastic-mapreduce --list <JobFlowID>. You can also use find and replace to change bracketed parameters in bulk.

3. Do NOT enable the Word Wrap feature in Windows Notepad or the text editor you use to view this file.


++++ Developing Your Application ++++

==================================================================================================================
2.2: Create the Cognito Identity Pool
==================================================================================================================

2.2.13 Copy the IAM policy

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:BatchGetItem",
                "dynamodb:Query",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:BatchWriteItem"
            ],
            "Resource": [
                "<CognitoLab Table ARN>"
            ],
            "Condition": {
                "ForAllValues:StringEquals": {
                    "dynamodb:LeadingKeys": [
                        "${cognito-identity.amazonaws.com:sub}"
                    ]
                }
            }
        }
    ]
}

==================================================================================================================
2.3: Using Cognito in Your Website
==================================================================================================================

2.3.4 Creating a local development webserver

cd <yourWorkdir>\cognitoJavascriptLab\src
python -m http.server

© 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.
