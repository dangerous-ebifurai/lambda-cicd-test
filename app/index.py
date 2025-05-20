import json

def lambda_handler(event, context):

    print("Event: ", event["body"])
    print("Event: ", event["headers"])

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda!",
            "input": event
        })
    }
    return response