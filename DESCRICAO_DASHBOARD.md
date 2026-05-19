# 🎯 Dashboard Eleitoral Amazonas 2026

## O Que É?

Um **dashboard interativo** que mapeia e analisa o comportamento eleitoral de **todas as 4.468 seções de votação** do Amazonas, com foco na estratégia eleitoral para 2026. É uma ferramenta de **inteligência política** que identifica onde focar esforços de campanha com precisão geográfica.

---

## Para Quem Serve?

- **Campanha eleitoral** - Estratégia de impulsionamento por região
- **Análise política** - Entender tendências e volatilidade eleitoral
- **Gestão de recursos** - Alocar esforços onde têm maior impacto
- **Monitoramento** - Acompanhar mudanças no eleitorado em tempo real

---

## Como Funciona?

### 📊 **Dados Base (2022)**

O dashboard analisa **3 dimensões eleitorais** de cada seção:

1. **Presidencial 2022**
   - Votos: Lula (PT) vs Bolsonaro (Direita)
   - Margem e percentuais
   - Comparação com média estadual

2. **Governador 2022**
   - Votos: Eduardo Braga (EB) vs Wilson Miranda Lima
   - Desempenho local vs estadual
   - Base eleitoral de cada candidato

3. **Histórico 2018**
   - Volatilidade eleitoral (mudanças de voto 2018→2022)
   - Tendências de movimento de eleitores
   - Seções estáveis vs seções voláteis

### 🔍 **Análise por Seção**

Cada seção é analisada por **3 índices principais**:

#### **Índice Nacional (indice_nacional)**
```
Como a seção se comporta versus a média estadual para PT/Bolsonaro
- Positivo (+0.10) = PT muito acima da média estadual
- Negativo (-0.10) = Bolsonaro muito acima da média estadual
- Neutro (0.00) = Comportamento igual ao estado
```

#### **Índice Eduardo Braga (indice_eb)**
```
Como a seção se comporta versus a média estadual para EB
- Positivo (+0.10) = EB muito acima da média estadual (bastião)
- Negativo (-0.10) = EB muito abaixo da média estadual (difícil)
- Neutro (0.00) = Comportamento igual ao estado
```

#### **Volatilidade (volatilidade)**
```
Quanto a seção mudou de 2018 para 2022
- 0.00 = Votação igual em 2018 e 2022 (seção estável)
- 0.30 = Votação mudou muito entre eleições (seção volátil)
```

### 🎨 **Categorização Automática**

Cada seção é classificada em **5 categorias** baseadas nos índices:

| Categoria | Cor | Significado | Estratégia |
|-----------|-----|-------------|-----------|
| **LULA+EB** | 🟢 Verde | PT forte + EB acima da média | Consolidar. Reforçar marca de EB |
| **EB_PURO** | 🟣 Roxo | EB forte mesmo com Bolsonaro na frente | Valorizar EB independente. Transferência de voto |
| **BOLSO+EB** | 🟠 Laranja | Bolsonaro na frente MAS EB tem votos | Focar em EB. Diferenciar de Bolsonaro |
| **PURO_SWING** | 🟡 Amarelo | Muito volátil ou equilibrado | Máxima prioridade. Tudo funciona |
| **DIFÍCIL** | 🔴 Vermelho | EB muito abaixo da média estadual | Investimento alto. Conquistar novo eleitor |

---

## 🗺️ **Componentes do Dashboard**

### **1. Mapa Interativo**
- Visualizar **4.468 pontos** (seções) no mapa do Amazonas
- Cada ponto colorido = categoria
- **Filtrar por município** - Zoom automático e lista de seções
- **Hover nas seções** - Ver número, endereço, categoria
- **Coordenadas geográficas** - Cada seção tem lat/long com offset aleatório

### **2. Tab "Radar Eleitoral"**
- **Índice Nacional** - Qual é o desempenho de PT vs Bolsonaro por município
- **Índice EB** - Qual é o desempenho de Eduardo Braga por município
- **Ranking** - Municípios ordenados por desempenho em cada dimensão
- **Análise** - Explicação detalhada de cada métrica

### **3. Tab "Impulsionamento"**
- **Seletor de município** - Escolher qual município analisar
- **Mapa com seções** - Ver todas as seções do município
- **Cores e categorias** - Identificar onde estão as dificuldades/oportunidades
- **CSV download** - Exportar dados para planilha (Excel, Google Sheets)
  - Pode ser tudo ou filtrado por município

### **4. Tab "Dados Brutos"**
- **Tabela interativa** - Ver todas as 4.468 seções
- **Busca por município** - Filtrar rapidinho
- **Colunas completas** - Números brutos, votos, índices, projeções
- **Ordenação** - Clicando no header das colunas

### **5. Documentação**
- **Como usar** - Passo a passo
- **Definições** - O que significa cada métrica
- **Metodologia** - Como os índices são calculados
- **FAQ** - Respostas rápidas

---

## 📈 **Dados Exportáveis**

Você pode **baixar os dados em 3 formatos**:

### **CSV** (para Excel/Planilhas)
```
numero_secao,municipio,categoria,latitude,longitude,votos_pt_2022,votos_bolsonaro_2022,...
1,ALVARÃES,LULA+EB,-3.6759,-64.7089,471,122,...
2,ALVARÃES,DIFÍCIL,-3.6634,-64.6520,468,121,...
```

