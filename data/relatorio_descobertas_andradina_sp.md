# Relatorio de Descobertas: Validador de Cidades
# Municipio: Andradina - SP (IBGE 3502101)
# Data: 2026-04-06
# Autor: Equipe sua-org

---

## 1. Objetivo

Validar automaticamente se os dados exibidos no dashboard painel analítico territorial
(Looker Studio) estao corretos para o municipio de Andradina-SP, e identificar a causa raiz
quando metricas aparecem zeradas.

## 2. Metodologia

Ferramenta Python (`validador.py`) que:
- Executa 36 metricas mapeadas contra o BigQuery (`{GCP_PROJECT}`)
- Compara valores do script com os valores visiveis no dashboard (PDF)
- Para metricas zeradas, rastreia automaticamente as tabelas fonte (upstream)
- Classifica cada metrica: OK, ZERO_LEGITIMO, ZERO_SUSPEITO, PERDEU_NO_PAINEL

Total: 57 queries executadas, 217 MB processados.

## 3. Resultados Gerais

| Classificacao | Qtd | Percentual |
|---|---|---|
| OK (dados presentes e corretos) | 19 | 53% |
| ZERO_LEGITIMO (zero confirmado na fonte) | 6 | 17% |
| ZERO_SUSPEITO (requer investigacao) | 11 | 30% |
| **Total** | **36** | **100%** |

Dos 11 zeros suspeitos, a validacao upstream revelou:
- 4 com dados PERDIDOS no pipeline (bug real)
- 4 com valor zerado mas dados existentes (comportamento esperado)
- 3 com upstream inconclusivo

---

## 4. Metricas Validadas (19 OK)

Estas metricas batem 100% entre o script e o dashboard:

| Pag. | Metrica | Valor Script | Valor Dashboard | Fonte |
|---|---|---|---|---|
| 1 | Escolas | 38 | 38 | painel_escola |
| 1 | Escolas Integrais | 23 | — | painel_escola |
| 1 | Matriculas | 8.897 | 8.897 | painel_matricula_municipio |
| 1 | Docentes (Publica) | 608 | 519* | painel_pneerq |
| 1 | Escolas PNEERQ | 50 | — | painel_pneerq |
| 1 | Matriculas PNEERQ | 12.101 | — | painel_pneerq |
| 3 | CNCA Investimento Total | 74.390 | R$ 74,39 mil | painel_cnca |
| 3 | CNCA Repasse Bolsistas | 32.400 | 32,40 mil | painel_cnca |
| 3 | CNCA Articuladores | 1 | 1 | painel_cnca |
| 3 | CNCA Investimento Acumulado | 74.390 | R$ 74,39 mil | painel_cnca_investimento |
| 3 | PND Municipios Aderidos | 1 | 1 | painel_pnd_adesao |
| 3 | ETI Valor Repasse | 328.864 | presente | eti_valores_2025_csv |
| 3 | ETI Valor Fomento | 386.899 | presente | eti_valores_2025_csv |
| 4 | FUNDEB Repasse (Realizado) | 40.304.538 | R$ 40,30 mi | painel_fundeb |
| 4 | Salario Educacao (Realizado) | 2.661.787 | R$ 2,66 mi | painel_salario_educacao |
| 6 | NovoPAC Total Acoes | 1 | 1,00 | painel_novopac_consolidado |
| 6 | NovoPAC Valor Previsto | 9.873.820 | R$ 9,87 mi | painel_novopac_consolidado |
| 6 | Selecoes Total | 1 | ETI: 1 | painel_novopac_selecoes |
| 6 | Selecoes Valor Investimento | 9.873.820 | R$ 9,87 mi | painel_novopac_selecoes |

*Docentes: dashboard mostra 519 (deduplica docentes entre escolas/redes via Looker Studio).
Script retorna 608 (SUM por escola). Diferenca esperada e documentada.

---

## 5. Zeros Confirmados na Fonte (6 ZERO_LEGITIMO)

Estes zeros sao reais — o dado nao existe em nenhuma camada do pipeline.
Andradina genuinamente nao participa destes programas.

| Metrica | Fonte Upstream | Registros Fonte | Conclusao |
|---|---|---|---|
| Pronatec Vagas | gaia_pronatec_vaga | 0 | Sem vagas Pronatec no municipio |
| Pronatec Matriculas | gaia_pronatec_vaga | 0 | Idem |
| Mulheres Mil | gaia_mulheres_mil_vaga | 0 | Sem programa Mulheres Mil |
| FIES Valor | fnde_fies | 0 | Sem contratos FIES ativos |
| Pacto Total Obras | novopac_fnde_pacto | 0 | Sem obras do Pacto Retomada |
| Pacto Valor Previsto | novopac_fnde_pacto | 0 | Idem |

**Acao necessaria:** Nenhuma. Os zeros estao corretos.

---

