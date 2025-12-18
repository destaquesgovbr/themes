# Diagnóstico de Distribuição de Notícias por Tema

**Gerado em:** 2025-12-17
**Atualizado em:** 2025-12-18
**Fonte:** Typesense (collection: news)
**Total de documentos:** 308.427
**Status:** FASE 0 CONCLUÍDA

---

## 1. Distribuição por Tema - Nível 1

| # | Tema | Notícias | % | Status |
|---|------|----------|---|--------|
| 1 | Meio Ambiente e Sustentabilidade | 2.101 | 15.5% | SOBRECARREGADO |
| 2 | Saúde | 1.297 | 9.6% | Normal |
| 3 | Políticas Públicas e Governança | 1.083 | 8.0% | Normal |
| 4 | Segurança Pública | 1.050 | 7.7% | Normal |
| 5 | Ciência, Tecnologia e Inovação | 769 | 5.7% | Normal |
| 6 | Cultura, Artes e Patrimônio | 759 | 5.6% | Normal |
| 7 | Educação | 617 | 4.5% | Normal |
| 8 | Economia e Finanças | 604 | 4.5% | Normal |
| 9 | Justiça e Direitos Humanos | 543 | 4.0% | Normal |
| 10 | Infraestrutura e Transportes | 543 | 4.0% | Normal |
| 11 | Desenvolvimento Social | 527 | 3.9% | Normal |
| 12 | Agricultura, Pecuária e Abastecimento | 520 | 3.8% | Normal |
| 13 | Relações Internacionais e Diplomacia | 455 | 3.4% | Normal |
| 14 | Trabalho e Emprego | 424 | 3.1% | Normal |
| 15 | Energia e Recursos Minerais | 332 | 2.4% | Normal |
| 16 | Turismo | 206 | 1.5% | Baixo |
| 17 | Minorias e Grupos Especiais | 185 | 1.4% | Baixo |
| 18 | Esportes e Lazer | 155 | 1.1% | Baixo |
| 19 | Comunicações e Mídia | 138 | 1.0% | Baixo |
| 20 | Indústria e Comércio | 128 | 0.9% | Baixo |
| 21 | Legislação e Regulamentação | 106 | 0.8% | Baixo |
| 22 | Habitação e Urbanismo | 101 | 0.7% | Baixo |
| 23 | Defesa e Forças Armadas | 38 | 0.3% | MUITO BAIXO |
| 24 | Eventos Oficiais e Cerimônias | 33 | 0.2% | MUITO BAIXO |
| 25 | Estatísticas e Dados Públicos | 6 | 0.04% | CRÍTICO |

**Total classificado:** ~13.740 notícias (4.5% do total)

---

## 2. Distribuição por Tema - Nível 2 (Top 40)

| # | Subtema | Notícias | Tema Pai |
|---|---------|----------|----------|
| 1 | Mudanças Climáticas | 1.058 | Meio Ambiente |
| 2 | Conservação Ambiental | 871 | Meio Ambiente |
| 3 | Combate ao Crime Organizado | 536 | Segurança Pública |
| 4 | Vigilância Sanitária | 425 | Saúde |
| 5 | Administração Pública | 411 | Políticas Públicas |
| 6 | Sistema Único de Saúde (SUS) | 392 | Saúde |
| 7 | Pesquisa Científica | 347 | Ciência e Tecnologia |
| 8 | Fiscalização e Tributação | 286 | Economia |
| 9 | Participação e Colaboração Social | 284 | Políticas Públicas |
| 10 | Política Externa | 273 | Relações Internacionais |
| 11 | Campanhas de Saúde Pública | 261 | Saúde |
| 12 | Sistema Judiciário | 260 | Justiça |
| 13 | Ensino Superior | 246 | Educação |
| 14 | Programas Sociais | 243 | Desenvolvimento Social |
| 15 | Programas de Emprego | 238 | Trabalho |
| 16 | Eventos Culturais | 232 | Cultura |
| 17 | Programas e Políticas Educacionais | 219 | Educação |
| 18 | Preservação do Patrimônio | 210 | Cultura |
| 19 | Desenvolvimento Tecnológico | 203 | Ciência e Tecnologia |
| 20 | Agricultura Familiar | 201 | Agricultura |