### **XML** (para APIs/Integrações)
```xml
<dashboard>
  <secoes>
    <municipio nome="ALVARÃES">
      <secao>
        <numero>1</numero>
        <categoria>LULA+EB</categoria>
        <votos_2022>
          <pt>471</pt>
          <bolsonaro>122</bolsonaro>
          <eb>178</eb>
        </votos_2022>
      </secao>
    </municipio>
  </secoes>
</dashboard>
```

### **JSON** (para aplicações web)
```json
{
  "ALVARÃES": [
    {
      "numero_secao": 1,
      "categoria": "LULA+EB",
      "votos_2022": {"pt": 471, "bolsonaro": 122, "eb": 178},
      "latitude": -3.6759,
      "longitude": -64.7089
    }
  ]
}
```

---

## 🎯 **Casos de Uso**

### **1. Identificar Frentes de Trabalho**
```
Gerente de Campanha abre o mapa, filtro por BOLSO+EB
↓
Vê exatamente quais são as seções com Bolsonaro na frente 
mas EB tem votos
↓
Foca em diferenciação de EB (não é Bolsonaro)
↓
Resultado: mais eficiência
```

### **2. Alocar Recursos**
```
Tem 10 militantes? 
- 5 para PURO_SWING (tudo funciona lá)
- 3 para DIFÍCIL (conquistar novo eleitor)
- 2 para EB_PURO (consolidar)
↓
Distribuição estratégica baseada em dados
```

### **3. Monitorar Volatilidade**
```
Detecta seções com volatilidade > 30%
↓
Sabe que são seções que podem mudar de lado
↓
Aumenta monitoramento dessas seções
```

### **4. Projetar 2026**
```
Com base em 2022 + volatilidade histórica
↓
Dashboard projeta PT%, Bolsonaro%, EB% para 2026
↓
Pode antecipar cenários e se preparar
```

---

## 📊 **Estatísticas Globais**

| Métrica | Valor |
|---------|-------|
| **Total de Seções** | 4.468 |
| **Municípios** | 62 |
| **LULA+EB** | 2.312 (51.7%) |
| **DIFÍCIL** | 1.239 (27.7%) |
| **PURO_SWING** | 532 (11.9%) |
| **BOLSO+EB** | 261 (5.8%) |
| **EB_PURO** | 124 (2.8%) |

**Estado Total 2022:**
- PT (Lula): 50.32%
- Bolsonaro: 45.78%
- EB (Eduardo Braga): 31.93%

---

## 🔧 **Funcionalidades Técnicas**

- ✅ **Mapa interativo** com Leaflet (OpenStreetMap)
- ✅ **Zoom automático** por município selecionado
- ✅ **Tooltips** ao passar o mouse nas seções
- ✅ **Download CSV/XML** com dados completos
- ✅ **Busca e filtro** em tempo real
- ✅ **Responsivo** - funciona em desktop e mobile
- ✅ **Online** - Vercel (sem depender de computador local)
- ✅ **Dados atualizados** - Último cálculo 27 de abril de 2026

---

## 🚀 **Como Usar?**

1. **Abra o dashboard online** (URL do Vercel)
2. **Explore o Mapa** - Veja distribuição de categorias
3. **Filtro por Município** - Zoom na região que te interessa
4. **Analise os Índices** - Entenda tendências
5. **Baixe CSV/XML** - Leve dados para planilha/API
6. **Leia a Documentação** - Entenda cada métrica

---

## 📁 **Arquivos Disponíveis**

| Arquivo | Formato | Uso |
|---------|---------|-----|
| `index.html` | HTML/JavaScript | Dashboard ao vivo |
| `TODAS_SECOES_MAPEADAS.csv` | CSV | Excel/Planilhas |
| `TODAS_SECOES_MAPEADAS.xml` | XML | APIs/Integrações |
| `secoes_2022.json` | JSON | Aplicações web |
| `secoes_2022.js` | JavaScript | Embed em websites |

---

## ⚡ **Tecnologias**

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Mapa**: Leaflet + OpenStreetMap
- **Dados**: JSON + CSV + XML
- **Deploy**: Vercel
- **Versionamento**: Git + GitHub
- **Análise**: Python (Pandas)

---

## 📞 **Suporte & Recuperação**

Se precisar voltar para essa versão estável (v1.0):
```bash
git checkout v1.0-stable
```

Ver arquivo: `VERSAO_ATUAL.md` para mais detalhes.

---

## 🎓 **Próximos Passos Possíveis**

- Integrar dados de 2020, 2016, 2014, 2010
- Adicionar dados demográficos (idade, renda, educação)
- Análise de redes (influência entre seções)
- Simulações de cenários
- App mobile nativo
- Integração com WhatsApp/Telegram
- Dashboard de campanha em tempo real

---

**Versão:** v1.0-stable  
**Data:** 27 de abril de 2026  
**Status:** ✅ Produção  
**Criado por:** Claude + Vitor Colares

---

## 📝 **Licença & Dados**

- Dados base: TSE (Tribunal Superior Eleitoral)
- Dashboard: Propriedade privada
- Uso: Estratégia eleitoral interna
- Acesso: Restrito à equipe
