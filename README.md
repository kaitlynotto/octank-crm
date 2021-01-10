# octank-crm

1. Get the current time.minute
2. Scan and return Items from dynamodb based on nowTime.minute and runJob
3. Download custom_code.py from s3 to /tmp/ directory in lambda
4. Read file in /tmp/ line-by-line to send API request to API Gateway
5. Iterate through file once 200 success response is returned, else stop
5. Complete steps 3-5 for next customer

