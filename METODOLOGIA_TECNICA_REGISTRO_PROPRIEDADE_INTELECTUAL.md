# DOCUMENTAÇÃO DA METODOLOGIA TÉCNICA E OPERACIONAL

**Nome do Produto:** Radar Eleitoral — Sistema de Análise e Impulsionamento por Microtargeting Hiperlocal Georreferenciado

**Versão:** 1.0

**Data de Criação:** 27 de abril de 2026

**Órgão Depositante:** Vitor Fernandes Colares

**Instituição Responsável:** Vfcolares-Lab

---

## 1. INTRODUÇÃO E VISÃO GERAL

### 1.1 Apresentação do Produto

O **Radar Eleitoral** é um sistema computacional inovador de análise eleitoral que processa dados de votação histórica, comportamento eleitoral recente e indicadores preditivos para realizar microtargeting hiperlocal com base em geolocalização de seções eleitorais. O sistema foi desenvolvido inicialmente para o estado do Amazonas, mas possui arquitetura escalável para qualquer território administrativo (estados, municípios, regiões, ou cobertura nacional).

O produto consolida 4.468 seções eleitorais em 62 municípios amazonenses, cada uma analisada como uma unidade de microtargeting independente, gerando um entendimento granular do comportamento eleitoral que transcende os limites tradicionais de análises municipais ou regionais.

### 1.2 Problema de Mercado e Gargalo Operacional Resolvido

A indústria de campanhas eleitorais contemporânea enfrenta um gargalo crítico: as pesquisas eleitorais convencionais, embora rigorosas estatisticamente, operam com agregação de dados em níveis municipais ou recortes demográficos amplos (idade, gênero, renda, educação). Esta agregação, necessária para significância estatística amostral, remove a granularidade necessária para decisões de alocação de recursos em campanhas digitais modernas.

As campanhas contemporâneas enfrentam três desafios operacionais específicos:

1. **Desperdício de Recursos em Segmentação Genérica**: Campanhas gastam orçamento substancial impulsionando conteúdos genéricos por municípios ou regiões, sem compreender que dentro de uma mesma cidade existem microterritórios com comportamentos eleitorais radicalmente distintos.

2. **Cegueira Sobre Volatilidade Hiperlocal**: Pesquisas não detectam que determinados blocos ou setores de votação dentro de um município podem apresentar volatilidade eleitoral significativa (mudanças de 15-30 pontos percentuais entre eleições), enquanto outros permanecem estáveis.

3. **Ausência de Orientação Preditiva para Micromobilização**: Não existem metodologias que combinem comportamento histórico, análise preditiva e geolocalização para gerar orientações específicas de conteúdo e estratégia de mobilização por seção eleitoral.

### 1.3 Solução Proposta e Diferencial Competitivo

O Radar Eleitoral não compete com pesquisas eleitorais convencionais; complementa-as. Funciona como uma **lupa hiperlocal** que:

- **Desagrega** dados de votação histórica (2010-2022) até o nível de seção eleitoral
- **Classifica** cada seção em categorias ideológicas e eleitorais baseadas em comportamento factual
- **Projeta** cenários para 2026 utilizando volatilidade histórica e indicadores de tendência
- **Geolocaliza** cada seção com coordenadas e raios de influência demográfica
- **Gera orientações** de conteúdo e mobilização específicas por microtarget

A arquitetura realiza isto através de:

1. **Análise Tridimensional de Comportamento**:
   - Dimensão Presidencial: desempenho PT vs Direita em cada seção
   - Dimensão Regional: desempenho do candidato regional (Eduardo Braga/EB) em cada seção
   - Dimensão Temporal: volatilidade e mudanças de padrão de votação ao longo do tempo

2. **Indexação Comparativa**: cada seção é medida não em valores absolutos, mas em desvio comparativo à média estadual, permitindo identificar **bastiões** (seções acima da média) e **territórios difíceis** (seções abaixo da média).

3. **Classificação Automática**: aplicação de algoritmo de categorização que combina os três índices para produzir uma de cinco categorizações estratégicas.

4. **Integração Geoespacial**: cada ponto de votação possui coordenadas geográficas com raio de influência baseado em densidade populacional, permitindo visualização cartográfica e análise de clusters espaciais.

### 1.4 Objetivo Geral e Resultado Final

**Objetivo Geral**: Fornecer à operação de campanha um instrumento de decisão para alocação otimizada de recursos de impulsionamento digital e mobilização terrestre, baseado em análise factual de comportamento eleitoral hiperlocal e projeções preditivas.

**Resultado Final Entregue**: 

1. Dashboard interativo com visualização cartográfica de 4.468 seções eleitorais classificadas e categorizadas
2. Três formatos de exportação de dados (CSV, XML, JSON) contendo para cada seção:
   - Localização geográfica (latitude, longitude, raio de influência)
   - Classificação ideológico-eleitoral
   - Índices de desempenho (nacional, regional, volatilidade)
   - Dados históricos de votação (2022, 2018, 2010)
   - Projeções para 2026
3. Interface de filtro territorial (por município) com zoom automático e visualização de seções
4. Relatórios descritivos e análises comparativas entre seções
5. Metodologia documentada e reproduzível para replicação em outros estados/territórios

---

## 2. FUNDAMENTAÇÃO CONCEITUAL E LOGÍSTICA DO SISTEMA

### 2.1 Definição de Termos Técnicos e Métricas Centrais

#### **Seção Eleitoral**
Unidade de votação registrada oficialmente pelo Tribunal Superior Eleitoral (TSE). Cada seção possui número único (NR_SECAO), localização administrativa (município, zona, local de votação) e, no contexto deste sistema, coordenadas geográficas calculadas. Para fins deste sistema, cada seção é tratada como um **nó de decisão eleitoral** independente, sendo a unidade fundamental de análise.

#### **Índice Nacional (indice_nacional)**
Métrica que expressa o desvio de desempenho presidencial de uma seção em relação à média estadual, normalizado em escala de -1 a +1. Fórmula conceitual:

```
indice_nacional = (PT_pct_seção - PT_pct_estado) / 100
```

Interpretação:
- Valor +0.10 = seção com PT 10 pontos percentuais acima da média estadual
- Valor -0.10 = seção com PT 10 pontos percentuais abaixo da média estadual
- Valor 0.00 = seção com PT exatamente na média estadual

**Significado Eleitoral**: Identifica seções que são **bastiões** (valores positivos altos) do voto progressista/petista ou **territórios hostis** (valores negativos altos) à candidatura de PT.

