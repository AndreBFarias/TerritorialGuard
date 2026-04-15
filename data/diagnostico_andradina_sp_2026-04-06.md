# Diagnostico Final: Andradina - SP (v3 - com upstream)
# Data: 2026-04-06
# Projeto: {GCP_PROJECT}
# id_municipio IBGE: 3502101
# Queries: 57 | Bytes: 217 MB

## Resumo Executivo

| Classificacao | Quantidade | Descricao |
|---|---|---|
| OK | 19 | Dados presentes e validados |
| ZERO_LEGITIMO | 6 | Zero confirmado na fonte (programa nao existe no municipio) |
| ZERO_SUSPEITO | 11 | Upstream revelou problemas em 4 destes |

### Descobertas Criticas (dados perdidos no pipeline)

| Metrica | Fonte Upstream | Registros Fonte | Registros Painel | Diagnostico |
|---|---|---|---|---|
| PDMLIC Elegiveis | pdmlic_inscricao_sisu | 2 | 0 | PERDEU_NO_PAINEL |
| SISTEC Matriculas | sistec_ciclo_matricula | 6.593 | 0 | PERDEU_NO_PAINEL |
| SISU Vagas | sisu_vaga_ofertada | 567 | 0 | VALOR_ZERADO |
| SESU Obras NovoPAC | simec_obra_monitoramento | 28 | 0 | PERDEU_NO_PAINEL |

### Zeros Confirmados na Fonte (nada a fazer)

| Metrica | Fonte | Registros | Motivo |
|---|---|---|---|
| Pronatec Vagas | gaia_pronatec_vaga | 0 | Nao tem dados Pronatec |
| Mulheres Mil | gaia_mulheres_mil_vaga | 0 | Nao tem dados Mulheres Mil |
| FIES Valor | fnde_fies | 0 | Nao tem contratos FIES |
| Pacto Obras | novopac_fnde_pacto | 0 | Nao tem obras do Pacto |
| Escolas Quilombolas | censo_escolar | 926 (geral) | Escola existe mas nenhuma e quilombola |
| CNCA Formacoes | gaia_cnca | 10 | CNCA existe mas formacoes nao pagas |

---

## Investigacoes Necessarias

### 1. SISTEC (6.593 registros perdidos) — PRIORIDADE ALTA
- Fonte: sistec_ciclo_matricula tem 6.593 matriculas para id_municipio 3502101
- Painel: painel_ept_sistec tem 0 registros para Andradina
- Hipotese: o JOIN no painel_ept_sistec.sql usa `nome_municipio` que pode ter formato
  diferente da fonte (ex: "ANDRADINA" vs "Andradina"). Verificar CTE `qualificacao_profissional_publica`.
- Acao: abrir o modelo painel_ept_sistec.sql e verificar como o id_municipio e mapeado

### 2. PDMLIC (2 inscricoes perdidas) — PRIORIDADE MEDIA
- Fonte: pdmlic_inscricao_sisu tem 2 inscricoes com municipio = Andradina
- Painel: 0 registros com filtro ano=2025
- Hipotese: inscricoes podem ser de edital 2026, nao 2025. Filtro de ano exclui.
- Acao: verificar qual ano/edital as inscricoes tem na fonte

### 3. SISU (567 vagas, valor=0) — PRIORIDADE MEDIA
- Fonte: sisu_vaga_ofertada tem 567 registros com municipio_campus LIKE 'andradina'
- Painel: 5 registros com qtd_vagas_ofertadas = 0
- Hipotese: as 567 vagas sao de campus em Andradina (municipio_campus), mas o painel
  filtra por municipio do candidato, nao do campus. Ou o filtro de ano excluiu.
- Acao: verificar diferenca entre municipio e municipio_campus no painel_sisu.sql

### 4. SESU NovoPAC (28 obras) — PRIORIDADE BAIXA
- Fonte: simec_obra_monitoramento tem 28 registros com municipio LIKE 'andradina'
- Painel: 0 registros
- Hipotese: campo 'municipio' na fonte pode conter "Andradina" de outro estado,
  ou o JOIN com filtro_territorio nao casa.
- Acao: verificar quais municipios aparecem nos 28 registros

---

## Metricas que Batem 100%

| Metrica | Script | Dashboard |
|---|---|---|
| Escolas | 38 | 38 |
| Matriculas | 8.897 | 8.897 |
| CNCA Total | 74.390 | R$ 74,39 mil |
| CNCA Repasse Bolsistas | 32.400 | 32,40 mil |
| CNCA Articuladores | 1 | 1 |
| PND Municipios | 1 | 1 |
| ETI Repasse | 328.864 | presente |
| FUNDEB (Realizado) | 40.304.538 | R$ 40,30 mi |
| Salario Educacao | 2.661.787 | R$ 2,66 mi |
| NovoPAC Total | 1 | 1,00 |
| NovoPAC Valor | 9.873.820 | R$ 9,87 mi |
| Selecoes Total | 1 | ETI: 1 |
| Selecoes Valor | 9.873.820 | R$ 9,87 mi |
