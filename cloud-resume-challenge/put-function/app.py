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
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('VisitorCount')
        id_key = 'visitors'

        # Attempt to update the existing item
        try:
            response = table.update_item(
                Key={
                    'id': id_key
                },
                UpdateExpression='SET visitor_count = if_not_exists(visitor_count, :init) + :val',
                ExpressionAttributeValues={
                    ':init': 0,
                    ':val': 1
                },
                ReturnValues='UPDATED_NEW',
                ConditionExpression='attribute_exists(id)'
            )

            # Convert Decimal to float for JSON serialization
            visitor_count = float(response['Attributes']['visitor_count'])
            print("UpdateItem succeeded")

        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            # If the item does not exist, create it using PutItem
            table.put_item(
                Item={
                    'id': id_key,
                    'visitor_count': 1
                }
            )
            print("PutItem succeeded")
            visitor_count = 1

        # Your response headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }

        # Your response body
        body = {
            "visitor_count": visitor_count,
        }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(body)
        }

    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")

        # Return an error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }