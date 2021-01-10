# why is this needed? https://highlandsolutions.com/blog/hands-on-examples-for-working-with-dynamodb-boto3-and-python
from boto3.dynamodb.conditions import Key
import json
import boto3
import requests
import datetime


def lambda_handler(event, context):

    # 1. get the current time.minute
    nowTime = datetime.datetime.now()
    print("time is: " + nowTime.minute)

    # 2. scan and return Items from dynamodb based on nowTime.minute and runJob
    dbItems = scanJobs(nowTime) 

    for item in dbItems: # looping through functions defined below
        downloadS3File(item.s3key)
        processFile(item.s3key, item.customerId, item.presharedKey)


def scanJobs(nowTime):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('customer')

    runJob = 1 if nowTime.minute < 30 else 2

    resp = table.scan(FilterExpression=Attr("runJob").eq(str(runJob)))
# should this also include: (ProjectionExpression="customerId, presharedKey, s3key")

# return all Items from the scan to be used in other parts of the function
    print(resp['Items'])
    return resp['Items']

# 3. download custom_code.py to /tmp/ directory in lambda


def downloadS3File(s3Key):
    s3 = boto3.resource("s3")
    srcFileName = s3Key
    destFileName = "/tmp/" + s3Key
    bucketName = "octank-custom-code"
    k = Key(bucketName, srcFileName)
    k.get_contents_to_filename(destFileName)


# 4. read file line-by-line and only continue with loop once 200 success response is returned
def processFile(s3Key, customerId, apiKey):
    file1 = open('/tmp/' + s3Key, 'r')
    Lines = file1.readlines()
    for line in Lines:
        # how do i pass the customerId + api Key with the request?  -- look at the API gateway docs to find the header names and then add headers to the request like this https://stackoverflow.com/questions/8685790/adding-headers-to-requests-module
        response = request.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(response.status_code)
            # would this stop the loop? i don't think so - yes, fail the job and log the failure somewhere for simplicity in the poc
            print(response.text)

# 5. loop through next customer
# 6. 


# NON-CODE STUFF
# url = 'https://www.w3schools.com/python/demopage.php'
# myobj = {'somekey': 'somevalue'}

# x = requests.post(url, data=myobj)


# for item in resp['Items']:
#     	if item.runJob == checktime.rightnow() if less than 30 min, run all jobs that have 1, if gt > 29 run all jobs that have 2)
# 			then post


# 			make flask_api return something
# 			take each one of those runs and log it out to show there was success
# 			just needs an indicator that it succeeded

# Show proof that happening
# Put logging within the code to demonstrate what is happening

#    By adding load
#    Response just returned to the lambda function
#    everything works over http request and http Response
#    api result will be in response

#    change the last line


# # iterate through s3 bucket object

# s3= boto3.resource('s3')
# bucket= s3.Bucket('test-bucket')
# # Iterates through all the objects, doing the pagination for you. Each obj
# # is an ObjectSummary, so it doesn't contain the body. You'll need to call
# # get to get the whole body.
# for obj in bucket.objects.all():
#     key= obj.key
#     body= obj.get()['Body'].read()