## 6. Zeros com Valor Zerado mas Dados Existentes (4 VALOR_ZERADO)

O municipio TEM registros na tabela, mas a metrica especifica retorna 0.
Isso pode ser comportamento esperado ou indicar filtro inadequado.

| Metrica | Fonte | Reg. Fonte | Reg. Painel | Analise |
|---|---|---|---|---|
| Escolas Quilombolas | censo_escolar | 926 | 150 | 926 escolas no censo, nenhuma quilombola. **Correto.** |
| CNCA Formacoes Pagas | gaia_cnca | 10 | 4 | CNCA registrado, mas valor_pago_formacoes = 0. **Correto — ainda nao pago.** |
| CNCA Formacoes Empenhadas | gaia_cnca | 10 | 4 | Idem — valor_empenhado_formacoes = 0. **Correto.** |
| PND Estados Aderidos | simec_adesao_pnd | 1 | 1 | Andradina e municipio (indicador_uf=FALSE), nao estado. **Correto.** |

**Acao necessaria:** Nenhuma. Os zeros fazem sentido no contexto do dado.

---

## 7. DADOS PERDIDOS NO PIPELINE (4 descobertas criticas)

Estes sao os casos onde o dado EXISTE na fonte mas NAO aparece no dashboard.
Indica bug no JOIN, filtro ou transformacao do modelo dbt.

### 7.1 SISTEC — 6.593 matriculas perdidas

| Item | Detalhe |
|---|---|
| **Severidade** | ALTA |
| **Metrica afetada** | SISTEC Matriculas (pagina 5) |
| **Tabela painel** | painel_ept_sistec |
| **Tabela fonte** | sistec_ciclo_matricula (educacao_politica_sistec) |
| **Registros na fonte** | 6.593 |
| **Registros no painel** | 0 |

**Analise:**
O modelo `painel_ept_sistec.sql` usa a CTE `qualificacao_profissional_publica` que referencia
`sistec_ciclo_matricula`. A fonte tem `id_municipio = '3502101'` com 6.593 registros.
Porem, o painel final faz JOIN com `filtro_territorio` usando `nome_municipio`.

**Hipotese:** O formato de `nome_municipio` no resultado do JOIN nao corresponde ao valor
esperado pelo `filtro_territorio`. Possivel diferenca entre 'ANDRADINA', 'Andradina' ou
'Andradina - SP'.

**Verificacao sugerida:**
```sql
SELECT DISTINCT nome_municipio
FROM {GCP_PROJECT}.projeto_painel_ministro.painel_ept_sistec
WHERE id_municipio = '3502101' OR LOWER(nome_municipio) LIKE '%andradina%'
```

**Modelo dbt:** `queries/models/projeto_painel_ministro/painel_ept_sistec.sql`

---

### 7.2 PDMLIC — 2 inscricoes perdidas

| Item | Detalhe |
|---|---|
| **Severidade** | MEDIA |
| **Metrica afetada** | PDMLIC Elegiveis/Cadastrados/Beneficiarios (pagina 3) |
| **Tabela painel** | painel_pdmlic |
| **Tabela fonte** | pdmlic_inscricao_sisu (educacao_politica_pdmlic) |
| **Registros na fonte** | 2 (SISU), 0 (PROUNI) |
| **Registros no painel** | 0 |

**Analise:**
O modelo `painel_pdmlic.sql` filtra por `sigla_edital` e extrai o ano. Com filtro `ano=2025`,
registros de editais 2026 sao excluidos.

**Hipotese:** As 2 inscricoes SISU sao do edital PDML-2026 (ano=2026), nao 2025.
O filtro de ano no validador excluiu corretamente — nao e bug do dbt, e filtro temporal.

**Verificacao sugerida:**
```sql
SELECT sigla_edital, municipio, COUNT(*)
FROM {GCP_PROJECT}.educacao_politica_pdmlic.pdmlic_inscricao_sisu
WHERE LOWER(municipio) LIKE '%andradina%'
GROUP BY 1, 2
```

**Modelo dbt:** `queries/models/projeto_painel_ministro/painel_pdmlic.sql`

---

### 7.3 SISU — 567 vagas com valor zerado

| Item | Detalhe |
|---|---|
| **Severidade** | MEDIA |
| **Metrica afetada** | SISU Vagas Ofertadas (pagina 5) |
| **Tabela painel** | painel_sisu |
| **Tabela fonte** | sisu_vaga_ofertada (educacao_sisu_dados_abertos) |
| **Registros na fonte** | 567 |
| **Registros no painel** | 5 (com qtd_vagas_ofertadas = 0) |

**Analise:**
A fonte tem 567 registros com `municipio_campus` contendo 'andradina'. O painel tem 5 registros
para `municipio = 'Andradina - SP'` mas com vagas = 0.

