# Guia 04 — Padrões de Código e Revisão

Este guia consolida os padrões de qualidade aplicados nas revisões de pull requests.
Seguir estes padrões evita retrabalho e acelera a aprovação das PRs.

---

## SQL

### 1. CAST, nunca SAFE_CAST

```sql
-- Correto
CAST(campo AS INT64)

-- Errado (mascara erros de conversão, retorna NULL silenciosamente)
SAFE_CAST(campo AS INT64)
```

Se o campo tem dados inválidos, o erro deve ser explícito — não silenciado.

### 2. Sem CASTs desnecessários

Se o campo já vem com o tipo correto da origem, não fazer CAST redundante:

```sql
-- Errado (campo já é STRING)
CAST(nome AS STRING)

-- Correto
nome
```

### 3. UPPER/LOWER em comparações de string

Cargas futuras podem vir com formatação diferente. Normalizar sempre:

```sql
-- Correto
WHERE UPPER(status) = 'APROVADO'

-- Errado (falha se vier como 'Aprovado' ou 'aprovado')
WHERE status = 'APROVADO'
```

Quando possível, preferir o campo de ID (numérico) à comparação por texto.

### 4. CTEs reutilizáveis

Se uma tabela é referenciada com `{{ ref() }}` mais de uma vez, criar CTE no início:

```sql
-- Correto
tabela_aux AS (
  SELECT * FROM {{ ref('tabela') }}
),
cte_1 AS (
  SELECT ... FROM tabela_aux
),
cte_2 AS (
  SELECT ... FROM tabela_aux JOIN ...
)

-- Errado (ref duplicado)
cte_1 AS (
  SELECT ... FROM {{ ref('tabela') }}
),
cte_2 AS (
  SELECT ... FROM {{ ref('tabela') }} JOIN ...
)
```

### 5. Precisão numérica em somas

Para campos FLOAT64 (valores monetários), aplicar tratamento de precisão:

```sql
TRUNC(ROUND(SUM(COALESCE(valor, 0)), 2), 2) AS valor_total
```

Para campos INT64, o `SUM` simples é suficiente.

### 6. Comentários em Jinja

```sql
-- Errado (comentário SQL aparece na documentação gerada)
-- Este é um comentário

-- Correto (comentário Jinja, não aparece na documentação)
{# Este é um comentário #}
```

### 7. Referências e fontes

Nunca usar nomes de tabelas hardcoded:

```sql
-- Correto
{{ ref('modelo_dbt') }}
{{ source('schema_fonte', 'tabela') }}

-- Errado
`{GCP_PROJECT}.schema.tabela`
```

### 8. Colunas não utilizadas

Remover colunas que não são usadas em nenhum visual do dashboard.
Se houver dúvida, verificar com a equipe antes de remover.

### 9. Consolidação de CTEs duplicadas

Se duas CTEs têm corpo praticamente idêntico, consolidar em uma CTE base:

```sql
-- Correto
base AS (
  SELECT ... FROM tabela  -- tratamentos comuns
),
variante_a AS (
  SELECT ... FROM base WHERE tipo = 'A'
),
variante_b AS (
  SELECT ... FROM base WHERE tipo = 'B'
)
```

---

## schema.yml

### Formato de descrição do modelo (obrigatório)

```yaml
description: "Descrição breve do modelo. // Frequência de atualização: Mensal. // Partição: Estado e Município. // Nível da observação: id_pessoa. // Fonte: CAPES. // Gestora dos dados: CAPES. // Tratamento dos dados: sua-org."
```

**Os separadores `//` são críticos** — um script do catálogo de dados depende deles para parsing automático.

### Campos da descrição

| Campo | Descrição | Se não souber |
|-------|-----------|--------------|
| Frequência de atualização | Diária, Semanal, Mensal, Anual | "Não informado" |
| Partição | Campos de cluster (corresponde ao `cluster_by` do modelo) | — |
| Nível da observação | Campos que compõem a chave primária (filtrar por eles retorna linha única) | — |
| Fonte | Órgão ou sistema de origem dos dados | — |
| Gestora dos dados | Órgão responsável pela gestão | — |
| Tratamento dos dados | Quem fez o tratamento (geralmente sua-org) | — |

### Descrição de colunas

```yaml
columns:
  - name: id_pessoa
    description: "Identificador único da pessoa."
```

- **Não** usar `data_type` nas colunas
- Descrição clara e concisa
- Acentuação correta obrigatória

---

## Acentuação

Regra absoluta: **toda palavra em português que exige acento deve ter acento**.

Isso vale para:
- Mensagens de commit
- Descrições no schema.yml
- Strings dentro do SQL (`'Sem informação'`, `'Pública'`)
- Nomes de colunas quando em português
- Documentação

Exemplos obrigatórios:
- `migração` (nunca `migracao`)
- `correção` (nunca `correcao`)
- `descrição` (nunca `descricao`)
- `configuração` (nunca `configuracao`)
- `validação` (nunca `validacao`)
- `função` (nunca `funcao`)
- `Pé-de-Meia` (nunca `Pe-de-Meia`)

---

## Commits

| Regra | Detalhe |
|-------|---------|
| Idioma | PT-BR |
| Formato | `tipo: descrição imperativa` |
| Tipos | `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `chore` |
| Emojis | Proibidos |
| Acentuação | Obrigatória |

---

## Checklist de Revisão

Antes de abrir a PR, verificar:

- [ ] Sem SAFE_CAST
- [ ] Comparações de string com UPPER/LOWER
- [ ] Sem CASTs desnecessários
- [ ] CTEs sem duplicação de refs
- [ ] Somas com tratamento de precisão (se FLOAT)
- [ ] schema.yml com formato `//` separadores
- [ ] Descrições com Frequência, Partição, Nível, Fonte, Gestora, Tratamento
- [ ] Acentuação correta em todo o código
- [ ] Sem colunas não utilizadas
- [ ] Commit com mensagem PT-BR descritiva