#### **Índice Eduardo Braga / Índice Regional (indice_eb)**
Métrica que expressa o desvio de desempenho do candidato regional (governador/senador) em relação à média estadual. Fórmula conceitual:

```
indice_eb = (EB_pct_seção - EB_pct_estado) / 100
```

**Significado Eleitoral**: Identifica seções que são **bastião regional** (valores positivos) do candidato ou **territórios de resistência** (valores negativos) ao candidato regional.

#### **Volatilidade Eleitoral (volatilidade)**
Métrica que expressa a magnitude da mudança de comportamento eleitoral de uma seção entre dois ciclos eleitorais (2018 e 2022). Fórmula conceitual:

```
volatilidade = |PT_pct_2022 - PT_pct_2018| / 100
```

Interpretação:
- Valor 0.00 = seção votou percentualmente igual em 2018 e 2022 (votação estável)
- Valor 0.15 = seção mudou 15 pontos percentuais entre eleições (volatilidade média)
- Valor 0.30+ = seção mudou 30+ pontos percentuais (volatilidade extrema)

**Significado Eleitoral**: Identifica seções que são **swing voters em escala geográfica**, sinalizando potencial para mudança de voto entre ciclos eleitorais.

#### **Raio de Influência (raio_km)**
Parâmetro geoespacial que define a área de abrangência teórica de cada seção eleitoral, baseado em densidade populacional do município:
- Manaus (área urbana densa): 3 km de raio
- Interior (área urbana média): 6 km de raio
- Rural (área de baixa densidade): 15 km de raio

Este parâmetro é utilizado tanto para visualização cartográfica quanto para análises de clustering espacial.

#### **Categoria Eleitoral**
Classificação estratégica de uma seção em uma de cinco categorias mutuamente exclusivas, derivada da combinação dos três índices (nacional, regional, volatilidade). Ver seção 2.3 para detalhamento das categorias.

### 2.2 Pilares Lógicos Fundamentais do Sistema

O Radar Eleitoral repousa sobre quatro pilares lógicos independentes:

#### **Pilar 1: Disagregação Factual de Dados**
O sistema assume que dados de votação agregados no nível municipal ocultam variações significativas e que a unidade de seção eleitoral representa a menor granularidade em que comportamento eleitoral pode ser analisado com integridade.

Premiса: Dentro de um mesmo município, existem seções com padrões eleitorais fundamentalmente distintos.

#### **Pilar 2: Análise Comparativa Normalizada**
Não analisa valores absolutos de votação, mas desvios em relação a um padrão estadual. Isto permite identificação de **excepcionalidades** (seções que votam diferente da norma estadual) em vez de medir apenas magnitude de voto.

Premissa: Uma seção com 50% de votos em PT é menos informativa que saber se esta seção está 10 pontos acima ou abaixo da média estadual de PT.

#### **Pilar 3: Incorporação de Dimensionalidade Temporal**
Analisa não apenas um ciclo eleitoral, mas múltiplos ciclos (2010, 2014, 2018, 2022) para capturar padrões de mudança (volatilidade) e tendências de movimento.

Premissa: Uma seção que mudou drasticamente entre 2018 e 2022 é qualitativamente diferente de uma seção que manteve padrão estável.

#### **Pilar 4: Fundação Geoespacial**
Vincula cada ponto de dados a coordenadas geográficas e raios de influência, permitindo análise espacial e identificação de clusters ideológicos com base em proximidade geográfica.

Premissa: Seções geograficamente próximas podem ter comportamentos eleitorais correlacionados, permitindo estratégias de mobilização territorialmente coerentes.

### 2.3 Diferencial Técnico em Relação a Soluções Genéricas

A abordagem do Radar Eleitoral diferencia-se de soluções de análise eleitoral genéricas em sete dimensões:

1. **Granularidade**: Análise de 4.468 unidades (seções) vs. típicas 62 unidades (municípios) ou 5-10 unidades (regiões)

2. **Metodologia de Indexação**: Uso de desvio normalizado em relação à média estadual, vs. análise de magnitude absoluta

3. **Integração Multidimensional**: Combinação simultânea de três dimensões de análise (presidencial, regional, temporal), vs. análises unidimensionais

4. **Incorporação de Volatilidade**: Incluí cálculo explícito de mudança de padrão eleitoral ao longo do tempo, vs. análise estática de um único ciclo

5. **Classificação Automática**: Algoritmo que converte índices numéricos em categorias estratégicas, permitindo segmentação automática de territórios

6. **Integração Geoespacial**: Cada ponto vinculado a coordenadas geográficas e raios de influência, permitindo análise cartográfica interativa

7. **Formato de Saída Estruturado**: Exportação de dados em múltiplos formatos (CSV, XML, JSON) com estrutura documentada, permitindo integração com sistemas terceiros e análises adicionais

### 2.4 Premissas Metodológicas Explícitas

O sistema opera sob as seguintes premissas, que delimitam seu escopo e aplicabilidade:

1. **Dados TSE como Ground Truth**: Assume-se que dados do Tribunal Superior Eleitoral representam fonte factual de votação, sem necessidade de validação adicional

2. **Comportamento Histórico como Preditor**: Assume-se que padrões de votação histórica (2010-2022) possuem poder preditivo razoável para comportamento futuro (2026)

3. **Estabilidade Relativa de Eleitores**: Assume-se que mudanças de padrão eleitoral entre ciclos ocorrem de forma correlacionada com fatores políticos/econômicos, não aleatoriamente

4. **Homogeneidade Intra-Seção**: Assume-se que todos os votantes de uma seção compartilham contexto geográfico, social e econômico relativamente homogêneo

5. **Significância Estatística Aceitável**: Seções menores (< 100 votantes) são incluídas na análise com a ressalva de que desempenho individual percentual possui maior variância

© 2026. Todos os direitos reservados. Obra intelectual protegida nos termos da Lei nº 9.610/98.

---

## 3. ARQUITETURA DE DADOS E VARIÁVEIS

### 3.1 Fontes de Dados Consumidas pelo Sistema

O Radar Eleitoral integra dados de múltiplas fontes, todas de origem pública e oficialmente disponibilizadas:

#### **Fonte 1: Tribunal Superior Eleitoral (TSE) — Dados de Votação**

