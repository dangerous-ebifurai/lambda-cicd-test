import json

def lambda_handler(event, context):
    """Lambda のエントリーポイント"""
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda!",
            "input": event
        })
    }
    return response