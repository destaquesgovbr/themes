# Relatório de Validação de Qualidade - Subfase 4.2

**Arquivo analisado:** `themes_tree_enriched_full.yaml`

**Total de problemas:** 1006

## 1. Análise de Tamanho e Complexidade

### Estatísticas por Nível

| Nível | Média (palavras) | Mediana | Mínimo | Máximo |
|-------|------------------|---------|--------|--------|
| L1 | 18.2 | 17.0 | 9 | 30 |
| L2 | 49.8 | 50.0 | 35 | 68 |
| L3 | 18.2 | 18.0 | 9 | 32 |

### Problemas Identificados


#### Severidade: ALTO (477 problemas)


**too_short** (477 nós):

- `01` - Economia e Finanças: Descrição muito curta: 25 palavras (mínimo: 30)
- `01.01.01` - Política Fiscal: Descrição muito curta: 22 palavras (mínimo: 30)
- `01.01.02` - Autonomia Econômica: Descrição muito curta: 22 palavras (mínimo: 30)
- `01.01.03` - Análise Econômica: Descrição muito curta: 18 palavras (mínimo: 30)
- `01.01.04` - Boletim Econômico: Descrição muito curta: 19 palavras (mínimo: 30)
- `01.02.01` - Fiscalização Econômica: Descrição muito curta: 22 palavras (mínimo: 30)
- `01.02.02` - Tributação e Impostos: Descrição muito curta: 21 palavras (mínimo: 30)
- `01.02.03` - Combate à Evasão Fiscal: Descrição muito curta: 24 palavras (mínimo: 30)
- `01.02.04` - Regulamentação Financeira: Descrição muito curta: 23 palavras (mínimo: 30)
- `01.03.01` - Atração de Investimentos: Descrição muito curta: 24 palavras (mínimo: 30)
- `01.03.02` - Investimentos no Exterior: Descrição muito curta: 22 palavras (mínimo: 30)
- `01.03.03` - Investimentos Verdes: Descrição muito curta: 19 palavras (mínimo: 30)
- `01.03.04` - Balança Comercial: Descrição muito curta: 24 palavras (mínimo: 30)
- `01.03.05` - Política de Comércio Internacional: Descrição muito curta: 18 palavras (mínimo: 30)
- `01.04.01` - Apoio Financeiro a Pequenas Empresas: Descrição muito curta: 24 palavras (mínimo: 30)
- `01.04.02` - Apoio Financeiro para Inovação: Descrição muito curta: 19 palavras (mínimo: 30)
- `01.04.03` - Financiamento de Infraestrutura: Descrição muito curta: 19 palavras (mínimo: 30)
- `01.04.04` - Microcrédito e Inclusão Financeira: Descrição muito curta: 23 palavras (mínimo: 30)
- `01.05.01` - Economia Circular: Descrição muito curta: 21 palavras (mínimo: 30)
- `01.05.02` - Economia Digital: Descrição muito curta: 22 palavras (mínimo: 30)
- ... e mais 457 nós

#### Severidade: BAIXO (529 problemas)


**below_recommended** (529 nós):

- `01` - Economia e Finanças: Abaixo do recomendado para L1: 25 palavras (recomendado: 80-200)
- `01.01` - Política Econômica: Abaixo do recomendado para L2: 40 palavras (recomendado: 50-150)
- `01.01.01` - Política Fiscal: Abaixo do recomendado para L3: 22 palavras (recomendado: 30-100)
- `01.01.02` - Autonomia Econômica: Abaixo do recomendado para L3: 22 palavras (recomendado: 30-100)
- `01.01.03` - Análise Econômica: Abaixo do recomendado para L3: 18 palavras (recomendado: 30-100)
- `01.01.04` - Boletim Econômico: Abaixo do recomendado para L3: 19 palavras (recomendado: 30-100)
- `01.02` - Fiscalização e Tributação: Abaixo do recomendado para L2: 44 palavras (recomendado: 50-150)
- `01.02.01` - Fiscalização Econômica: Abaixo do recomendado para L3: 22 palavras (recomendado: 30-100)
- `01.02.02` - Tributação e Impostos: Abaixo do recomendado para L3: 21 palavras (recomendado: 30-100)
- `01.02.03` - Combate à Evasão Fiscal: Abaixo do recomendado para L3: 24 palavras (recomendado: 30-100)
- `01.02.04` - Regulamentação Financeira: Abaixo do recomendado para L3: 23 palavras (recomendado: 30-100)
- `01.03` - Investimentos e Comércio Exterior: Abaixo do recomendado para L2: 36 palavras (recomendado: 50-150)
- `01.03.01` - Atração de Investimentos: Abaixo do recomendado para L3: 24 palavras (recomendado: 30-100)
- `01.03.02` - Investimentos no Exterior: Abaixo do recomendado para L3: 22 palavras (recomendado: 30-100)
- `01.03.03` - Investimentos Verdes: Abaixo do recomendado para L3: 19 palavras (recomendado: 30-100)
- `01.03.04` - Balança Comercial: Abaixo do recomendado para L3: 24 palavras (recomendado: 30-100)
- `01.03.05` - Política de Comércio Internacional: Abaixo do recomendado para L3: 18 palavras (recomendado: 30-100)
- `01.04` - Financiamento e Apoio Financeiro: Abaixo do recomendado para L2: 46 palavras (recomendado: 50-150)
- `01.04.01` - Apoio Financeiro a Pequenas Empresas: Abaixo do recomendado para L3: 24 palavras (recomendado: 30-100)
- `01.04.02` - Apoio Financeiro para Inovação: Abaixo do recomendado para L3: 19 palavras (recomendado: 30-100)
- ... e mais 509 nós

## 2. Recomendações

### Ações Sugeridas:

2. **Prioridade Alta:** Expandir descrições muito curtas (477 nós)
4. **Prioridade Baixa:** Ajustar para faixas recomendadas (529 nós)