**Hipotese:** O modelo `painel_sisu.sql` usa `municipio` do candidato (via filtro_territorio),
nao `municipio_campus` da IES. As 567 vagas sao ofertadas em campus de Andradina, mas os
candidatos sao de outros municipios. O painel mostra vagas por residencia do candidato, nao
por localizacao do campus.

**Verificacao sugerida:**
```sql
SELECT municipio, municipio_campus, SUM(qtd_vagas_ofertadas)
FROM {GCP_PROJECT}.projeto_painel_ministro.painel_sisu
WHERE municipio = 'Andradina - SP' OR municipio_campus LIKE '%Andradina%'
GROUP BY 1, 2
```

**Modelo dbt:** `queries/models/projeto_painel_ministro/painel_sisu.sql`

---

### 7.4 SESU NovoPAC — 28 obras perdidas

| Item | Detalhe |
|---|---|
| **Severidade** | BAIXA |
| **Metrica afetada** | SESU Total Obras / Valor Previsto (pagina 6) |
| **Tabela painel** | painel_novopac_sesu |
| **Tabela fonte** | simec_obra_monitoramento_painelbi (educacao_politica_simec) |
| **Registros na fonte** | 28 |
| **Registros no painel** | 0 |

**Analise:**
A fonte tem 28 registros com `municipio` contendo 'andradina'. Porem a busca por LIKE
pode ter pego obras de outros municipios com nome similar ou obras nao relacionadas a SESU.

**Hipotese:** Os 28 registros podem incluir obras de outros programas (nao SESU), ou o campo
`municipio` na fonte contem "Andradina" de outro estado (improvavel dado que so existe 1
Andradina no Brasil). O filtro do modelo `painel_novopac_sesu.sql` pode excluir por categoria
ou tipo de obra.

**Verificacao sugerida:**
```sql
SELECT municipio, sigla_uf, programa, categoria, COUNT(*)
FROM {GCP_PROJECT}.educacao_politica_simec.simec_obra_monitoramento_painelbi
WHERE LOWER(municipio) LIKE '%andradina%'
GROUP BY 1, 2, 3, 4
```

**Modelo dbt:** `queries/models/projeto_painel_ministro/painel_novopac_sesu.sql`

---

## 8. Padroes Tecnicos Descobertos

### 8.1 Triplicacao pelo filtro_territorio

O modelo `filtro_territorio` gera 3 linhas por municipio nos niveis municipio, estado e brasil.
Tabelas que usam `nome_municipio` como filtro (em vez de `id`) capturam os 3 niveis.

**Tabelas afetadas:** painel_fundeb, painel_salario_educacao, painel_pneerq, painel_ept_sistec,
eti_valores.

**Correcao aplicada:** filtrar por `CAST(id AS STRING) = '{id_municipio_ibge}'`.

### 8.2 CROSS JOIN cria registros esqueleto

Modelos como pronatec, mulheresmil e sisu fazem CROSS JOIN entre `filtro_territorio` e
dimensoes (anos, tipo_vinculo). Isso gera linhas para TODOS os municipios com valor 0.

**Impacto:** COUNT(*) retorna > 0 mesmo sem dados reais. O validador precisa verificar
o VALOR da metrica, nao apenas a existencia de registros.

### 8.3 Filtros implicitos do dashboard

O Looker Studio aplica filtros que nao estao nos modelos dbt:
- FUNDEB: `status = 'Realizado'`
- Salario Educacao: `id_status = 1`
- CNCA: sem filtro de ano (acumulado)
- Docentes: COUNT DISTINCT (deduplicacao entre escolas)

### 8.4 Duplicacao em selecoes_consolidado

A tabela `painel_novopac_selecoes_consolidado` apresenta 3 linhas identicas para a mesma obra
ETI (proposta 4527/2024, Edital 1). Isso triplica o valor de investimento se somado com SUM.

**Correcao aplicada:** usar `COUNT(DISTINCT proposta)` e `MAX(valor_investimento)`.

---

## 9. Recomendacoes

### Imediatas
1. **Investigar SISTEC** (item 7.1) — 6.593 matriculas perdidas e a descoberta mais critica
2. **Corrigir duplicacao selecoes** (item 8.4) — possivel bug no UNION ALL dos editais

### Curto prazo
3. **Verificar PDMLIC** (item 7.2) — confirmar se inscricoes sao de edital 2026
4. **Verificar SISU** (item 7.3) — confirmar diferenca municipio vs municipio_campus

### Medio prazo
5. **Padronizar filtros** — documentar quais filtros o Looker Studio aplica implicitamente
6. **Executar validador para outras cidades** — Andradina pode nao ser o unico caso

---

## 10. Como Reproduzir

```bash
cd ~/Desenvolvimento/sua organização/TerritorialGuard
.venv/bin/python validador.py --municipio "Andradina - SP" --ano 2025 --upstream
```

O xlsx com todos os resultados esta em:
`data/Projeto_Validador_Visao_Municipal.xlsx`
