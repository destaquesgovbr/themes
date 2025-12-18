# Registro de Decisões Estruturais da Árvore Temática

**Criado em:** 2025-12-17
**Última atualização:** 2025-12-18

Este documento registra todas as decisões tomadas sobre a estrutura da árvore temática durante o processo de revisão.

---

## Resumo de Decisões

| ID | Título | Status |
|----|--------|--------|
| DEC-001 | Fusão de Estatísticas com Políticas Públicas | APROVADA |
| DEC-002 | Remoção de Eventos Oficiais | APROVADA |
| DEC-003 | Manter Meio Ambiente unificado | APROVADA |
| DEC-004 | Remoção de temas L2/L3 sem uso | APROVADA |
| DEC-005 | Fusão de Direitos Fundamentais com Direitos Humanos | APROVADA |

---

## Decisões Aprovadas

### DEC-001: Fusão de "Estatísticas e Dados Públicos" com "Políticas Públicas e Governança"

**Data:** 2025-12-17 | **Aprovada:** 2025-12-18
**Status:** APROVADA

**Contexto:**
O tema "23 - Estatísticas e Dados Públicos" possui apenas 6 notícias (0.04%). Seus subtemas têm volume crítico:
- Censos e Pesquisas: 6 notícias
- Indicadores Econômicos e Sociais: 0 notícias
- Interoperabilidade: 2 notícias
- Transparência e Acesso à Informação: 0 notícias

**Decisão:**
Fundir o tema 23 com o tema 20 (Políticas Públicas e Governança).

**Mapeamento de Subtemas:**
| Origem (23) | Destino (20) |
|-------------|--------------|
| 23.01 - Censos e Pesquisas | 20.01 - Transparência e Prestação de Contas |
| 23.02 - Indicadores | REMOVER (zero notícias) |
| 23.03 - Interoperabilidade | 20.03 - Gestão Pública |
| 23.04 - Transparência e Acesso | 20.01 - Transparência e Prestação de Contas |

**Impacto:**
- Redução de 25 para 24 temas L1
- Reclassificar 6 notícias
- Renumerar tema 24 (Minorias) para 23, tema 25 (Habitação) para 24

---

### DEC-002: Remoção de "Eventos Oficiais e Cerimônias"

**Data:** 2025-12-17 | **Aprovada:** 2025-12-18
**Status:** APROVADA

**Contexto:**
O tema "22 - Eventos Oficiais e Cerimônias" possui apenas 33 notícias (0.2%). Distribuição interna:
- Comemorações e Datas Festivas: 17 notícias
- Inaugurações: 4 notícias
- Visitas Oficiais: 1 notícia
- Discursos Oficiais: 0 notícias
- Luto Oficial: 0 notícias

**Decisão:**
Remover tema 22 e redistribuir notícias para temas por ASSUNTO, não por formato.

**Justificativa:**
- Eventos são transversais - o assunto do evento é mais relevante que o formato
- Uma inauguração de hospital vai para Saúde, não para Eventos
- Volume muito baixo confirma que classificadores já evitam este tema
- 2 dos 5 subtemas têm zero notícias

**Mapeamento:**
- As 33 notícias serão reclassificadas manualmente por assunto
- Subtemas serão removidos da árvore

**Impacto:**
- Redução para 23 temas L1 (após DEC-001)
- Renumeração dos temas subsequentes

---

### DEC-003: Manter "Meio Ambiente e Sustentabilidade" Unificado

**Data:** 2025-12-17 | **Aprovada:** 2025-12-18
**Status:** APROVADA

**Contexto:**
O tema "05 - Meio Ambiente e Sustentabilidade" concentra 15.5% das notícias (2.101). Distribuição L2:
- Mudanças Climáticas: 1.058 (50%)
- Conservação Ambiental: 871 (42%)
- Gestão de Resíduos e Licenciamento: 98 (5%)
- Energia Renovável e Limpa: 83 (4%)

**Decisão:**
MANTER o tema unificado, sem subdivisão.

