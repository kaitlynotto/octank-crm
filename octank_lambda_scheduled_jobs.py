from boto3.dynamodb.conditions import Key, Attr
import boto3
import botocore
import datetime
import urllib3
import json
import logging

def lambda_handler(event, context):
    
    nowTime = datetime.datetime.now()
    print(f"time is: {nowTime.minute}")

    dbItems = scanJobs(nowTime.minute)
    
    for item in dbItems: # looping through functions defined below
        downloadS3File(item["s3Key"])
        #processFile(item["s3Key"], item["customerId"], item["presharedKey"])
                    
def scanJobs(currentTime):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('customer')

    runJob = "a" if currentTime < 30 else "b"

    resp = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("runJob").eq(runJob))

# return all Items from the scan to be used in other parts of the function
    print(resp['Items'])
    return resp['Items']

def downloadS3File(s3key):
    s3 = boto3.resource('s3')
    print("Downloading file '" + s3key + "'")
    try:
        s3.Bucket("octank-custom-code").download_file(s3key, "/tmp/" + s3key)
        print("download succeeded")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object " + s3key + " does not exist.")
        else:
            raise


# def downloadS3File(s3Key):
#     print("Downloading file '" + s3Key + "'")
#     try:
#         s3 = boto3.resource("s3")
#         srcFileName = s3Key
#         destFileName = "/tmp/" + s3Key
#         bucketName = "octank-custom-code"
#         k = boto3.s3.Key(bucketName, srcFileName)
#         k.get_contents_to_filename(destFileName)
#     except Exception as e:
#         print(e)
        
#http = urllib3.PoolManager()

#def processFile(s3Key, customer_id, apikey): 
#    file1 = open('/tmp/' + s3Key, 'r')
#    Lines = file1.readlines()
#    for line in Lines:
#        lineParts = line.split(" = ")
#        endpoint = lineParts[1][1:-1] #slicing to remove double quotes around endpoint
#        print("calling endpoint " + endpoint)
#        response = http.request('GET', endpoint, headers={'customerId':customer_id, 'apiKey':apikey}) 
#        if response.status == 200:
#            data = json.loads(response.data.decode('utf-8')) #response.json()
#            print(data)
#        else:
#            print(response.status)
#            logging.info("Job could not be completed")
#            break
    
