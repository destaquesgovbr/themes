# Case Study: Engenharia de Prompt para Tarefas Longas com LLM

**Autor:** Nitai
**Data:** 2025-12-17
**Ferramenta:** Claude Code (Claude Opus 4.5)

---

## Resumo Executivo

Este documento descreve uma estratégia de Engenharia de Prompt para executar tarefas complexas e longas com LLMs, superando a limitação de "amnésia" (perda de contexto entre sessões). A abordagem consiste em:

1. **Fornecer contexto rico** no prompt inicial
2. **Solicitar um plano detalhado** com múltiplas fases
3. **Criar documentos de memória externa** que persistem entre sessões
4. **Estruturar a execução** para maximizar o investimento de capacidade do LLM

---

## 1. O Problema: Amnésia do LLM

### Limitação Fundamental

LLMs não possuem memória persistente entre sessões. Cada nova conversa começa do zero. Para tarefas que exigem múltiplas sessões de trabalho, isso significa:

- Perda de contexto e decisões anteriores
- Necessidade de re-explicar o problema a cada sessão
- Inconsistência nas abordagens ao longo do tempo
- Desperdício de tokens re-estabelecendo contexto

### O Caso Concreto

**Tarefa:** Melhorar a árvore temática do projeto DestaquesGovBr
- ~540 nós (25 L1 + 113 L2 + 400 L3)
- Cada nó precisa de descrição, keywords, exemplos
- Decisões estruturais (fusão/divisão de temas)
- Impossível completar em uma única sessão

---

## 2. A Solução: Memória Externa + Planejamento Estruturado

### Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPT INICIAL                           │
│  (Contexto rico + Pedido de plano + Acesso a dados)        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASE DE PLANEJAMENTO                     │
│  LLM analisa, consulta dados, faz perguntas, cria plano    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              DOCUMENTOS DE MEMÓRIA EXTERNA                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ PLANO.md     │ │ DECISOES.md  │ │ PROGRESSO.md │        │
│  │ (fases)      │ │ (histórico)  │ │ (status)     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   SESSÕES DE EXECUÇÃO                       │
│  Sessão 1 → lê docs → executa fase → atualiza docs         │
│  Sessão 2 → lê docs → executa fase → atualiza docs         │
│  Sessão N → lê docs → executa fase → atualiza docs         │
└─────────────────────────────────────────────────────────────┘
```

### Benefícios

1. **Contexto preservado:** Documentos persistem entre sessões
2. **Consistência:** Decisões registradas evitam contradições
3. **Rastreabilidade:** Histórico completo do processo
4. **Eficiência:** Menos tokens gastos re-explicando contexto
5. **Colaboração:** Documentos podem ser revisados por humanos

---

## 3. O Prompt Inicial

### Prompt Utilizado

```
Neste diretório @/Users/nitai/Dropbox/dev-mgi/destaquesgovbr/themes existe
a árvore temática utilizada no projeto DestaquesGovBr. Mais sobre o projeto
e o uso da árvore, em @/Users/nitai/Dropbox/dev-mgi/destaquesgovbr/docs

Precisamos melhorar esta árvore temática. Esta árvore foi gerada por um
processo pouco controlado e não teve revisão. Por isso ela sofre de vários
problemas. Por exemplo, existe desbalanceamento em algumas sub árvores.
Em alguns casos temas muito específicos que não deveriam estar na árvore,
em outros casos falta de temas. No portal existe uma tela que mostra a
quantidade de notícias por tema no último mês. É visível um desbalanceamento.
Temas com muito mais notícias que outros. Claro que existe um volume maior
de notícias em certos temas do governo. Também temos que considerar que o
processo de classificação pode ser enviesado.

O processo de classificação é baseado em LLM e utiliza um prompt simples
para classificação em 2 etapas. Na primeira etapa é pedido para classificar
o conteúdo de uma notícia dentre os 25 temas de primeiro nível. Depois é
pedido para classificar dentre os subtemas de segundo e terceiro nível.
Esse processo em 2 etapas reduz o número de opções em cada etapa para o
LLM decidir, já que a árvore tem mais de 600 nós. Além disso o processo
de classificação se baseia apenas no "nome" do tema. Uma das melhorias
que precisamos fazer é adicionar descrição para cada tema e com isso
evoluir o processo de classificação para utilizar um RAG, e o match ser
mais semântico.

Uma das minhas questões é qual a abordagem que devemos seguir para criar
as descrições, botton up ou top down. [...] Decidindo isso precisamos
criar um processo metódico para escrita das descrições e um plano com
várias fases para cobrir tudo.

Se achar interessante você pode/poderá acessar o typesense em produção
para consultar e constatar o desbalanceamento a que me referi. [...]

Conexão typesense
{
  "host": "34.39.186.38",
  "port": 8108,
  "protocol": "http",
  "searchOnlyApiKey": "..."
}