**Observação:** Mudanças Climáticas + Conservação Ambiental = 1.929 (92% do tema Meio Ambiente)

---

## 3. Temas L2 com ZERO Notícias (8 temas)

| Subtema | Tema Pai | Observação |
|---------|----------|------------|
| Direitos Fundamentais | Justiça e Direitos Humanos | Sobrepõe com "Direitos Humanos" |
| Discursos Oficiais | Eventos Oficiais | Tema pai já tem baixo volume |
| Indicadores Econômicos e Sociais | Estatísticas | Tema pai crítico (6 notícias) |
| Luto Oficial | Eventos Oficiais | Tema muito específico |
| Planejamento Urbano | Habitação e Urbanismo | Possivelmente confundido com outros |
| Saneamento Básico | Habitação e Urbanismo | Pode estar em Meio Ambiente |
| Situações de Emergência | Defesa e Forças Armadas | Tema pai muito baixo |
| Transparência e Acesso à Informação | Estatísticas | Tema pai crítico |

---

## 4. Temas L2 com Volume Crítico (<10 notícias)

| Subtema | Notícias | Tema Pai |
|---------|----------|----------|
| Defesa Civil | 1 | Defesa |
| Saúde Mental | 1 | Saúde |
| Visitas Oficiais | 1 | Eventos Oficiais |
| Saúde da Criança | 1 | Saúde |
| Segurança Nacional | 1 | Defesa |
| Infraestrutura Urbana | 1 | Habitação |
| Políticas de Saúde Pública | 1 | Saúde |
| Controle de Fatores Ambientais | 1 | Saúde |
| Interoperabilidade | 2 | Estatísticas |
| Atenção ao Idoso | 2 | Desenvolvimento Social |
| Liberdade Religiosa | 2 | Justiça |
| Justiça Climática | 2 | Justiça |
| Política Externa Econômica | 2 | Relações Internacionais |
| Educação em Saúde | 3 | Saúde |
| Inaugurações | 4 | Eventos Oficiais |
| Cadeia Produtiva | 4 | Indústria |
| Relações Bilaterais | 4 | Relações Internacionais |
| Boas Práticas e Inovação Regulatória | 4 | Legislação |
| Reformas Legislativas | 5 | Legislação |
| Censos e Pesquisas | 6 | Estatísticas |
| Políticas de Lazer | 9 | Esportes |
| Desenvolvimento Urbano | 9 | Habitação |

**Total:** 22 subtemas L2 com menos de 10 notícias

---

## 5. Distribuição por Tema - Nível 3 (Top 30)

| # | Tema Específico | Notícias |
|---|-----------------|----------|
| 1 | Justiça Climática | 489 |
| 2 | Proteção da Vida Selvagem | 446 |
| 3 | Ciência Aberta | 314 |
| 4 | Serviços Públicos | 309 |
| 5 | Assistência em Saúde | 283 |
| 6 | Catástrofes Climáticas | 226 |
| 7 | Sociedade Civil | 223 |
| 8 | Agricultura Sustentável | 217 |
| 9 | Investigação de Organizações Criminosas | 207 |
| 10 | Educação Ambiental | 174 |
| 11 | Relações Bilaterais | 173 |
| 12 | Inspeção de Produtos | 166 |
| 13 | Desenvolvimento Sustentável | 155 |
| 14 | Tributação e Impostos | 143 |
| 15 | Pesquisa Acadêmica e Inovação | 139 |
| 16 | Recursos Hídricos | 131 |
| 17 | Assistência Técnica e Extensão Rural | 131 |
| 18 | Justiça e Lei | 121 |
| 19 | Políticas Antidiscriminatórias | 119 |
| 20 | Apresentações Artísticas | 117 |
| 21 | Inclusão no Trabalho | 112 |
| 22 | Combate à Fome | 110 |
| 23 | Saúde da Criança | 110 |
| 24 | Controle de Doenças | 110 |
| 25 | Políticas Educacionais | 108 |
| 26 | Repressão a Facções Criminosas | 100 |
| 27 | Saúde Mental | 97 |
| 28 | Energia Renovável | 97 |
| 29 | Transporte Aquaviário | 95 |
| 30 | Produção de Alimentos | 95 |

