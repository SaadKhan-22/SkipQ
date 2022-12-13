import boto3
import os
import json



def lambda_handler(event, context):
    #add alarm info to event parameter

    #parse event info to get relevant alarm info for placing in database
    ddb_name = os.environ.get('SaadKAlarmsTableName')

    client = boto3.client('dynamodb')

    for record in event['Records']:

        # Parse message's key value from string to json
        message = json.loads(record['Sns']['Message'])

        # Prepare an item to stor in the DDB Table 
        # AlarmName, Timestamp, NewStateReason, MetricName, URL parsed from Events
        item = {
            "AlarmName": {'S': message["AlarmName"]},
            "Timestamp": {'S': record['Sns']['Timestamp']},
            "NewStateReason": {'S': message["NewStateReason"]},
            "MetricName": {'S': message["Trigger"]["MetricName"]},
            "URL": {'S': message["Trigger"]["Dimensions"][0]["value"]},
        }        
        
        # Put item in DynamoDB Table
        response = client.put_item(
            TableName=ddb_name,
            Item=item
        )

    return response
    