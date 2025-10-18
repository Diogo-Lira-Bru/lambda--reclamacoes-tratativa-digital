import json
import os
import uuid
from datetime import datetime
import boto3

sqs_client = boto3.client('sqs')

SQS_QUEUE_URL = os.environ.get('SQS_CENTRAL_URL')

def lambda_handler(event, context):
    """
    Função Handler do AWS Lambda.
    Recebe o evento do API Gateway (que contém o JSON da requisição).
    """
    
    # ----------------------------------------------------
    # 1. RECEPÇÃO E EXTRAÇÃO DO PAYLOAD DO API GATEWAY
    # ----------------------------------------------------
    
    try:
        raw_payload = json.loads(event['body'])
    except Exception as e:
        context.log(f"ERRO 400: Falha ao desserializar o JSON do API Gateway. Erro: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'JSON de entrada inválido.'})
        }

    # ----------------------------------------------------
    # 2. VALIDAÇÃO E PADRONIZAÇÃO BÁSICA
    # ----------------------------------------------------

    customer_id = raw_payload.get('customer_id')
    reclamation_text = raw_payload.get('reclamacao_texto')

    if not customer_id or not reclamation_text:
        context.log("ERRO 400: Dados de entrada incompletos (ID ou Texto faltando).")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Dados do cliente ou texto da reclamação estão faltando.'})
        }

    standardized_reclamation = {
        'Id': str(uuid.uuid4()),
        'CustomerIdentifier': customer_id,
        'ReclamationText': reclamation_text,
        'ReceivedDate': datetime.utcnow().isoformat() + 'Z',
        'SourceChannel': 'Digital',
        'CustomerHistory': None,
        'ClassifiedCategories': []
    }
    
    # ----------------------------------------------------
    # 3. ENVIO PARA O SQS CENTRAL
    # ----------------------------------------------------
    
    message_body = json.dumps(standardized_reclamation)
    
    try:
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=message_body,
            MessageAttributes={
                'Origem': {
                    'DataType': 'String',
                    'StringValue': 'Digital'
                }
            }
        )
        
        context.log(f"Reclamação {standardized_reclamation['Id']} enviada para o SQS Central. Status: 200")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'id': standardized_reclamation['Id'], 'status': 'Recebido para processamento assíncrono'})
        }

    except Exception as e:
        context.log(f"ERRO CRÍTICO: Falha ao enviar a mensagem para o SQS. Erro: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Falha interna ao processar a requisição.'})
        }