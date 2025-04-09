# Order Processing with AWS Serverless

This project implements a serverless solution for managing and processing orders using AWS services, providing automatic scalability, simplified maintenance, and seamless integration between components.

## Overview

The project exposes a REST API via AWS API Gateway, allowing clients to submit orders. Once received, the order is validated, stored in DynamoDB, and sent to an SQS queue for asynchronous processing. After processing, the client is notified via SNS.

## Process Flow

1. **Submit Order**: The client sends a POST request to the REST API.
2. **Validation (Lambda)**: Checks for required fields (`customerId` and `items`) and stores the order with `RECEIVED` status in DynamoDB.
3. **SQS Queue**: Receives the order ID for later processing.
4. **Processing (Lambda)**: Updates the order status to `PROCESSING`, performs necessary operations, and finally sets the status to `COMPLETED`.
5. **Notification (SNS)**: Sends a completion message to the client indicating the order has been processed.

## Technologies Used

- **AWS CloudFormation**: Infrastructure as code.
- **AWS API Gateway**: Manages and exposes the public REST API.
- **AWS Lambda (Python)**: Serverless code execution for validation and processing.
- **AWS DynamoDB**: Scalable NoSQL storage for orders.
- **AWS SQS (Simple Queue Service)**: Asynchronous and decoupled processing queue.
- **AWS SNS (Simple Notification Service)**: Sends notifications after processing.

## Project Structure

```
.
├── lambda_validacao.py     # Lambda code for order validation and insertion
├── lambda_processamento.py # Lambda code for order processing
└── template.yaml           # CloudFormation template to create the infrastructure
```

## Deploying the Infrastructure

The infrastructure can be easily deployed using the provided CloudFormation template (`template.yaml`). Configure the required parameters such as S3 bucket names and keys for the ZIP packages containing Lambda function code.

## Future Improvements

- Implement a Dead-Letter Queue (DLQ) for messages that fail to be processed.
- Advanced monitoring with CloudWatch Alarms and Dashboards.
- Improved exception handling and detailed logs for easier debugging.

---

Built with :heart: using AWS Serverless technologies.

---

# Processamento de Pedidos com AWS Serverless

Este projeto implementa uma solução serverless para gerenciamento e processamento de pedidos utilizando serviços AWS, proporcionando escalabilidade automática, manutenção simplificada e integração fluida entre componentes.

## Visão Geral do Funcionamento

O projeto expõe uma API REST via AWS API Gateway, permitindo a recepção de pedidos. Uma vez recebido, o pedido é validado, armazenado no DynamoDB e inserido em uma fila SQS para processamento assíncrono. Após o processamento, o cliente é notificado através do serviço SNS.

## Fluxo do Processo

1. **Envio do Pedido**: O cliente realiza um POST na API REST.
2. **Validação (Lambda)**: Verifica os campos obrigatórios (`customerId` e `items`) e armazena o pedido com status `RECEIVED` no DynamoDB.
3. **Fila SQS**: Recebe o identificador do pedido para processamento posterior.
4. **Processamento (Lambda)**: Atualiza o status do pedido para `PROCESSING`, realiza operações necessárias e, finalmente, define o status como `COMPLETED`.
5. **Notificação (SNS)**: Envia uma mensagem de conclusão para o cliente informando que o pedido foi processado.

## Tecnologias Utilizadas

- **AWS CloudFormation**: Infraestrutura como código.
- **AWS API Gateway**: Gestão e exposição da API REST pública.
- **AWS Lambda (Python)**: Execução de código serverless para validação e processamento.
- **AWS DynamoDB**: Armazenamento NoSQL eficiente e escalável para pedidos.
- **AWS SQS (Simple Queue Service)**: Fila para processamento assíncrono e desacoplado.
- **AWS SNS (Simple Notification Service)**: Envio de notificações após processamento.

## Estrutura do Projeto

```
.
├── lambda_validacao.py     # Código Lambda para validação e inserção do pedido
├── lambda_processamento.py # Código Lambda para processamento dos pedidos
└── template.yaml           # Template CloudFormation para criação da infraestrutura
```

## Deploy da Infraestrutura

A infraestrutura pode ser facilmente provisionada utilizando o template CloudFormation fornecido (`template.yaml`). Configure os parâmetros necessários como nomes do bucket S3 e chaves para os pacotes ZIP contendo o código das funções Lambda.

## Melhorias Futuras

- Implementar uma fila secundária (DLQ) para tratamento de mensagens que não puderam ser processadas.
- Monitoramento avançado com CloudWatch Alarms e Dashboards para análise de performance.
- Melhorias no tratamento de exceções e logs detalhados para facilitar debugging.

---

Desenvolvido com :heart: utilizando tecnologias AWS Serverless.

