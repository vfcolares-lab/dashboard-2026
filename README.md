# 🎯 RADAR ELEITORAL AMAZONAS 2026
## Dashboard de Inteligência Estratégica para Campanha Senatorial

**Projeto confidencial** — Análise eleitoral histórica (2010-2022) de 62 municípios amazonenses com modelo preditivo para 2026.

---

## 📋 Arquivos

```
dashboard-2026/
├── index.html          ← 🎯 ABRIR NO NAVEGADOR
├── data.js             ← Dados processados (103 KB)
├── data.json           ← Backup em JSON
├── pipeline.py         ← Script para reprocessar dados
└── README.md           ← Este arquivo
```

---

## 🚀 Como Usar

### Opção 1: Abrir direto no navegador
```bash
# Mac/Linux
open /Users/vitorcolares/Desktop/relatorios\ tse/dashboard-2026/index.html

# Windows
start "C:\Users\...\dashboard-2026\index.html"
```

### Opção 2: Usar um servidor local (recomendado)
```bash
cd /Users/vitorcolares/Desktop/relatorios\ tse/dashboard-2026

# Python 3
python3 -m http.server 8000
# Depois abrir: http://localhost:8000
```

---

## 📊 Seções do Dashboard

| Seção | Descrição | Dados |
|-------|-----------|-------|
| **📊 Overview** | Distribuição por classificação, mapa coroplético, scatter (IN × IEB) | 88 municípios |
| **📈 Histórico** | Evolução EB e Presidente 2010-2022 por município | 4 eleições |
| **🏛️ Classificação** | Tabela completa com Índice Nacional, IEB, Eixo E1-E6 | 88 municípios |
| **🎯 Preditivo** | Modelo 2026 com cenários, gráficos de distribuição | Score + tendência |
| **📍 Impulsionamento** | Mapa de seções eleitorais para Meta Ads (em desenvolvimento) | Geolocalização |
| **📋 Dados Brutos** | Tabela master com busca, filtro, export | 88 municípios |

---

## 🔍 Indicadores-Chave

### Classificação Nacional (Índice de -1 a +1)
- **E1**: Lulismo Interior (51 municípios) — PT forte
- **E2**: Lulismo Manaus — PT forte em zona urbana
- **E3**: Amazonas Interior — Região ambígua
- **E4**: Amazonas Manaus — Região ambígua em zona urbana
- **E5**: Bolsonarismo Interior (36 municípios) — Direita forte
- **E6**: Bolsonarismo Manaus (1 município) — Direita forte em zona urbana

### Classificação Eduardo Braga (Índice de -1 a +1)
- **Bastião Eduardista** (51 municípios): IEB > 0.15
- **Tendência Eduardista**: 0.05 < IEB ≤ 0.15
- **Swing**: -0.05 ≤ IEB ≤ 0.05
- **Tendência Anti-EB**: -0.15 ≤ IEB < -0.05
- **Bastião Anti-EB** (10 municípios): IEB < -0.15

### Prognóstico 2026
- **SEGURO EB** (41): Score > 0.55
- **COMPETITIVO PRÓ-EB** (4): 0.45-0.55
- **BATTLEGROUND** (6): 0.40-0.45 ← **MÁXIMA PRIORIDADE**
- **COMPETITIVO CONTRA** (1): 0.35-0.40
- **DIFÍCIL** (10): < 0.35

---

## 🔧 Reprocessar Dados (Atualizar com novos dados TSE)

Se houver novos dados eleitorais:

```bash
cd /Users/vitorcolares/Desktop/relatorios\ tse/dashboard-2026

# Rodar o pipeline
python3 pipeline.py

# Atualiza data.js automaticamente
```

### Requisitos Python:
```bash
pip install pandas scipy numpy
```

---

## 📈 Metodologia de Cálculo

### Índice Nacional (IN)
```
margem_ano = (votos_PT / votos_válidos) - (votos_direita / votos_válidos)

IN = (margem_2010 × 0.10) + 
     (margem_2014 × 0.15) + 
     (margem_2018 × 0.30) + 
     (margem_2022 × 0.45)
```

Pesos maiores para eleições recentes (2022 tem 45%).

### Índice Eduardo Braga (IEB)
```
performance_eb = (votos_EB_município / votos_válidos) - 
                 (votos_EB_estado / votos_válidos)

IEB = (perf_2010 × 0.10) + 
      (perf_2014 × 0.15) + 
      (perf_2018 × 0.30) + 
      (perf_2022 × 0.45)
```

Mede se EB **supera** a média estadual no município.

### Modelo Preditivo 2026
```
Score = (tendência × 0.40) + 
        (correlação_lula_eb × 0.25) + 
        (última_eleição × 0.35)

tendência = regressão linear dos 4 ciclos
correlação_lula_eb = se Lula vai bem, EB vai bem?
última_eleição = desempenho em 2022
```

---

## 🎯 Candidatos Rastreados

### Presidência
| Ano | PT | Direita |
|-----|----|----|
| 2010 | Dilma Rousseff | José Serra |
| 2014 | Dilma Rousseff | Aécio Neves |
| 2018 | Fernando Haddad | Jair Bolsonaro |
| 2022 | Lula | Jair Bolsonaro |

### Eduardo Braga
| Ano | Cargo | Resultado |
|-----|-------|-----------|
| 2010 | Senador (PMDB) | ✅ Eleito |
| 2014 | Governador (PMDB) | ✅ Eleito |
| 2018 | Senador (MDB) | ✅ Eleito |
| 2022 | Governador (MDB) | ❌ Perdeu 2º turno |

---

## 📁 Estrutura de Dados (data.js)

```javascript
const DASHBOARD_DATA = {
  metadata: {
    generated_at: "2026-04-27T...",
    version: "1.0",
    state: "Amazonas",
    total_municipalities: 88,
    elections: [2010, 2014, 2018, 2022]
  },
  municipios: {
    "MANAUS": {
      indice_nacional: 0.123,
      classificacao_nacional: "Tendência Lulista",
      indice_eb: 0.234,
      classificacao_eb: "Bastião Eduardista",
      eixo_estrategico: "E2",
      eixo_label: "Lulismo Manaus",
      presidente: {
        2010: { pt: 52.1, direita: 47.9, margem: 4.2 },
        ...
      },
      eb: {
        2010: { cargo: "Senado", votos_pct: 42.1, media_estado: 38.1, diff: 4.0 },
        ...
      },
      preditivo_2026: {
        score: 0.58,
        classificacao: "SEGURO EB",
        tendencia: "positiva",
        volatilidade: 0.12
      }
    },
    ...
  }
}
```

---

## ⚠️ CONFIDENCIALIDADE

Este dashboard contém **análise estratégica confidencial** da campanha de Eduardo Braga. 

**Restrições:**
- ✋ Não distribuir fora da equipe
- ✋ Não publicar em nenhum servidor público
- ✋ Não compartilhar links ou screenshots
- ✅ Funciona **offline** — todos os dados estão locais

---

## 🔗 Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Gráficos**: Chart.js 4, D3.js
- **Mapas**: Leaflet.js + CartoDB
- **Backend**: Python 3 (pandas, scipy, numpy)
- **Data**: CSV do TSE

---

## 📞 Suporte

Para atualizar dados ou adicionar novas análises, roda:
```bash
python3 pipeline.py
```

O dashboard usa `data.js` que é regenerado automaticamente.

---

**Última atualização:** 27 de Abril de 2026
**Versão:** 1.0
**Status:** ✅ Produção
