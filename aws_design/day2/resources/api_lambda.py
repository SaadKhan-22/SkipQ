import json
import os

def lambda_handler(event, context):
    if event["httpMethod"] == "POST":
        print(event)
        
        response = {
                "statusCode": 200,
                "body": json.dumps({"statusCode": 200, 
                                    "event[body]":event['body'],
                                    "status":"Value Inserted",
                                    "list":"Alarms have been generated"}),
                "isBase64Encoded": False
            }
        return response