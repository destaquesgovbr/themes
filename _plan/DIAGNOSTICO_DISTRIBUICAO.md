# Diagnóstico de Distribuição de Notícias por Tema

**Gerado em:** 2025-12-17
**Fonte:** Typesense (collection: news)
**Total de documentos:** 308.303

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

**Total classificado:** ~13.740 notícias (4.5% do total de 308.303)
**Observação:** A maioria das notícias ainda não foi classificada

---

## 2. Análise Estatística

### Métricas de Desbalanceamento

| Métrica | Valor |
|---------|-------|
| Maior tema | Meio Ambiente (2.101) |
| Menor tema | Estatísticas (6) |
| Razão maior/menor | **350:1** |
| Mediana | ~455 (Relações Internacionais) |
| Média | ~550 |

### Distribuição por Faixas

| Faixa | Temas | Lista |
|-------|-------|-------|
| >1000 notícias | 4 | Meio Ambiente, Saúde, Políticas Públicas, Segurança |
| 500-1000 | 8 | Ciência, Cultura, Educação, Economia, Justiça, Infraestrutura, Desenvolvimento, Agricultura |
| 100-500 | 9 | Relações Internacionais, Trabalho, Energia, Turismo, Minorias, Esportes, Comunicações, Indústria, Legislação, Habitação |
| <100 | 3 | Defesa, Eventos, Estatísticas |

---

## 3. Distribuição por Tema - Nível 2

**A COLETAR** - Executar consulta Typesense com facet em `theme_1_level_2_label`

---

## 4. Distribuição por Tema - Nível 3

**A COLETAR** - Executar consulta Typesense com facet em `theme_1_level_3_label`

---

## 5. Temas com Zero Notícias

**A IDENTIFICAR** - Comparar lista de temas L2/L3 da árvore com facets do Typesense

---

## 6. Análise de Sobreposições Semânticas

### Candidatos a Sobreposição (análise manual necessária)

| Tema A | Tema B | Razão da Suspeita |
|--------|--------|-------------------|
| 05 - Meio Ambiente | 06.04 - Sustentabilidade e Descarbonização | Ambos tratam de sustentabilidade |
| 01.05 - Novas Economias | 06.03 - Inovação | Economia digital vs inovação |
| 13 - Justiça e Direitos Humanos | 24 - Minorias e Grupos Especiais | Ambos tratam de direitos |
| 20 - Políticas Públicas | 21 - Legislação | Governança vs regulamentação |
| 23 - Estatísticas | 20 - Políticas Públicas | Dados públicos vs transparência |

---

## 7. Recomendações Estruturais

### Candidatos a Fusão (volume muito baixo)

| Tema | Notícias | Sugestão de Destino | Justificativa |
|------|----------|---------------------|---------------|
| 23 - Estatísticas e Dados Públicos | 6 | 20 - Políticas Públicas e Governança | Dados públicos são parte de governança/transparência |
| 22 - Eventos Oficiais e Cerimônias | 33 | Distribuir entre temas relacionados | Eventos são transversais a todos os temas |

### Candidatos a Subdivisão (volume muito alto)

| Tema | Notícias | Sugestão | Justificativa |
|------|----------|----------|---------------|
| 05 - Meio Ambiente e Sustentabilidade | 2.101 | Separar "Sustentabilidade" | 15.5% é muito concentrado |

### Candidatos a Revisão de Subtemas

| Tema | Motivo |
|------|--------|
| 19 - Defesa e Forças Armadas | Só 38 notícias - subtemas podem estar muito específicos |
| 09 - Esportes e Lazer | 155 notícias - verificar se subtemas fazem sentido |

---

## 8. Próximas Ações

1. [ ] Coletar distribuição L2 do Typesense
2. [ ] Coletar distribuição L3 do Typesense
3. [ ] Identificar temas L2/L3 com zero notícias
4. [ ] Validar recomendações de fusão/subdivisão
5. [ ] Documentar decisões em DECISOES_ESTRUTURAIS.md
