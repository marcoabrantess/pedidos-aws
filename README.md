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
