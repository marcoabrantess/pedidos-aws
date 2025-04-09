import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError

# Inicializa recursos AWS
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

# Obtém as variáveis de ambiente
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'Orders')
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'JSON inválido no corpo da requisição'})
        }
    
    if 'customerId' not in body or 'items' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Campos obrigatórios ausentes: customerId e items'})
        }
    
    # Gera um ID único para o pedido
    order_id = str(uuid.uuid4())
    order = {
        'orderId': order_id,
        'customerId': body['customerId'],
        'items': body['items'],
        'status': 'RECEIVED'
    }
    
    table = dynamodb.Table(TABLE_NAME)
    try:
        table.put_item(Item=order)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao armazenar pedido no banco de dados', 'details': str(e)})
        }
    
    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({'orderId': order_id})
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao enviar mensagem para SQS', 'details': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Pedido recebido com sucesso', 'orderId': order_id})
    }