A árvore é um vocabulário controlado.

Crie um plano
```

### Análise do Prompt

| Elemento | Propósito | Exemplo no Prompt |
|----------|-----------|-------------------|
| **Contexto do projeto** | Situar o LLM no domínio | "projeto DestaquesGovBr", referência a docs |
| **Problema específico** | Definir o que precisa ser resolvido | "desbalanceamento", "temas específicos demais" |
| **Contexto técnico** | Explicar como o sistema funciona | "classificação em 2 etapas", "mais de 600 nós" |
| **Objetivo claro** | O que queremos alcançar | "adicionar descrição", "RAG semântico" |
| **Dúvida explícita** | Engajar o LLM em decisão | "bottom up ou top down?" |
| **Acesso a dados** | Permitir validação empírica | Credenciais do Typesense |
| **Pedido de plano** | Solicitar estrutura | "plano com várias fases" |

---

## 4. A Interação de Planejamento

### Fluxo da Conversa

```
HUMANO: [Prompt inicial com contexto]
   │
   ▼
CLAUDE: Explora o código (3 agentes paralelos)
        - Agente 1: Estrutura da árvore temática
        - Agente 2: Processo de classificação
        - Agente 3: Documentação do projeto
   │
   ▼
CLAUDE: Consulta Typesense para dados reais
        → Descobre desbalanceamento 350:1
   │
   ▼
CLAUDE: Faz perguntas de esclarecimento
        - Abordagem: top-down, bottom-up ou híbrido?
        - Foco: LLM, RAG ou ambos?
        - Escopo: só descrições ou revisão estrutural também?
   │
   ▼
HUMANO: Responde às perguntas
        - Híbrido
        - Ambos (RAG primeiro, LLM depois)
        - Descrições + revisão estrutural
   │
   ▼
CLAUDE: Cria plano detalhado com 5 fases
   │
   ▼
HUMANO: "Escreva em documentos de suporte"
   │
   ▼
CLAUDE: Cria 6 documentos de memória externa
```

### Perguntas do Claude

O Claude fez 3 perguntas estratégicas antes de criar o plano:

1. **Qual a abordagem para criar descrições?**
   - Top-down (L1 → L2 → L3)
   - Bottom-up (L3 → L2 → L1)
   - Híbrido (L1 → L3 → L2) ← *Escolhido*

2. **Qual o foco das descrições?**
   - Classificação LLM
   - RAG/Embeddings
   - Ambos ← *Escolhido*

3. **Escopo do trabalho?**
   - Apenas descrições
   - Descrições + revisão estrutural ← *Escolhido*

---

## 5. Os Documentos de Memória Externa

### Estrutura Criada

```
themes/
├── README.md                      # Visão geral do diretório
├── PLANO_ARVORE_TEMATICA.md       # Plano mestre
├── DIAGNOSTICO_DISTRIBUICAO.md   # Dados coletados
├── DECISOES_ESTRUTURAIS.md       # Registro de decisões
├── TEMPLATE_DESCRICOES.md        # Padrão para descrições
├── PROGRESSO_DESCRICOES.md       # Status por tema
└── themes_tree.yaml              # Árvore atual
```

### Propósito de Cada Documento

| Documento | Função na Memória | Conteúdo |
|-----------|-------------------|----------|
| **PLANO** | Roteiro de execução | Fases, tarefas, critérios de sucesso |
| **DIAGNOSTICO** | Dados empíricos | Estatísticas do Typesense, análises |
| **DECISOES** | Histórico de escolhas | Cada decisão com contexto e justificativa |
| **TEMPLATE** | Padrão de qualidade | Formato e critérios para descrições |
| **PROGRESSO** | Estado atual | Checklist por tema, % concluído |

### Formato do Registro de Decisões

```markdown
### DEC-001: Fusão de "Estatísticas" com "Políticas Públicas"

**Data:** 2025-12-17
**Status:** PROPOSTA | APROVADA | IMPLEMENTADA | REJEITADA

**Contexto:**
[Por que estamos considerando isso]

**Decisão:**
[O que foi decidido]

**Justificativa:**
[Por que esta decisão]

**Impacto:**
[Consequências]

