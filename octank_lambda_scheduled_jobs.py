import json
import boto3
import requests
import datetime

def lambda_handler(event, context):

# 1. get the current time.minute
nowTime = datetime.datetime.now()
print(nowTime.minute)

# 2. scan and return Items from dynamodb based on nowTime.minute and runJob
from boto3.dynamodb.conditions import Key #why is this needed? https://highlandsolutions.com/blog/hands-on-examples-for-working-with-dynamodb-boto3-and-python

def scanJobs():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('customer')
    
    resp = table.scan(FilterExpression=Attr("runJob").eq(
    	if nowTime.minute >= 0 and nowTime.minute < 30:
    		runJob = 1
		else:
			runJob = 2))
    
    # should this also include: (ProjectionExpression="customerId, presharedKey, s3key")
    
    print(resp['Items']) #is this the right way to return values to use in the next step?

# 3. download custom_code.py to /tmp/ directory in lambda

s3 = boto3.resource("s3")
srcFileName="custom_code.py"
destFileName="s3_custom_code.py"
bucketName="octank-custom-code"
k = Key(bucket,srcFileName)
k.get_contents_to_filename(destFileName)

# 4. read file line-by-line and only continue with loop once 200 success response is returned

file1 = open('s3_custom_code.py', 'r')  
Lines = file1.readlines()
for line in Lines:
	response = request.get(endpoint)  #how do i pass the customerId + api Key with the request?
	if response.status_code = 200:
		data = response.json()
		return data
	else:
		print(response.status_code)
		print(response.text)        # would this stop the loop? i don't think so

#5. loop through next customer