**Justificativa:**
1. A concentração em Mudanças Climáticas e Conservação é coerente com a agenda atual do governo
2. Criar um tema separado "Clima" fragmentaria artificialmente assuntos relacionados
3. As descrições e keywords podem diferenciar melhor os subtemas sem necessidade de subdivisão
4. O desbalanceamento pode ser corrigido com melhores descrições, não com estrutura

**Impacto:**
- Nenhuma alteração estrutural
- Foco em descrições detalhadas para diferenciar subtemas

---

### DEC-004: Remoção de Temas L2/L3 sem Uso

**Data:** 2025-12-18
**Status:** APROVADA

**Contexto:**
Identificados 8 temas L2 com zero notícias e ~190 temas L3 sem uso.

**Decisão:**
Remover temas com zero notícias E baixa probabilidade de uso futuro.

**Lista de Remoções L2:**
| Tema | Motivo |
|------|--------|
| 13.03 - Direitos Fundamentais | Redundante com Direitos Humanos |
| 22.01 - Discursos Oficiais | Tema pai removido (DEC-002) |
| 22.04 - Luto Oficial | Tema pai removido, muito específico |
| 23.02 - Indicadores Econômicos | Tema pai fundido (DEC-001) |
| 23.04 - Transparência e Acesso | Tema pai fundido (DEC-001) |

**Lista de Remoções L3 (exemplos):**
| Tema | Motivo |
|------|--------|
| 09.01.03 - Jogos de Inverno | Irrelevante para Brasil |
| 01.05.04 - Criptomoedas e Finanças Descentralizadas | Muito específico, zero uso |

**Impacto:**
- Redução de ~115 para ~107 temas L2
- Redução de ~492 para ~400 temas L3
- Árvore mais enxuta e focada

---

### DEC-005: Fusão de "Direitos Fundamentais" com "Direitos Humanos"

**Data:** 2025-12-18
**Status:** APROVADA

**Contexto:**
O subtema "13.03 - Direitos Fundamentais" tem zero notícias e sobrepõe semanticamente com "13.02 - Direitos Humanos".

**Decisão:**
Remover 13.03 e manter apenas 13.02 - Direitos Humanos.

**Justificativa:**
- Zero notícias indica que o classificador não diferencia os dois
- Conceitualmente, direitos fundamentais são um subconjunto de direitos humanos
- Simplificação sem perda de cobertura

**Impacto:**
- Tema 13 fica com 2 subtemas L2 ao invés de 3

---

## Decisões Implementadas

*(Implementação será feita na criação do themes_tree_enriched.yaml)*

---

## Histórico de Alterações

| Data | Alteração |
|------|-----------|
| 2025-12-17 | Criação do documento com 3 propostas iniciais |
| 2025-12-18 | Atualização com dados de L2/L3, aprovação de decisões |
| 2025-12-18 | Adição de DEC-004 e DEC-005 |

---

## Estrutura Final Proposta

Após aplicar todas as decisões:

| Código | Tema L1 |
|--------|---------|
| 01 | Economia e Finanças |
| 02 | Educação |
| 03 | Saúde |
| 04 | Segurança Pública |
| 05 | Meio Ambiente e Sustentabilidade |
| 06 | Ciência, Tecnologia e Inovação |
| 07 | Infraestrutura e Transportes |
| 08 | Cultura, Artes e Patrimônio |
| 09 | Esportes e Lazer |
| 10 | Agricultura, Pecuária e Abastecimento |
| 11 | Indústria e Comércio |
| 12 | Relações Internacionais e Diplomacia |
| 13 | Justiça e Direitos Humanos |
| 14 | Trabalho e Emprego |
| 15 | Desenvolvimento Social |
| 16 | Turismo |
| 17 | Energia e Recursos Minerais |
| 18 | Comunicações e Mídia |
| 19 | Defesa e Forças Armadas |
| 20 | Políticas Públicas e Governança |
| 21 | Legislação e Regulamentação |
| 22 | Minorias e Grupos Especiais |
| 23 | Habitação e Urbanismo |

**Total:** 23 temas L1 (redução de 2)
