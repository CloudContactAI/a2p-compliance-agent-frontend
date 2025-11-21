"""
AWS Lambda handler for serverless deployment
"""

import json
import base64
from app import app

def lambda_handler(event, context):
    """AWS Lambda handler"""
    
    # Handle API Gateway event
    if 'httpMethod' in event:
        # Convert API Gateway event to WSGI environ
        environ = {
            'REQUEST_METHOD': event['httpMethod'],
            'PATH_INFO': event['path'],
            'QUERY_STRING': event.get('queryStringParameters', '') or '',
            'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
            'CONTENT_LENGTH': str(len(event.get('body', '') or '')),
            'HTTP_HOST': event.get('headers', {}).get('host', ''),
            'wsgi.input': event.get('body', '') or '',
        }
        
        # Add headers
        for key, value in event.get('headers', {}).items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
        
        # Handle the request
        with app.test_request_context(
            path=event['path'],
            method=event['httpMethod'],
            headers=event.get('headers', {}),
            data=event.get('body', ''),
            query_string=event.get('queryStringParameters', {})
        ):
            response = app.full_dispatch_request()
            
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True),
                'isBase64Encoded': False
            }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid request format'})
    }