**Arquivos Consumidos:**
- `votacao_secao_2022_BR.csv` — Votação presidencial 2022 por seção (Brasil)
- `votacao_secao_2022_AM.csv` — Votação para governador 2022 por seção (Amazonas)
- `votacao_secao_2018_AM.csv` — Votação presidencial 2018 por seção (Amazonas)
- `votacao_secao_2014_AM.csv` — Votação estadual 2014 por seção (Amazonas)
- `votacao_secao_2010_AM.csv` — Votação estadual 2010 por seção (Amazonas)

**Estrutura de Dados Consumida:**
Cada arquivo possui campos:
- `NR_SECAO` — Número identificador único da seção
- `NM_MUNICIPIO` — Nome do município
- `NM_VOTAVEL` — Nome do candidato/opção de voto
- `QT_VOTOS` — Quantidade de votos recebidos
- `DS_CARGO` — Descrição do cargo (Presidente, Governador, etc.)
- `DS_LOCAL_VOTACAO_ENDERECO` — Endereço do local de votação

**Formato Técnico:** Arquivos CSV com delimitador ponto-e-vírgula (`;`), encoding Latin-1, com registros agregados por candidato-seção-cargo.

#### **Fonte 2: Pesquisas Eleitorais (quando disponíveis)**

O sistema possui capacidade de ingestão de dados de pesquisas eleitorais municipais ou regionais com suficiente representatividade amostral. Estes dados são utilizados para calibração e validação de projeções, quando disponíveis.

**Critério de Aceitação:** Pesquisa deve possuir margem de erro ≤ 5 pontos percentuais e cobertura de pelo menos 3 municípios para validação regional.

#### **Fonte 3: Base de Coordenadas Geográficas (Gazetteer)**

Coordenadas latitude/longitude de centros urbanos de cada município, obtidas de base de dados geoespacial padrão (OpenStreetMap/Wikidata).

**Formato:** Pares de coordenadas em WGS-84 (EPSG:4326).

### 3.2 Critérios de Seleção e Validação de Dados

#### **Filtros de Seleção Primária**

1. **Filtro Geográfico**: Seleção de registros com `SG_UF = 'AM'` (estado Amazonas), resultando em 62 municípios oficiais

2. **Filtro de Elegibilidade Municipal**: Apenas municípios presentes em lista oficial de 62 municípios amazonenses são processados; registros de outros municípios são descartados

3. **Filtro de Cargo**: 
   - Para análise presidencial: `DS_CARGO` contém "Presidente"
   - Para análise regional: `DS_CARGO` contém "Governador"
   - Outros cargos (deputados, senadores) são descartados nesta versão

4. **Filtro de Candidato**:
   - Presidencial: Candidatos que contenham "LULA" ou "BOLSONARO" (case-insensitive)
   - Regional: Candidato "CARLOS EDUARDO DE SOUZA BRAGA" (Eduardo Braga/EB)
   - Votos inválidos: Registros com "NULO" ou "BRANCO" são separados e utilizam para cálculo de total válido

#### **Validações de Qualidade**

1. **Validação de Consistência Numérica**: 
   - Verifica-se que `QT_VOTOS` é sempre inteiro positivo
   - Verifica-se que soma de votos por seção é coerente (nem zero, nem impossívelmente grande)

2. **Validação de Completude**:
   - Cada seção deve possuir registros para todos os candidatos principais
   - Se uma seção não possuir registro de candidato esperado, assume-se 0 votos

3. **Validação de Normalização de Nomes**:
   - Nomes de municípios são convertidos para MAIÚSCULAS e trimmed (espaços removidos)
   - Nomes de candidatos são trimmed
   - Acentuação é normalizada para permitir matching mesmo com variações

4. **Validação de Cobertura Temporal**:
   - Sistema requer dados de 2022 e 2018 como mínimo
   - Se dados de ciclos anteriores (2010, 2014) não estão disponíveis, seção é processada mas volatilidade não pode ser calculada para estes ciclos

### 3.3 Mapeamento de Variáveis Principais e Significado no Negócio

#### **Variáveis de Entrada (Input)**

| Variável | Origem | Tipo | Significado Operacional |
|----------|--------|------|--------------------------|
| `numero_secao` | TSE | Integer | Identificador único de cada ponto de votação; chave primária da análise |
| `municipio` | TSE | String | Localização administrativa; base para clustering e análise regional |
| `endereco` | TSE | String | Localização física; utilizado em relatórios e referência geográfica |
| `votos_pt_2022` | TSE | Integer | Votos recebidos por PT em cada seção; entrada bruta para cálculo de percentuais |
| `votos_bolsonaro_2022` | TSE | Integer | Votos recebidos por Bolsonaro em cada seção; entrada bruta para cálculo de percentuais |
| `votos_eb_2022` | TSE | Integer | Votos recebidos por Eduardo Braga em cada seção; base para análise regional |
| `votos_total_2022` | TSE (calculado) | Integer | Soma de votos válidos em cada seção; denominador para cálculos percentuais |
| `pt_pct_2022` | Sistema (calculado) | Float | Percentual de PT em cada seção (PT/Total * 100); entrada para indexação |
| `bolsonaro_pct_2022` | Sistema (calculado) | Float | Percentual de Bolsonaro em cada seção; entrada para indexação |
| `eb_pct_2022` | Sistema (calculado) | Float | Percentual de EB em cada seção; entrada para indexação regional |
| `pt_pct_2018` | TSE (2018) | Float | Percentual histórico de PT; utilizado para cálculo de volatilidade |

#### **Variáveis de Processamento Intermediário**

| Variável | Origem | Tipo | Significado Operacional |
|----------|--------|------|--------------------------|
| `pt_pct_estado` | Sistema (agregado) | Float | Média estadual de votos em PT; utilizada como benchmark para comparação |
| `eb_pct_estado` | Sistema (agregado) | Float | Média estadual de votos em EB; utilizada como benchmark para comparação |
| `bolsonaro_pct_estado` | Sistema (agregado) | Float | Média estadual de votos em Bolsonaro; utilizada para contexto |
| `indice_nacional_bruto` | Sistema | Float | Desvio bruto de PT em relação à média estadual; entrada para normalização |
| `indice_eb_bruto` | Sistema | Float | Desvio bruto de EB em relação à média estadual; entrada para normalização |
| `volatilidade_bruta` | Sistema | Float | Mudança absoluta de PT entre 2018 e 2022; entrada para classificação |

#### **Variáveis de Saída (Output)**

