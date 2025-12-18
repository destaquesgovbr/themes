# Relatório de Análise de Similaridade Semântica - Subfase 4.2

**Modelo de embeddings:** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`

**Threshold de similaridade:** 0.85

## Sumário Executivo

- **Pares L2 com alta similaridade:** 19
- **Pares L3 com alta similaridade:** 8
- **Total de problemas identificados:** 27

## Pares L2 Similares

| Código 1 | Label 1 | Código 2 | Label 2 | Similaridade |
|----------|---------|----------|---------|-------------|
| 10.03 | Política Agrícola | 10.04 | Agricultura Familiar | 0.949 |
| 10.01 | Agronegócio | 10.03 | Política Agrícola | 0.947 |
| 10.01 | Agronegócio | 10.04 | Agricultura Familiar | 0.937 |
| 03.02 | Campanhas de Saúde Pública | 03.04 | Saúde Pública | 0.932 |
| 16.02 | Infraestrutura Turística | 16.03 | Eventos Turísticos | 0.932 |
| 16.02 | Infraestrutura Turística | 16.04 | Sustentabilidade no Turismo | 0.921 |
| 03.04 | Saúde Pública | 03.05 | Programas e Projetos em Saúde | 0.907 |
| 16.03 | Eventos Turísticos | 16.04 | Sustentabilidade no Turismo | 0.899 |
| 24.02 | Populações Indígenas | 24.04 | Comunidades Tradicionais | 0.891 |
| 09.03 | Incentivo ao Esporte | 09.04 | Esporte e Inclusão | 0.884 |
| 24.03 | Comunidade LGBTQIA+ | 24.05 | Direitos das Pessoas com Deficiência | 0.880 |
| 10.03 | Política Agrícola | 10.05 | Sanidade | 0.879 |
| 15.01 | Programas Sociais | 15.02 | Combate à Pobreza | 0.878 |
| 03.02 | Campanhas de Saúde Pública | 03.05 | Programas e Projetos em Saúde | 0.872 |
| 05.01 | Conservação Ambiental | 05.02 | Mudanças Climáticas | 0.864 |
| 05.02 | Mudanças Climáticas | 05.03 | Energia Renovável e Limpa | 0.864 |
| 10.02 | Segurança Alimentar | 10.05 | Sanidade | 0.862 |
| 25.04 | Desenvolvimento Urbano | 25.05 | Infraestrutura Urbana | 0.853 |
| 03.03 | Vigilância Sanitária | 03.04 | Saúde Pública | 0.851 |
## Pares L3 Similares (Top 50)

| Código 1 | Label 1 | Código 2 | Label 2 | Similaridade |
|----------|---------|----------|---------|-------------|
| 09.03.02 | Desenvolvimento Esportivo | 09.03.04 | Educação e Formação no Esporte | 0.923 |
| 10.05.02 | Sanidade Vegetal | 10.05.03 | Controle de Pragas e Doenças | 0.897 |
| 09.01.01 | Jogos Olímpicos | 09.01.05 | Competições Internacionais | 0.895 |
| 06.04.02 | Inovação e Descarbonização | 06.04.03 | Tecnologias Verdes | 0.882 |
| 21.03.02 | Recebimento de Contribuições | 21.03.03 | Análise de Contribuições | 0.874 |
| 21.03.01 | Abertura de Consultas | 21.03.02 | Recebimento de Contribuições | 0.867 |
| 06.04.01 | Inovação e Sustentabilidade | 06.04.03 | Tecnologias Verdes | 0.865 |
| 21.03.01 | Abertura de Consultas | 21.03.03 | Análise de Contribuições | 0.862 |

## Recomendações

### Prioridade Média: Revisar L2 similares

Os seguintes pares de subtemas L2 possuem descrições muito similares e podem causar confusão na classificação:

- **10.03** (Política Agrícola) ↔ **10.04** (Agricultura Familiar): 0.949
  → Adicionar termos distintivos às descrições

- **10.01** (Agronegócio) ↔ **10.03** (Política Agrícola): 0.947
  → Adicionar termos distintivos às descrições

- **10.01** (Agronegócio) ↔ **10.04** (Agricultura Familiar): 0.937
  → Adicionar termos distintivos às descrições

- **03.02** (Campanhas de Saúde Pública) ↔ **03.04** (Saúde Pública): 0.932
  → Adicionar termos distintivos às descrições

- **16.02** (Infraestrutura Turística) ↔ **16.03** (Eventos Turísticos): 0.932
  → Adicionar termos distintivos às descrições

- **16.02** (Infraestrutura Turística) ↔ **16.04** (Sustentabilidade no Turismo): 0.921
  → Adicionar termos distintivos às descrições

- **03.04** (Saúde Pública) ↔ **03.05** (Programas e Projetos em Saúde): 0.907
  → Adicionar termos distintivos às descrições

- **16.03** (Eventos Turísticos) ↔ **16.04** (Sustentabilidade no Turismo): 0.899
  → Adicionar termos distintivos às descrições

- **24.02** (Populações Indígenas) ↔ **24.04** (Comunidades Tradicionais): 0.891
  → Adicionar termos distintivos às descrições

- **09.03** (Incentivo ao Esporte) ↔ **09.04** (Esporte e Inclusão): 0.884
  → Adicionar termos distintivos às descrições

