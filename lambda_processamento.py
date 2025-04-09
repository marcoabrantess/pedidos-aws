import json
import boto3
import os
from botocore.exceptions import ClientError

# Inicializa recursos AWS
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Obtém as variáveis de ambiente
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'Orders')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    for record in event['Records']:
        try:
            message_body = json.loads(record['body'])
            order_id = message_body['orderId']
        except Exception as e:
            print("Erro ao processar mensagem:", e)
            continue
        
        try:
            # Atualiza o status do pedido para PROCESSING
            table.update_item(
                Key={'orderId': order_id},
                UpdateExpression="set #s = :s",
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':s': 'PROCESSING'}
            )
            
            # Aqui você pode incluir sua lógica de processamento adicional...
            
            # Atualiza o status para COMPLETED
            table.update_item(
                Key={'orderId': order_id},
                UpdateExpression="set #s = :s",
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':s': 'COMPLETED'}
            )
            
            # Publica uma mensagem no SNS para notificar o cliente
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=json.dumps({'orderId': order_id, 'status': 'COMPLETED'}),
                Subject='Pedido Processado'
            )
        except ClientError as e:
            print("Erro ao processar pedido:", e)
            continue

    return {'status': 'Done'}
