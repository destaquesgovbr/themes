# Fase 4: Validação e Refinamento da Árvore Temática

Este diretório contém todos os scripts, dados e relatórios da **Fase 4** do projeto de refinamento da árvore temática DestaquesGovBr.

## 📋 Visão Geral

A Fase 4 consiste em 6 subfases para validar e refinar a árvore temática enriquecida:

1. **Subfase 4.1:** Validação de Consistência Estrutural
2. **Subfase 4.2:** Validação de Qualidade das Descrições
3. **Subfase 4.3:** Preparação de Dataset de Teste
4. **Subfase 4.4:** Testes de Classificação Comparativos
5. **Subfase 4.5:** Análise de Resultados e Ajustes Iterativos
6. **Subfase 4.6:** Documentação Final e Entrega

**Documentação detalhada:** [FASE_4_DETALHAMENTO.md](./FASE_4_DETALHAMENTO.md)

## 📂 Estrutura de Diretórios

```
_plan_refinamento/
├── README.md                    # Este arquivo
├── FASE_4_DETALHAMENTO.md       # Plano detalhado completo
├── requirements.txt             # Dependências Python
├── .python-version              # Python 3.13
│
├── scripts/                     # Scripts Python organizados
│   ├── config.py               # Configurações globais
│   ├── utils/                  # Utilitários compartilhados
│   ├── validacao/              # Subfase 4.1 e 4.2
│   ├── dataset/                # Subfase 4.3
│   ├── classificacao/          # Subfase 4.4
│   └── refinamento/            # Subfase 4.5
│
├── data/                        # Dados gerados
│   ├── test_dataset.csv
│   ├── embeddings_cache/       # Cache de embeddings
│   └── annotations/            # Anotações manuais
│
├── reports/                     # Relatórios gerados
│   ├── 01_estrutura_report.md
│   ├── 02_qualidade_report.md
│   ├── 03_classification_guide.md
│   ├── 04_classification_results.md
│   ├── 05_ajustes_realizados.md
│   └── 06_RELATORIO_VALIDACAO_FINAL.md
│
└── notebooks/                   # Jupyter notebooks
    └── 06_classification_examples.ipynb
```

## 🚀 Início Rápido

### 1. Ativar Ambiente Virtual

```bash
# Ativar virtual env do Poetry
source /Users/nitai/Library/Caches/pypoetry/virtualenvs/govbr-news-ai-_H0Lmpg7-py3.13/bin/activate

# Verificar Python 3.13
python --version
```

### 2. Instalar Dependências

```bash
cd /Users/nitai/Dropbox/dev-mgi/destaquesgovbr/themes/_plan_refinamento
pip install -r requirements.txt
```

### 3. Executar Subfase 4.1 (Validação Estrutural)

```bash
python scripts/validacao/01_validate_structure.py
```

## 📊 Subfases Detalhadas

### Subfase 4.1: Validação Estrutural

**Scripts:**
- `scripts/validacao/01_validate_structure.py`

**Output:**
- `reports/01_estrutura_report.md`
- `reports/01_estrutura_stats.json`

**Como executar:**
```bash
python scripts/validacao/01_validate_structure.py
```

---

### Subfase 4.2: Validação de Qualidade

**Scripts:**
- `scripts/validacao/02_validate_quality.py`
- `scripts/validacao/02_analyze_similarity.py`
- `scripts/validacao/02_check_keywords.py`

**Output:**
- `reports/02_qualidade_report.md`
- `reports/02_problemas_qualidade.csv`
- `reports/02_similarity_matrix_L2.png`
- `reports/02_similarity_matrix_L3.png`

**Como executar:**
```bash
python scripts/validacao/02_validate_quality.py
python scripts/validacao/02_analyze_similarity.py
python scripts/validacao/02_check_keywords.py
```

---

### Subfase 4.3: Dataset de Teste

**Scripts:**
- `scripts/dataset/03_collect_news.py`
- `scripts/dataset/03_annotation_app.py`
- `scripts/dataset/03_validate_annotations.py`

**Output:**
- `data/test_dataset.csv`
- `reports/03_classification_guide.md`
- `reports/03_dataset_stats.md`

