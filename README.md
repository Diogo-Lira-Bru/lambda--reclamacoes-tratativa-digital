🌐 lambda--reclamacoes-tratativa-digital
Função Lambda responsável por receber reclamações enviadas por canais digitais (como aplicativos e sites), validar os dados, padronizar a estrutura e encaminhar para o sistema central de processamento via Amazon SQS.

📌 Propósito
Automatizar a ingestão de reclamações digitais, garantindo:

  Validação dos dados recebidos via API Gateway
  Padronização da estrutura de reclamação
  Encaminhamento assíncrono para o pipeline central
  Rastreabilidade e controle de origem

🔄 Fluxo de Execução
  Recepção do payload JSON via API Gateway

Validação dos campos obrigatórios:
  customer_id
  reclamacao_texto
  Criação de objeto padronizado
  Envio para fila SQS central
  Retorno HTTP com status e ID da reclamação

🧠 Lógica de Padronização
A função cria um objeto com os seguintes campos:


json
    {
      "Id": "e3f1c2a0-9d4b-4f3f-9a2e-123456789abc",
      "CustomerIdentifier": "12345678900",
      "ReclamationText": "Texto da reclamação enviada pelo cliente.",
      "ReceivedDate": "2025-11-04T23:55:12.000Z",
      "SourceChannel": "Digital",
      "CustomerHistory": null,
      "ClassifiedCategories": []
    }


🛡️ Tratamento de Erros
  JSON malformado: Retorno HTTP 400 com mensagem de erro
  Campos obrigatórios ausentes: Retorno HTTP 400 com mensagem de validação
  Falha no envio ao SQS: Retorno HTTP 500 com log crítico

📬 Integração com SQS
  A reclamação padronizada é enviada para a fila central com o atributo:
    Atributo	Valor
    Origem	Digital

🧰 Tecnologias Utilizadas
  Componente	Tecnologia
  Função Serverless	AWS Lambda
  Entrada	Amazon API Gateway
  Fila de mensagens	Amazon SQS
  Identificação	UUID
  Data e Hora	datetime (Python)
  
🧪 Testes Recomendados
  Payloads válidos com todos os campos
  Payloads incompletos ou malformados
  Simulações de falha no envio ao SQS
  Verificação do conteúdo e formato do JSON gerado

🔐 Segurança e Rastreabilidade
  Identificador único por reclamação
  Log completo de eventos e falhas
  Canal de origem explicitamente marcado como Digital
