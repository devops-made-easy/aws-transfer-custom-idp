# this file is sample python boto3 script to create users
# will be handy when need to create users in bulk.

# sample csv should container username in column 2 and folderpath within s3 bucket in column 4 in order for this script to work.


from csv import reader
import string
from random import *
import sys
import boto3
import json

sftpgatewayid = "s-xxxxxxxxxx"
iamrolearn = "arn:aws:iam::<account_id>:role/<role_name>"
sftp_s3_bucket = "<bucketname>"

# open file in read mode
with open('myscript.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    next(csv_reader)
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        print(row[1] + "=>" + row[3])
        characters = string.ascii_letters + string.digits
        password = "".join(choice(characters) for x in range(randint(8, 16)))
        SecretString = {
                    "Password": password,
                    "Role": iamrolearn,
                    "HomeDirectoryDetails": "[{\"Entry\": \"/\", \"Target\": \"/sftp_s3_bucket/" + row[3] + "\"}]"
            }
        client = boto3.client('secretsmanager', region_name='us-east-2')
        response = client.create_secret(
            Name=sftpgatewayid + '/' + row[1].lower(),
            Description='<add some jira ticket or description that suite your needs',
            SecretString=json.dumps(SecretString)
        )
        print(response['Name'] + "=>" + password)