**Como executar:**
```bash
# Coletar notícias do Typesense
python scripts/dataset/03_collect_news.py

# Abrir interface de anotação (Streamlit)
streamlit run scripts/dataset/03_annotation_app.py

# Validar anotações
python scripts/dataset/03_validate_annotations.py
```

---

### Subfase 4.4: Testes de Classificação

**Scripts:**
- `scripts/classificacao/04_classifier.py`
- `scripts/classificacao/04_run_tests.py`
- `scripts/classificacao/04_calculate_metrics.py`
- `scripts/classificacao/04_analyze_errors.py`

**Output:**
- `reports/04_classification_results.md`
- `reports/04_metrics_summary.json`
- `reports/04_best_strategy_recommendation.md`
- `reports/04_confusion_matrices/`
- `reports/04_classification_errors.csv`

**Como executar:**
```bash
# Executar todos os testes (20 combinações)
python scripts/classificacao/04_run_tests.py

# Calcular métricas
python scripts/classificacao/04_calculate_metrics.py

# Analisar erros
python scripts/classificacao/04_analyze_errors.py
```

---

### Subfase 4.5: Refinamento

**Scripts:**
- `scripts/refinamento/05_analyze_confusions.py`
- `scripts/refinamento/05_suggest_fixes.py`
- `scripts/refinamento/05_apply_fixes.py`
- `scripts/refinamento/05_retest_themes.py`

**Output:**
- `reports/05_ajustes_realizados.md`
- `themes_tree_enriched_full.yaml` (versão 3.2+)
- `reports/05_improvements.md`
- `reports/05_iteration_log.md`

**Como executar:**
```bash
# Analisar confusões
python scripts/refinamento/05_analyze_confusions.py

# Sugerir correções
python scripts/refinamento/05_suggest_fixes.py

# Aplicar correções aprovadas
python scripts/refinamento/05_apply_fixes.py

# Re-testar temas modificados
python scripts/refinamento/05_retest_themes.py
```

---

### Subfase 4.6: Documentação Final

**Output:**
- `reports/06_RELATORIO_VALIDACAO_FINAL.md`
- `reports/06_GUIA_USO_ARVORE_TEMATICA.md`
- `notebooks/06_classification_examples.ipynb`
- `reports/06_performance_benchmark.md`

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz deste diretório:

```env
# Caminhos
THEMES_FILE=../themes_tree_enriched_full.yaml
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_API_KEY=sua_chave_aqui

# Modelo de Embeddings
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
EMBEDDING_CACHE_DIR=data/embeddings_cache

# Thresholds
CONFIDENCE_THRESHOLD_L1=0.4
CONFIDENCE_THRESHOLD_L2=0.5
CONFIDENCE_THRESHOLD_L3=0.6

# Dataset
TEST_DATASET_SIZE=500
ANNOTATION_BATCH_SIZE=50
```

### Config.py

O arquivo `scripts/config.py` carrega todas as configurações automaticamente.

## 📈 Critérios de Sucesso

### Qualidade Técnica
- ✅ 0 erros estruturais no YAML
- ✅ 100% dos nós com campos obrigatórios
- ✅ < 5% de descrições com problemas ortográficos

### Qualidade Semântica
- ✅ < 10% de pares de irmãos com similaridade > 0.85
- ✅ Keywords relevantes e específicas
- ✅ Descrições com comprimento adequado

### Performance de Classificação
- ✅ Acurácia L1 ≥ 85% (top-1)
- ✅ Acurácia L2 ≥ 70% (top-1)
- ✅ Acurácia L3 ≥ 60% (top-1)
- ✅ Acurácia hierárquica completa ≥ 55%

## 🐛 Troubleshooting

### Erro: Modelo de embeddings não encontrado

```bash
# Baixar modelo manualmente
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### Erro: Memória insuficiente

- Reduzir batch size de embeddings em `config.py`
- Usar modelo menor: `distiluse-base-multilingual-cased-v2`

### Erro: Typesense connection refused

- Verificar se Typesense está rodando: `docker ps | grep typesense`
- Verificar credenciais em `.env`

## 📞 Suporte

Para dúvidas ou problemas:
1. Consultar [FASE_4_DETALHAMENTO.md](./FASE_4_DETALHAMENTO.md)
2. Verificar logs em `reports/`
3. Abrir issue no repositório

## 📝 Licença

Projeto interno - DestaquesGovBr
