import json

# import requests
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    try:
        # Example of making an HTTP request (uncomment if needed)
        # ip = requests.get("http://checkip.amazonaws.com/").text

        # You can include additional logic or external calls here

        
        # Get visitor count from DynamoDB table table name is VisitorCount
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('VisitorCount')
        response = table.get_item(
            Key={
                'id': 'visitors'
            }
        )
        visitor_count = float(response['Item']['visitor_count'])
        print("GetItem succeeded:")
        
        
        # Your response headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }

        # Your response body
        body = {
            # "message": "hello world",
            # "location": ip  # Uncomment if you have the 'ip' variable
            "visitor_count": visitor_count,
        }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(body)
        }

    except Exception as e:
        # Handle exceptions and return an error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
