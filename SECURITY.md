# Política de Segurança -- TerritorialGuard

## Versões Suportadas

| Versão | Suportada |
| ------ | --------- |
| 2.0.x  | sim       |
| 1.x    | não       |

## Credenciais

Este projeto consome dados do BigQuery via service account. O arquivo de credenciais (`keyfile.json`) NUNCA deve ser commitado. Está explicitamente ignorado no `.gitignore` (`credentials/`).

Se você acidentalmente commitar credenciais, gire-as imediatamente no console GCP.

## Reportando uma Vulnerabilidade

1. **Não** abra uma issue pública
2. Envie email ao mantenedor
3. Inclua: descrição, passos para reproduzir, impacto, sugestões

## Tempo de Resposta

- Recebimento: 48h
- Avaliação inicial: 7 dias
- Correção: 30 dias

## Escopo

- Código em `src/`
- Dependências diretas
- Scripts de instalação

## Fora do Escopo

- Vulnerabilidades em `google-cloud-bigquery` e outras upstream
- Engenharia social
- Disponibilidade do BigQuery
