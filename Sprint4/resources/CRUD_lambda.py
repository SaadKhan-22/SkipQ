import json
import boto3
import os

def lambda_handler(event, context):  
        
    DBName = os.environ.get("CRUD")
    client = boto3.client('dynamodb')
    # urlspath = "/urls"
    # createMethod = "POST"
    # readMethod = "GET"
    # updatMethod = "PATCH"
    # deleteMethod = "DELETE"
    # http_method = event["httpMethod"]
    # http_path = event["path"]
    
    if event["httpMethod"] == "POST":
        requestBody = json.loads(event['body'])

        #Defining the URL_ID and name
        url_id = requestBody["URL_ID"]
        url = requestBody["URL"]

        print(url + url_id)

        Item={
            "URL_ID": {'S': url_id},
            "URL": {'S': url}
        }

        client.put_item(
            TableName = DBName,
            Item=Item
        )

        response = {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, 
                                "event[body]":event['body'],
                                "status":"put + url Inserted",
                                "list":"Values have been inserted"}),
            "isBase64Encoded": False
        }
        return response
    
    
    elif event["httpMethod"] == "GET":
        
        response = {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, 
                                "event[body]":event['queryStringParameters']}),
            "isBase64Encoded": False
        }
        return response