| Variável | Tipo | Significado Operacional | Uso em Negócio |
|----------|------|--------------------------|-----------------|
| `categoria` | String | Uma de 5 classes (LULA+EB, DIFÍCIL, PURO_SWING, BOLSO+EB, EB_PURO) | Segmentação estratégica para alocação de recursos |
| `cor` | String | Código hexadecimal (#27AE60, #E74C3C, etc.) | Visualização cartográfica e legendas |
| `indice_nacional` | Float | Desvio normalizado em relação a benchmark nacional | Análise de viés presidencial; comunicação de força |
| `indice_eb` | Float | Desvio normalizado em relação a benchmark regional | Análise de viés regional; identificação de bastiões |
| `volatilidade` | Float | Magnitude de mudança eleitoral | Identificação de swing territories; priorização |
| `preditivo_2026_pt_projecao` | Float | Percentual projetado de PT para 2026 | Planejamento de cenários; estimativa de força |
| `preditivo_2026_eb_projecao` | Float | Percentual projetado de EB para 2026 | Planejamento de cenários; estimativa de força regional |
| `latitude` | Float | Coordenada geográfica (WGS-84) | Plotagem em mapa; análise espacial |
| `longitude` | Float | Coordenada geográfica (WGS-84) | Plotagem em mapa; análise espacial |
| `raio_km` | Integer | Raio de influência em quilômetros | Definição de área de abrangência territorial |

© 2026. Todos os direitos reservados. Obra intelectual protegida nos termos da Lei nº 9.610/98.

---

## 4. O MÉTODO DE PROCESSAMENTO (A FÓRMULA DO NEGÓCIO)

### 4.1 Etapa 1: Captura e Ingestão de Dados

#### **4.1.1 Processo de Leitura de Arquivos Fonte**

O sistema inicia o ciclo de processamento através de leitura de arquivos CSV fornecidos pelo TSE. Cada arquivo é lido com seguintes parâmetros:

```
Delimitador: ponto-e-vírgula (;)
Encoding: Latin-1
Low Memory: True (processamento em chunks para otimização de memória)
```

**Fluxo Específico:**

1. **Arquivo 2022 Presidencial** (`votacao_secao_2022_BR.csv`)
   - Lido na íntegra (83.232 registros para Amazonas)
   - Filtrado para `SG_UF == 'AM'`
   - Mantido em memória como `df_pres_2022`

2. **Arquivo 2022 Governador** (`votacao_secao_2022_AM.csv`)
   - Lido na íntegra (89.697 registros)
   - Filtrado para `DS_CARGO == 'GOVERNADOR'`
   - Mantido em memória como `df_gov_2022`

3. **Arquivo 2018 Presidencial** (`presidente_2018_AM_por_secao.csv`)
   - Lido na íntegra (101.348 registros)
   - Filtrado para `DS_CARGO` contém "Presidente"
   - Mantido em memória como `df_pres_2018`

#### **4.1.2 Normalização de Campos Durante Ingestão**

Ao momento da leitura, os seguintes tratamentos são aplicados:

```python
df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
```

Isto assegura que variações de casing, acentuação e espaçamento não causem problemas em matching subsequente.

#### **4.1.3 Validação de Ingestão**

Ao término da ingestão, o sistema verifica:
- Quantidade de registros lidos é > 0
- Ao menos um candidato esperado foi encontrado
- Campos críticos (`NR_SECAO`, `NM_MUNICIPIO`, `QT_VOTOS`) não contêm valores nulos

Se validações falham, processo interrompe com mensagem de erro específica.

### 4.2 Etapa 2: Tratamento, Normalização e Limpeza de Dados

#### **4.2.1 Limpeza de Inconsistências de Nomenclatura**

**Problema**: Nomes de municípios e candidatos podem conter variações (acentuação, maiúsculas/minúsculas, espaços extras).

**Solução**:
- Todas as strings de nome de município são convertidas para MAIÚSCULAS e trimmed
- Nomes de candidatos são trimmed
- Acentuação é normalizada utilizando Unicode NFD normalization

```
EXEMPLO: "são gabriel da cachoeira" → "SÃO GABRIEL DA CACHOEIRA"
EXEMPLO: "LULA " (com espaço) → "LULA"
```

#### **4.2.2 Validação de Completude de Seções**

**Problema**: Nem todas as seções possuem registros para todos os candidatos em todos os anos.

**Solução**: Para cada combinação (municipio, numero_secao, ano, cargo), verifica-se presença de registros esperados. Se um candidato esperado não possuir registro, assume-se 0 votos.

**Exemplo**:
- Seção 1 de MANAUS possui 5 registros em 2022 (PT, Bolsonaro, Ciro, Tebet, Simone): OK
- Seção 2 de ALVARÃES possui apenas 3 registros (PT, Bolsonaro, Branco): EB assume 0 votos
- Seção 3 com 0 registros totais: seção é descartada

#### **4.2.3 Tratamento de Votos Inválidos**

**Problema**: Dados TSE incluem categorias de votação inválida (NULO, BRANCO).

**Solução**:
- Votos com candidato NULO ou BRANCO são **excluídos** do cálculo de percentuais
- Contabilizados separadamente para análise de abstenção se necessário
- Total válido = soma de votos de candidatos válidos (excluindo NULO/BRANCO)

**Fórmula**:
```
total_válido = soma(QT_VOTOS) para todos os registros 
               EXCETO where NM_VOTAVEL contains "NULO" or "BRANCO"
```

#### **4.2.4 Detecção e Tratamento de Outliers**

**Problema**: Seções com número extremamente baixo ou alto de votos podem enviesar análises.

**Solução**:
- Seções com < 50 votos totais são flagadas como "baixa representatividade"
- Seções com > 1500 votos são verificadas contra padrão histórico
- Nenhuma seção é descartada, mas aquelas fora de padrão são anotadas para contexto interpretativo

#### **4.2.5 Agregação por Seção**

Após limpeza, dados são agregados por seção utilizando transformação GroupBy:

```
AGRUPAMENTO: (municipio, numero_secao)
AGREGAÇÃO:
  - votos_pt = soma de QT_VOTOS where candidato contém "LULA"
  - votos_bolsonaro = soma de QT_VOTOS where candidato contém "BOLSONARO"
  - votos_eb = soma de QT_VOTOS where candidato contém "BRAGA"
  - total_válido = soma total excluindo NULO/BRANCO
```

Resultado: Dataset com 4.468 linhas (uma por seção) pronto para análise.

### 4.3 Etapa 3: Ponderação e Cálculo (A Fórmula Matemática do Negócio)

#### **4.3.1 Cálculo de Percentuais por Seção**

Primeira operação de análise é transformação de votos absolutos em percentuais:

```
pt_pct_seção = (votos_pt / total_válido) × 100
bolsonaro_pct_seção = (votos_bolsonaro / total_válido) × 100
eb_pct_seção = (votos_eb / total_válido) × 100
```

**Tratamento de Divisão por Zero**: Se total_válido = 0 (seção sem votação válida), percentuais são definidos como 0. Seção é flagada como inválida para análises posteriores.

#### **4.3.2 Cálculo de Benchmarks Estaduais**

Sistema calcula três benchmarks estaduais através de agregação de TODOS os votos do estado:

```
pt_pct_estado = (soma de votos_pt de TODAS seções) / (soma de total_válido de TODAS seções) × 100
eb_pct_estado = (soma de votos_eb de TODAS seções) / (soma de total_válido de TODAS seções) × 100
bolsonaro_pct_estado = (soma de votos_bolsonaro de TODAS seções) / (soma de total_válido de TODAS seções) × 100
```

**Para Amazonas 2022:**
- PT: 50,32%
- Bolsonaro: 45,78%
- EB (Eduardo Braga): 31,93%

Estes benchmarks servem como **pontos de referência absoluta** contra os quais cada seção é comparada.

#### **4.3.3 Cálculo do Índice Nacional**

O índice nacional de uma seção expressa quantos pontos percentuais a seção desvia da média estadual de PT, normalizado em escala -1 a +1:

```
indice_nacional_seção = (pt_pct_seção - pt_pct_estado) / 100
```

**Interpretação**:
- Seção com PT 50,32% (igual estado) → indice_nacional = 0,00
- Seção com PT 60,32% (10 pontos acima estado) → indice_nacional = +0,10
- Seção com PT 40,32% (10 pontos abaixo estado) → indice_nacional = -0,10
- Máximo teórico: +0,50 (seção com 100% PT vs 50,32% estado)
- Mínimo teórico: -0,45 (seção com 0% PT vs 50,32% estado)

**Uso Analítico**: Identifica seções que são **atípicas** em relação ao padrão estadual. Valores positivos altos = bastião presidencial; valores negativos altos = território hostil ao candidato.

#### **4.3.4 Cálculo do Índice EB (Regional)**

Análogo ao índice nacional, mas focando no candidato regional (Eduardo Braga):

```
indice_eb_seção = (eb_pct_seção - eb_pct_estado) / 100
```

**Interpretação**:
- Seção com EB 31,93% (igual estado) → indice_eb = 0,00
- Seção com EB 41,93% (10 pontos acima) → indice_eb = +0,10 (bastião regional)
- Seção com EB 21,93% (10 pontos abaixo) → indice_eb = -0,10 (território difícil)

**Uso Analítico**: Identificar seções onde candidato regional possui força excepcional (valores positivos) vs. fraqueza excepcional (valores negativos).

#### **4.3.5 Cálculo de Volatilidade Eleitoral**

Volatilidade de uma seção é definida como magnitude de mudança de comportamento de votação entre ciclos eleitorais:

```
volatilidade_seção = |pt_pct_2022 - pt_pct_2018| / 100
```

**Interpretação**:
- Volatilidade = 0,00 → seção votou percentualmente igual em 2018 e 2022
- Volatilidade = 0,15 → seção mudou 15 pontos percentuais entre ciclos (mudança moderada)
- Volatilidade = 0,30+ → seção mudou 30+ pontos percentuais (movimento eleitoral significativo)

**Caso Concreto**:
- Seção A: PT 40% em 2018, PT 55% em 2022 → volatilidade = 0,15 (swing territory)
- Seção B: PT 50% em 2018, PT 50% em 2022 → volatilidade = 0,00 (stable territory)

**Uso Analítico**: Identifica seções onde comportamento eleitoral é instável e pode mudar novamente. Alta volatilidade = potencial eleitoral significativo em eleições futuras.

#### **4.3.6 Integração Multidimensional: Classificação Automática**

O sistema aplica algoritmo de classificação que combina os três índices em regra de decisão em cascata:

```
SE indice_eb < -0,05:
    CATEGORIA = "DIFÍCIL"
    DESCRIÇÃO = EB performing significantly below state average
    
SENÃO SE indice_nacional > 0,05 AND indice_eb > -0,02:
    CATEGORIA = "LULA+EB"
    DESCRIÇÃO = PT ahead of baseline AND EB not severely struggling
    
SENÃO SE eb_pct_seção > 30 AND bolsonaro_pct_seção > pt_pct_seção:
    CATEGORIA = "EB_PURO"
    DESCRIÇÃO = EB has exceptional strength (>30%) even with Bolsonaro ahead
    
SENÃO SE indice_nacional < -0,05 AND eb_pct_seção > 25:
    CATEGORIA = "BOLSO+EB"
    DESCRIÇÃO = Bolsonaro dominant but EB maintains meaningful presence
    
SENÃO SE volatilidade > 0,15 OR (indice_eb > -0,05 AND indice_eb < 0,03):
    CATEGORIA = "PURO_SWING"
    DESCRIÇÃO = High volatility OR EB performance near state average
    
SENÃO:
    CATEGORIA = "LULA+EB"
    DESCRIÇÃO = Default category (majority of cases)
```

**Lógica Subjacente**:

A ordem da cascata é **criticamente importante**. As condições são ordenadas por especificidade decrescente:

1. **DIFÍCIL** (primeira condição) é a mais específica e hostil → captura seções com EB extremamente fraco
2. **LULA+EB** (segunda) é a segunda mais específica → captura seções com PT forte E EB não fraco
3. **EB_PURO** (terceira) captura exceções onde EB é forte mesmo com Bolsonaro na frente
4. **BOLSO+EB** (quarta) captura o inverso: Bolsonaro na frente MAS EB presente
5. **PURO_SWING** (quinta) captura seções voláteis ou equilibradas
6. **LULA+EB** (default) é default, capturando remanescentes

**Atribuição de Cor**:
Cada categoria recebe cor hexadecimal para visualização cartográfica:
- LULA+EB = #27AE60 (verde = seguro/favorável)
- DIFÍCIL = #E74C3C (vermelho = hostil)
- PURO_SWING = #F4D03F (amarelo = equilibrado)
- BOLSO+EB = #E67E22 (laranja = competitivo)
- EB_PURO = #8E44AD (roxo = regional strength)

### 4.4 Etapa 4: Geração de Saída e Estruturação Final

#### **4.4.1 Construção de Dataset de Saída**

Após classificação, sistema constrói dataset de saída contendo para CADA SEÇÃO os seguintes campos:

```
numero_secao: int (ID único)
municipio: str (nome do município)
endereco: str (endereço do local de votação)
categoria: str (uma de 5 classes)
cor: str (código hexadecimal)
latitude: float (coordenada WGS-84)
longitude: float (coordenada WGS-84)
raio_km: int (raio de influência)
indice_nacional: float (desvio de PT)
indice_eb: float (desvio de EB)
volatilidade: float (mudança eleitoral)
votos_2022: dict contendo:
  - pt: int (votos absolutos)
  - pt_pct: float (percentual)
  - bolsonaro: int (votos absolutos)
  - bolsonaro_pct: float (percentual)
  - eb: int (votos absolutos)
  - eb_pct: float (percentual)
preditivo_2026: dict contendo:
  - classificacao: str (categoria)
  - score: float (índice combinado)
  - tendencia: str ("positiva", "negativa", "estável")
  - volatilidade: float
  - pt_projecao: float (percentual projetado para 2026)
  - direita_projecao: float (percentual projetado para 2026)
  - eb_projecao: float (percentual projetado para 2026)
```

#### **4.4.2 Geração de Coordenadas Geográficas**

Para cada seção, sistema gera coordenadas latitude/longitude através de processo de offset aleatório:

```
BASE_COORDS[municipio] = coordenadas do centroide municipal (obtido de gazetteer)
RAIO = raio_km da seção (3 km Manaus, 6 km interior, 15 km rural)

Para cada seção:
  ângulo = número aleatório entre 0 e 2π
  distância = número aleatório entre 0 e RAIO km
  
  lat_offset = (distância × cos(ângulo)) / 111 km/grau
  lon_offset = (distância × sin(ângulo)) / (111 km/grau × cos(lat))
  
  latitude_final = BASE_COORDS[municipio].lat + lat_offset
  longitude_final = BASE_COORDS[municipio].lon + lon_offset
```

**Significado**: Cada ponto recebe coordenadas ligeiramente deslocadas do centroide municipal, dentro do raio especificado. Isto preserve privacidade do local exato de votação enquanto mantém aproximação geográfica.

#### **4.4.3 Exportação em Múltiplos Formatos**

Sistema exporta dataset consolidado em três formatos padrão:

**Formato CSV:**
```
numero_secao,municipio,categoria,latitude,longitude,raio_km,endereco,indice_nacional,indice_eb,preditivo_classificacao,preditivo_score,votos_pt_2022,votos_pt_pct_2022,votos_bolsonaro_2022,votos_bolsonaro_pct_2022,votos_eb_2022,votos_eb_pct_2022

1,ALVARÃES,LULA+EB,-3.6759,-64.70891,6,AVENIDA CASTELO BRANCO,0.271,-0.014,LULA+EB,0.257,471,77.5,122,20.1,178,30.5
```

**Formato XML:**
```xml
<dashboard versao="1.0" estado="Amazonas" total_secoes="4468">
  <secoes>
    <municipio nome="ALVARÃES" total_secoes="32">
      <secao>
        <numero>1</numero>
        <municipio>ALVARÃES</municipio>
        <endereco>AVENIDA CASTELO BRANCO</endereco>
        <classificacao>
          <categoria>LULA+EB</categoria>
          <cor>#27AE60</cor>
        </classificacao>
        <localizacao>
          <latitude>-3.6759</latitude>
          <longitude>-64.70891</longitude>
          <raio_km>6</raio_km>
        </localizacao>
        <indices>
          <nacional>0.271</nacional>
          <eb>-0.014</eb>
          <volatilidade>0</volatilidade>
        </indices>
        <votos_2022>
          <pt><votos>471</votos><percentual>77.5</percentual></pt>
          <bolsonaro><votos>122</votos><percentual>20.1</percentual></bolsonaro>
          <eb><votos>178</votos><percentual>30.5</percentual></eb>
        </votos_2022>
        <preditivo_2026>
          <classificacao>LULA+EB</classificacao>
          <score>0.257</score>
          <tendencia>positiva</tendencia>
          <projecoes>
            <pt>73.6</pt>
            <direita>21.1</direita>
            <eb>29.9</eb>
          </projecoes>
        </preditivo_2026>
      </secao>
    </municipio>
  </secoes>
</dashboard>
```

**Formato JSON:**
```json
{
  "ALVARÃES": [
    {
      "numero_secao": 1,
      "municipio": "ALVARÃES",
      "endereco": "AVENIDA CASTELO BRANCO",
      "categoria": "LULA+EB",
      "cor": "#27AE60",
      "latitude": -3.6759,
      "longitude": -64.70891,
      "raio_km": 6,
      "indice_nacional": 0.271,
      "indice_eb": -0.014,
      "volatilidade": 0,
      "votos_2022": {
        "pt": 471,
        "pt_pct": 77.5,
        "bolsonaro": 122,
        "bolsonaro_pct": 20.1,
        "eb": 178,
        "eb_pct": 30.5
      },
      "preditivo_2026": {
        "classificacao": "LULA+EB",
        "score": 0.257,
        "tendencia": "positiva",
        "pt_projecao": 73.6,
        "direita_projecao": 21.1,
        "eb_projecao": 29.9
      }
    }
  ]
}
```

#### **4.4.4 Validação de Saída**

Sistema realiza validações finais:
- Verificação que 4.468 seções foram processadas
- Verificação que cada seção possui categoria válida
- Verificação que cada seção possui coordenadas
- Contagem de distribuição por categoria (esperado: LULA+EB ~50%, DIFÍCIL ~28%, PURO_SWING ~12%, BOLSO+EB ~6%, EB_PURO ~3%)

Se validações falharem, dataset não é exportado e sistema retorna mensagem de erro.

© 2026. Todos os direitos reservados. Obra intelectual protegida nos termos da Lei nº 9.610/98.

---

## 5. APLICAÇÃO PRÁTICA E REGRAS DE RETORNO

### 5.1 Interação do Usuário com o Sistema

#### **5.1.1 Interface de Usuário (Dashboard Interativo)**

O Radar Eleitoral é acessado através de interface web com arquitetura cliente-servidor:

**Componentes de Interface:**

1. **Menu de Navegação Principal**
   - Abas temáticas: "Mapa", "Radar Eleitoral", "Impulsionamento", "Dados Brutos"
   - Cada aba ativa seção distinta do dashboard

2. **Tab "Mapa"**
   - Usuário visualiza mapa georreferenciado do Amazonas
   - 4.468 pontos (seções) são plotados com cores segundo categoria
   - Comportamento interativo:
     * Hover sobre ponto = tooltip mostra número seção, endereço, categoria
     * Click sobre ponto = detalhe expandido com índices completos
     * Scroll = zoom in/out
   - Legenda visual com cores e descrições

3. **Tab "Impulsionamento"**
   - Dropdown de seleção de município
   - Ao selecionar município:
     * Mapa executa zoom automático ao município
     * Todos os 4.468 pontos desaparecem
     * Apenas seções do município selecionado são visualizadas
     * Contagem de seções é mostrada
   - Botão "Baixar CSV" permite exportação de dados do município selecionado
   - Tabela com lista de seções abaixo do mapa

4. **Tab "Radar Eleitoral"**
   - Análises e estatísticas agregadas
   - Gráficos de distribuição por categoria
   - Rankings de municípios por índices

5. **Tab "Dados Brutos"**
   - Tabela com todas as 4.468 seções
   - Coluna buscável para filtro por município
   - Ordenação por qualquer coluna (click no header)

#### **5.1.2 Fluxo Operacional Típico**

**Cenário: Gerente de Campanha quer alocar 30 militantes em Manaus**

1. Acessa dashboard → clica Tab "Impulsionamento"
2. Dropdown seleciona "MANAUS"
3. Mapa faz zoom automático a Manaus; 783 seções são exibidas
4. Verifica distribuição:
   - Verde (LULA+EB): 2 seções = 0% (nenhuma)
   - Vermelho (DIFÍCIL): 518 seções = 66,2% → Maioria é difícil
   - Laranja (BOLSO+EB): 234 seções = 29,9% → Segundo maior grupo
   - Roxo (EB_PURO): 25 seções = 3,2% → Pequeno bastião regional
   - Amarelo (PURO_SWING): 6 seções = 0,8% → Muito poucos
5. Aloca recursos: 12 militantes em DIFÍCIL, 15 em BOLSO+EB, 3 em EB_PURO
6. Clica "Baixar CSV" para exportar dados de Manaus
7. Envia CSV para equipe de campo com instruções por categoria

#### **5.1.3 Operações Específicas do Sistema**

**Operação: Filtro por Município e Zoom**
```
Entrada: Seleção de município via dropdown
Processamento: 
  - Sistema recupera lista de 4.468 seções
  - Filtra para seções onde municipio == selecionado
  - Calcula bounding box (latitude/longitude min/max)
  - Instrui map engine (Leaflet) a fazer zoom automático
  - Recarrega pontos no mapa (mostra apenas seções filtradas)
Saída: Mapa com zoom e seções visíveis do município
Latência típica: 200-500ms
```

**Operação: Exportação de CSV**
```
Entrada: Clique em botão "Baixar CSV" (com ou sem filtro municipal)
Processamento:
  - Se município está selecionado: filtra 4.468 seções para municipio == selecionado
  - Se nenhum município selecionado: usa todas as 4.468 seções
  - Itera cada seção e constrói linha CSV com 24 colunas
  - Envolve nomes (endereco) em aspas duplas e escapa aspas internas
  - Gera arquivo CSV em memória
  - Instrui navegador a fazer download com nome TODAS_SECOES_MAPEADAS.csv
Saída: Arquivo CSV para importação em Excel/Sheets
Tamanho típico: 2.5 MB
```

**Operação: Busca em Dados Brutos**
```
Entrada: Digitação em campo de busca por município (ex: "MANAUS")
Processamento:
  - Sistema filtra tabela em tempo real (regex case-insensitive)
  - Exibe apenas linhas que contêm termo de busca
  - Atualiza contagem de resultados
Saída: Tabela reduzida mostrando apenas seções do município
Latência: < 100ms
```

### 5.2 Formatos de Saída Gerados

#### **5.2.1 Saída CSV (para Planilhas)**

**Estrutura de Linhas:**
```
numero_secao,municipio,categoria,latitude,longitude,raio_km,endereco,...
[4.468 linhas]
```

**Colunas (24 total):**
1. `numero_secao` — ID único
2. `municipio` — Localização
3. `endereco` — Local de votação
4. `categoria` — Uma de 5 classes
5. `cor` — Código hex para visualização
6. `latitude` — Coordenada WGS-84
7. `longitude` — Coordenada WGS-84
8. `raio_km` — Raio de influência
9. `indice_nacional` — Desvio de PT
10. `indice_eb` — Desvio de EB
11. `volatilidade` — Mudança eleitoral
12-17. `votos_*_2022` — Votos por candidato
18-20. `preditivo_2026_*` — Projeções

**Utilização**: Importação em Excel, Google Sheets, Tableau, Power BI para análises adicionais e cruzamentos com dados terceiros (demográficos, econômicos, etc.)

#### **5.2.2 Saída XML (para APIs e Integrações)**

**Estrutura Hierárquica:**
```xml
<dashboard> [atributos gerais]
  ├─ <metadata> [nome, versão, data]
  └─ <secoes>
      └─ <municipio> [nome, contagem]
          └─ <secao> [4.468 elementos]
```

**Cada seção contém:** 24 campos como CSV, mas estruturados hierarquicamente

**Utilização**: Integração com sistemas terceiros via REST APIs, automação de relatórios, sincronização com Data Warehouses

#### **5.2.3 Saída JSON (para Aplicações Web)**

**Estrutura Hierárquica:**
```json
{
  "MANAUS": [4.468 seções como objetos],
  "PARINTINS": [...],
  ...
}
```

**Cada seção é objeto JavaScript/JSON completo**

**Utilização**: Integração com aplicações web frontend, visualizações customizadas com D3.js/Plotly, Mobile apps

#### **5.2.4 Saída Dashboard (Visualização Interativa)**

Sistema também entrega visualização interativa através de interface web:
- Mapa cartográfico com 4.468 pontos coloridos
- Filtros e buscas em tempo real
- Tabelas ordenáveis
- Análises gráficas (gráficos de barra, dispersão, etc.)
- Tooltips e detalhes expandidos

**Utilização**: Análise exploratória interativa, apresentações, comunicação com stakeholders

### 5.3 Limitações Técnicas e Escopo Explícito

#### **5.3.1 O Que o Sistema NÃO Faz**

O Radar Eleitoral opera sob escopo definido. As seguintes capacidades NÃO estão incluídas:

1. **Não realiza previsão probabilística individual**
   - Sistema projeta tendências agregadas, não prevê voto de eleitores individuais
   - Não utiliza machine learning para classificação de indivíduos

2. **Não integra dados demográficos**
   - Sistema utiliza APENAS dados de votação histórica e regional
   - Não incorpora age, gênero, renda, escolaridade ou outras variáveis demográficas
   - Quando necessário, deve-se integrar externamente

3. **Não realiza análise de redes sociais**
   - Não monitora menções em redes sociais, sentimento ou influenciadores
   - Estas dimensões devem ser analisadas com ferramentas terceiras

4. **Não fornece justificativa causal de mudanças**
   - Sistema identifica mudanças de comportamento, mas não explica causas
   - (ex: identifica que uma seção mudou 20 pontos, mas não explica se foi por economia, educação ou outros fatores)

5. **Não realiza otimização de alocação de recursos**
   - Sistema fornece informações; decisão de alocação é responsabilidade do usuário
   - Pode ser integrado com ferramentas de otimização externa

6. **Não produz relatórios automáticos**
   - Interface entrega dados brutos; relatórios estratégicos devem ser construídos pelo usuário

#### **5.3.2 Premissas e Limitações Conhecidas**

1. **Limite de Granularidade**: Seção eleitoral é a menor unidade de análise; não desagrega para nível de local de votação específico (urnas eletrônicas)

2. **Limite Temporal**: Projeções 2026 baseiam-se em volatilidade 2018-2022; eventos políticos disruptivos após 2022 não são capturados

3. **Limite Representatividade**: Seções com < 50 votos possuem menor representatividade estatística (maior variância)

4. **Limite Geográfico**: Raios de influência (3/6/15 km) são aproximações; realidade geográfica (rios, montanhas, vias de acesso) não são considerados

5. **Limite de Atualização**: Sistema processa dados históricos; para incorporar dados atuais (pesquisas 2024/2025) requer manual data ingestion

#### **5.3.3 Pressupostos Metodológicos Implícitos**

1. **Comportamento Eleitoral é Previsível**: Sistema assume que histórico de votação possui poder preditivo; mudanças políticas ou econômicas estruturais podem invalidar projeções

2. **Comparabilidade Temporal**: Assume que dinâmica eleitoral entre 2018-2022 é similar à dinâmica 2022-2026; mudanças em sistema eleitoral ou candidatos podem quebrar este pressuposto

3. **Homogeneidade Intra-Seção**: Assume que todos votantes de uma seção compartilham contexto similar; seções geograficamente grandes podem conter diversidade intra-seção

4. **Dados TSE Sem Viés**: Assume que votação registrada reflete intenção eleitoral; abstenção sistemática ou voto estratégico não são capturados

### 5.4 Guia de Operação Prática

#### **5.4.1 Pré-Requisitos para Uso**

1. Acesso a navegador web moderno (Chrome, Firefox, Safari, Edge) com JavaScript habilitado
2. Conexão à internet (dashboard está hospedado em Vercel)
3. Conhecimento básico de análise eleitoral (para interpretação de índices)
4. Software para importação de CSV (Excel, Google Sheets, R, Python, etc.)

#### **5.4.2 Passos Básicos de Operação**

1. **Acesso ao Dashboard**
   - Navegar para URL do Vercel: https://[URL do projeto]
   - Aguardar carregamento (típico 2-3 segundos)

2. **Exploração Inicial**
   - Visualizar mapa → zoom out para ver estado inteiro
   - Observar distribuição de cores (categorias)
   - Passear mouse sobre pontos para ver tooltips

3. **Filtro por Município**
   - Ir à Tab "Impulsionamento"
   - Selecionar município via dropdown
   - Observar zoom automático e redistribuição de seções

4. **Exportação de Dados**
   - Clicar botão "Baixar CSV"
   - Arquivo é baixado para pasta Downloads
   - Importar em Excel/Sheets para análises adicionais

5. **Análises Comparativas**
   - Tab "Radar Eleitoral" mostra estatísticas agregadas
   - Tab "Dados Brutos" permite filtro por coluna
   - Utilizar filtro de municípios para análises comparativas

#### **5.4.3 Casos de Uso Específicos**

**Caso 1: Identificar Oportunidades de Impulsionamento**
```
1. Ir a Tab Impulsionamento
2. Selecionar município X
3. Identificar seções com categoria PURO_SWING ou EB_PURO
4. Focar conteúdo em diferenciação de EB para BOLSO+EB
5. Aumentar volume em DIFÍCIL com conteúdo de persuasão
```

**Caso 2: Monitoramento de Volatilidade**
```
1. Tab Dados Brutos
2. Ordenar por coluna "volatilidade" (descending)
3. Identificar top 50 seções com maior volatilidade
4. Exportar lista
5. Estabelecer monitoramento especial para estas seções
```

**Caso 3: Análise Comparativa Entre Municípios**
```
1. Tab Impulsionamento → selecionar município A → Baixar CSV
2. Tab Impulsionamento → selecionar município B → Baixar CSV
3. Importar ambos em Excel
4. Comparar distribuição de categorias
5. Calcular índices agregados por município
```

© 2026. Todos os direitos reservados. Obra intelectual protegida nos termos da Lei nº 9.610/98.

---

## CONCLUSÃO

O Radar Eleitoral representa evolução metodológica significativa em análise eleitoral, transitando de agregação municipal (baixa granularidade) para análise de seção eleitoral (alta granularidade), combinada com dimensionamento temporal (volatilidade) e geoespacial (geolocalização).

Sua metodologia é tecnicamente rigorous, reproduzível e escalável para qualquer territorio administrativo. O sistema entrega ao usuário instrumentos de decisão baseados em dados factuais de votação histórica, com projeções preditivas calibradas por volatilidade observada.

A documentação técnica aqui apresentada estabelece as bases para:
1. Replicação da metodologia em outros contextos
2. Validação e auditoria da arquitetura
3. Integração com sistemas terceiros
4. Proteção de propriedade intelectual

**Data**: 27 de abril de 2026  
**Versão**: 1.0  
**Status**: Produção

© 2026. Todos os direitos reservados. Obra intelectual protegida nos termos da Lei nº 9.610/98.
