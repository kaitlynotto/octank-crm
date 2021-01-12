from boto3.dynamodb.conditions import Key, Attr
import boto3
import botocore
import datetime
import urllib3
import json

def lambda_handler(event, context):
    
    nowTime = datetime.datetime.now()
    print(f"time is: {nowTime.minute}")

    dbItems = scanJobs(nowTime.minute)
    
    for item in dbItems: # looping through functions defined below
        downloadS3File(item["s3Key"])
        processFile(item["s3Key"], item["customerId"], item["presharedKey"])
    
def scanJobs(currentTime):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('customer')

    runJob = "a" if currentTime < 30 else "b"

    resp = table.scan(FilterExpression=Attr("runJob").eq(runJob))

# return all Items from the scan to be used in other parts of the function
    print(resp['Items'])
    return resp['Items']

BUCKET_NAME = 'octank-custom-code' # replace with your bucket name
KEY = item["s3Key"] # replace with your object key

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, f"/tmp/{KEY}")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
        
'''def downloadS3File(s3Key):
    print("Downloading file '" + s3Key + "'")
    try:
        s3 = boto3.resource("s3")
        srcFileName = s3Key
        destFileName = "/tmp/" + s3Key
        bucketName = "octank-custom-code"
        k = Key(bucketName, srcFileName)
        k.get_contents_to_filename(destFileName)
    
    except Exception as e:
        print(e)'''
        
http = urllib3.PoolManager()

def processFile(url, customer_id, apikey): 
    file1 = open('/tmp/' + s3Key, 'r')
    Lines = file1.readlines()
    for item in itemIteration:
        response = http.request('GET', url, headers={'customerId':customer_id, 'apiKey':apikey}) 
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8')) #response.json()
            print(data)
            return data
        else:
            print(response.status)
            break
    
