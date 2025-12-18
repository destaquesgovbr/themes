# Relatório de Coleta do Dataset de Teste - Subfase 4.3

**Dataset fonte:** `nitaibezerra/govbrnews`

**Tamanho da amostra:** 500 documentos

## Estatísticas Gerais

- **Temas L1 únicos:** 25
- **Órgãos únicos:** 98

## Distribuição de Complexidade Estimada

| Complexidade | Quantidade | Percentual |
|--------------|------------|------------|
| Clara | 46 | 9.2% |
| Moderada | 310 | 62.0% |
| Dificil | 144 | 28.8% |

## Top 10 Temas L1 na Amostra

| Código | Quantidade | Percentual |
|--------|------------|------------|
| 20 | 5 | 1.0% |
| 04 | 4 | 0.8% |
| 05 | 4 | 0.8% |
| 06 | 3 | 0.6% |
| 15 | 3 | 0.6% |
| 25 | 2 | 0.4% |
| 18 | 2 | 0.4% |
| 03 | 2 | 0.4% |
| 10 | 2 | 0.4% |
| 21 | 2 | 0.4% |

## Próximos Passos

1. Usar interface de anotação (`03_annotation_app.py`) para classificar manualmente
2. Preencher colunas: `L1_anotado`, `L2_anotado`, `L3_anotado`, `confianca`
3. Executar validação de anotações (`03_validate_annotations.py`)
4. Usar dataset anotado para testes de classificação (Subfase 4.4)