**Observação:** "Justiça Climática" aparece em L3 com 489 notícias, mas também existe em L2 do tema Justiça com apenas 2 notícias - inconsistência de classificação

---

## 6. Análise Estatística Consolidada

### Métricas Gerais

| Métrica | L1 | L2 | L3 |
|---------|----|----|-----|
| Total na árvore | 25 | 115 | 492 |
| Com notícias | 25 | 107 | ~300 |
| Com zero notícias | 0 | 8 | ~190 |
| Com <10 notícias | 3 | 22 | ~100 |

### Concentração

| Nível | Top 3 temas | % do total |
|-------|-------------|------------|
| L1 | Meio Ambiente, Saúde, Políticas Públicas | 33% |
| L2 | Mudanças Climáticas, Conservação, Combate Crime | 18% |
| L3 | Justiça Climática, Proteção Vida Selvagem, Ciência Aberta | 9% |

---

## 7. Problemas Identificados

### 7.1 Desbalanceamento Extremo
- Razão L1 maior/menor: **350:1**
- Meio Ambiente concentra 15.5% das notícias
- 3 temas L1 têm menos de 50 notícias cada

### 7.2 Temas Subutilizados
- 8 temas L2 com zero notícias
- 22 temas L2 com menos de 10 notícias
- ~190 temas L3 sem uso

### 7.3 Sobreposições Semânticas
- "Justiça Climática" aparece tanto em L2 (Justiça) quanto em L3 (Meio Ambiente)
- "Sustentabilidade" fragmentada entre Meio Ambiente, Ciência, Turismo
- "Direitos" divididos entre Justiça e Minorias

### 7.4 Temas Muito Específicos
- "Luto Oficial" (0 notícias)
- "Criptomoedas e Finanças Descentralizadas" (0 notícias)
- "Jogos de Inverno" (provavelmente irrelevante para Brasil)

### 7.5 Temas Genéricos Demais
- "Serviços Públicos" (309 notícias) - muito amplo
- "Sociedade Civil" (223 notícias) - vago

---

## 8. Recomendações Estruturais Atualizadas

### Fusões Recomendadas

| Tema Origem | Destino | Justificativa |
|-------------|---------|---------------|
| 23 - Estatísticas e Dados Públicos | 20 - Políticas Públicas | 6 notícias, subtemas sem uso |
| 22 - Eventos Oficiais e Cerimônias | Distribuir por assunto | 33 notícias, natureza transversal |
| 13.03 - Direitos Fundamentais | 13.02 - Direitos Humanos | Zero notícias, redundante |

### Subdivisões Recomendadas

| Tema | Ação | Justificativa |
|------|------|---------------|
| 05 - Meio Ambiente | Avaliar separar "Clima" | Mudanças Climáticas sozinho tem 1.058 |

### Remoções Recomendadas

| Tema | Motivo |
|------|--------|
| 09.01.03 - Jogos de Inverno | Irrelevante para Brasil |
| 22.04 - Luto Oficial | Muito específico, zero uso |
| Vários L3 com zero notícias | Granularidade excessiva |

---

## 9. Próximas Ações (Fase 1)

- [x] Coletar distribuição L1 do Typesense
- [x] Coletar distribuição L2 do Typesense
- [x] Coletar distribuição L3 do Typesense
- [x] Identificar temas L2/L3 com zero notícias
- [ ] Tomar decisões estruturais (DEC-001 a DEC-003)
- [ ] Escrever descrições L1 (25 temas)
