# 🎯 VERSÃO ATUAL DO DASHBOARD - REFERÊNCIA

## Informações da Versão Estável

**Versão:** `v1.0-stable`  
**Data:** 27 de abril de 2026  
**Commit:** `f153456b91ba19efb8fb29d4a0ec4375aec2cb46` (curto: `f153456`)  
**Repositório:** https://github.com/vfcolares-lab/dashboard-2026.git

---

## 📊 O que está nessa versão

- ✅ **4.468 seções eleitorais** mapeadas em 62 municípios do Amazonas
- ✅ **5 categorias de classificação:**
  - LULA+EB: 2.312 seções (51.7%)
  - DIFÍCIL: 1.239 seções (27.7%)
  - PURO_SWING: 532 seções (11.9%)
  - BOLSO+EB: 261 seções (5.8%)
  - EB_PURO: 124 seções (2.8%)

- ✅ **Mapa interativo** com Leaflet
- ✅ **Coordenadas geográficas** com offset aleatório
- ✅ **Índices de desempenho:**
  - Índice Nacional (comparação com média estadual de PT)
  - Índice EB (comparação com média estadual de Eduardo Braga)
  - Volatilidade 2018→2022
  
- ✅ **Dados base 2022:**
  - Presidencial: PT (Lula) vs Bolsonaro
  - Governador: Eduardo Braga vs Wilson Miranda Lima
  - Histórico 2018 para cálculo de volatilidade

- ✅ **Projeções 2026** para cada seção

---

## 🔄 COMO VOLTAR PARA ESSA VERSÃO NO FUTURO

Se você fizer mudanças e quiser voltar exatamente para esse ponto:

### Opção 1: Checkout (recomendado - seguro)
```bash
cd "/Users/vitorcolares/Desktop/relatorios tse/dashboard-2026"
git checkout f153456b91ba19efb8fb29d4a0ec4375aec2cb46
```

### Opção 2: Usar a tag
```bash
git checkout v1.0-stable
```

### Opção 3: Reset hard (descarta TODAS as mudanças)
```bash
git reset --hard f153456b91ba19efb8fb29d4a0ec4375aec2cb46
```

---

## 📁 Arquivos importantes nessa versão

- `secoes_2022.json` - Dados de todas as 4.468 seções
- `secoes_2022.js` - Mesmo arquivo em formato JavaScript
- `index.html` - Dashboard completo
- `recalculate_sections.py` - Script de recalculação
- `add_coordinates.py` - Script de geração de coordenadas

---

## 🚀 Vercel Deployment

Essa versão está online em:  
https://dashboard-2026-vfcolares-lab.vercel.app (ou seu URL específico)

---

## ✅ Verificação

Para confirmar que está na versão correta, execute:
```bash
git log -1 --oneline
# Deve mostrar: f153456 Add geographic coordinates to all 4,468 voting sections
```

---

**Data de criação dessa documentação:** 27 de abril de 2026  
**Criado por:** Claude + Vitor  
**Status:** ✅ Produção (Online)