**Ações:**
- [ ] Tarefa 1
- [ ] Tarefa 2
```

---

## 6. Princípios de Engenharia de Prompt Aplicados

### 1. Contexto Rico e Específico

**Princípio:** Quanto mais contexto relevante, melhor a resposta.

**Aplicação:**
- Referência a diretórios e arquivos específicos
- Explicação do processo de classificação atual
- Dados de acesso ao Typesense para validação

### 2. Perguntas Antes de Ação

**Princípio:** O LLM deve clarificar ambiguidades antes de executar.

**Aplicação:**
- Claude fez 3 perguntas estratégicas
- Respostas informaram o design do plano
- Evitou retrabalho por mal-entendido

### 3. Planejamento Explícito

**Princípio:** Pedir um plano antes da execução melhora a qualidade.

**Aplicação:**
- Solicitação explícita: "Crie um plano"
- Plano com fases numeradas e tarefas específicas
- Critérios de sucesso definidos

### 4. Memória Externa

**Princípio:** Documentos persistentes superam a amnésia do LLM.

**Aplicação:**
- 6 documentos com funções específicas
- Formato estruturado para fácil leitura pelo LLM
- Histórico e status atualizáveis

### 5. Decomposição de Tarefas

**Princípio:** Tarefas grandes devem ser divididas em menores.

**Aplicação:**
- 5 fases distintas
- Cada fase com entregáveis claros
- Progresso rastreável tema a tema

---

## 7. Como Usar Esta Estratégia

### Passo a Passo

1. **Prepare o contexto**
   - Identifique todos os arquivos/dados relevantes
   - Documente o processo atual
   - Liste os problemas específicos

2. **Construa o prompt inicial**
   - Comece com contexto do projeto
   - Descreva o problema em detalhes
   - Explique o objetivo desejado
   - Faça perguntas que precisam de resposta
   - Forneça acesso a dados (APIs, arquivos)
   - Peça explicitamente um plano

3. **Responda às perguntas do LLM**
   - Não apresse a execução
   - Decisões tomadas aqui afetam todo o plano

4. **Solicite documentos de suporte**
   - Peça ao LLM criar documentos de memória
   - Defina o propósito de cada documento
   - Mantenha em local persistente (não efêmero)

5. **Execute em sessões**
   - Cada nova sessão: "Leia os documentos em X e continue"
   - Atualize documentos após cada sessão
   - Registre decisões no momento em que são tomadas

### Template de Prompt para Tarefas Longas

```
[CONTEXTO DO PROJETO]
Descreva o projeto, arquivos relevantes, como o sistema funciona.

[PROBLEMA]
Descreva o problema específico que precisa ser resolvido.

[OBJETIVO]
O que queremos alcançar ao final.

[QUESTÕES EM ABERTO]
Liste dúvidas que precisam de decisão.

[ACESSO A DADOS]
Forneça credenciais/caminhos para validação empírica.

[PEDIDO]
"Crie um plano detalhado com múltiplas fases. Depois, crie
documentos de suporte para acompanhar a execução ao longo
de várias sessões, superando a limitação de memória entre
conversas."
```

---

## 8. Resultados Obtidos

### Métricas

| Métrica | Valor |
|---------|-------|
| Tokens no prompt inicial | ~800 |
| Documentos criados | 6 |
| Fases do plano | 5 |
| Temas a processar | ~540 |
| Decisões estruturais identificadas | 3 |

### Entregáveis

1. Plano detalhado com 5 fases
2. Diagnóstico com dados reais (desbalanceamento 350:1)
3. 3 propostas de decisão estrutural documentadas
4. Template para garantir consistência
5. Sistema de rastreamento de progresso

### Benefício Principal

**Sem esta estratégia:** Cada sessão começaria do zero, repetindo contexto,
possivelmente tomando decisões inconsistentes.

**Com esta estratégia:** Cada sessão começa lendo os documentos, tem contexto
completo, segue o plano estabelecido, e atualiza o estado para a próxima sessão.

---

## 9. Conclusão

A combinação de **contexto rico**, **planejamento explícito** e **memória externa**
permite usar LLMs para tarefas que excedem uma única sessão. O investimento inicial
em estruturar o problema e criar documentos de suporte paga dividendos em:

- Consistência ao longo do tempo
- Rastreabilidade de decisões
- Eficiência no uso de tokens
- Possibilidade de colaboração humana

Esta arquitetura de Engenharia de Prompt transforma o LLM de uma ferramenta de
sessão única em um assistente para projetos de longo prazo.

---

## Anexo: Prompts Completos da Sessão

### Prompt 1 (Inicial)
*(Ver seção 3)*

### Prompt 2 (Documentação)
```
Escreva esse plano em um documento em @/Users/nitai/Dropbox/dev-mgi/destaquesgovbr/themes
Vamos usar ele para acompanhar a execução, já que vamos executar em fases e
precisamos preservar a memória da execução durante as várias interações e não
sermos afetados pela amnésia do LLM. Crie outros documentos de suporte nesse
processo de execução do plano que você achar importante
```

### Prompt 3 (Este documento)
```
Agora crie um novo documento relatando como chegamos a este plano. Basicamente
quero poder compartilhar com meus colegas os prompts que eu utilizei e destacar
a minha estratégia de, fornecer contexto suficiente, e pedir ao Claude Code para
criar um plano longo com várias etapas e com documentos de suporte à execução do
plano para superar a amnésia. E dessa forma conseguir investir mais poder de LLM
no resultado final. Quero enfatizar essa arquitetura de Engenharia de Prompt.
Este documento não é para servir de suporte ao processo de execução
```
