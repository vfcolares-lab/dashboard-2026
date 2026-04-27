#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIPELINE DE INTELIGÊNCIA ELEITORAL - AMAZONAS 2026
Processa dados do TSE e gera análise completa para dashboard
"""

import pandas as pd
import numpy as np
import json
import csv
from pathlib import Path
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIG
# ============================================================================
BASE_PATH = Path('/Users/vitorcolares/Desktop/relatorios tse')
OUTPUT_PATH = Path('/Users/vitorcolares/Desktop/relatorios tse/dashboard-2026')

# Arquivos TSE
TSE_FILES = {
    2010: BASE_PATH / 'votacao_secao_2010_AM/votacao_secao_2010_AM.csv',
    2014: BASE_PATH / 'votacao_secao_2014_AM/votacao_secao_2014_AM.csv',
    2018: BASE_PATH / 'data/raw/votacao_secao_2018_AM.csv',
    2022: BASE_PATH / 'votacao_secao_2022_AM/votacao_secao_2022_AM.csv',
    # Arquivos separados de Presidente
    '2010_pres': BASE_PATH / 'presidente_2010_AM_por_secao.csv',
    '2018_pres': BASE_PATH / 'presidente_2018_AM_por_secao.csv',
    '2022_pres': BASE_PATH / 'votacao_secao_2022_BR/votacao_secao_2022_BR.csv',
}

# Nomes de candidatos
EB_NAME = 'CARLOS EDUARDO DE SOUZA BRAGA'
PT_CANDIDATES = {
    2010: 'DILMA VANA ROUSSEFF LINHARES',
    2014: 'DILMA VANA ROUSSEFF LINHARES',
    2018: 'FERNANDO HADDAD TAMANDARÉ DE MELO',
    2022: 'LUIZ INÁCIO LULA DA SILVA'
}
RIGHT_CANDIDATES = {
    2010: 'JOSÉ ANÍBAL MENDES SATURNINO PEREIRA',
    2014: 'AÉCIO NEVES DO COUTO PEREIRA',
    2018: 'JAIR MESSIAS BOLSONARO',
    2022: 'JAIR MESSIAS BOLSONARO'
}

# ============================================================================
# 1. EXTRAÇÃO TSE
# ============================================================================
def load_tse_data():
    """Carrega e consolida dados do TSE"""
    print("📥 Carregando dados do TSE...")

    data = {}

    # Carregar 2010, 2014, 2018, 2022 (Amazonas)
    for year in [2010, 2014, 2018, 2022]:
        filepath = TSE_FILES[year]
        print(f"  {year} (votos por cargo)...", end='')

        df = pd.read_csv(
            filepath,
            delimiter=';',
            dtype={
                'NM_MUNICIPIO': str,
                'NR_ZONA': str,
                'NR_SECAO': str,
                'DS_CARGO': str,
                'NM_VOTAVEL': str,
                'QT_VOTOS': 'Int64',
                'NR_TURNO': 'Int64'
            },
            encoding='latin-1',
            low_memory=False
        )

        # Limpar strings
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip()
        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()

        data[year] = df
        print(f" ✓")

    # Carregar dados de Presidente de arquivos separados
    print(f"  2010 (Presidente separado)...", end='')
    df_pres_2010 = pd.read_csv(
        TSE_FILES['2010_pres'],
        delimiter=';',
        encoding='latin-1',
        low_memory=False
    )
    # Limpar e padronizar
    if 'NM_MUNICIPIO' in df_pres_2010.columns:
        df_pres_2010['NM_MUNICIPIO'] = df_pres_2010['NM_MUNICIPIO'].str.strip()
    if 'NM_VOTAVEL' in df_pres_2010.columns:
        df_pres_2010['NM_VOTAVEL'] = df_pres_2010['NM_VOTAVEL'].str.strip()
    if 'DS_CARGO' in df_pres_2010.columns:
        df_pres_2010['DS_CARGO'] = df_pres_2010['DS_CARGO'].str.strip().str.upper()
    else:
        df_pres_2010['DS_CARGO'] = 'PRESIDENTE'
    data['2010_pres'] = df_pres_2010
    print(f" ✓")

    print(f"  2018 (Presidente separado)...", end='')
    df_pres_2018 = pd.read_csv(
        TSE_FILES['2018_pres'],
        delimiter=';',
        encoding='latin-1',
        low_memory=False
    )
    if 'NM_MUNICIPIO' in df_pres_2018.columns:
        df_pres_2018['NM_MUNICIPIO'] = df_pres_2018['NM_MUNICIPIO'].str.strip()
    if 'NM_VOTAVEL' in df_pres_2018.columns:
        df_pres_2018['NM_VOTAVEL'] = df_pres_2018['NM_VOTAVEL'].str.strip()
    if 'DS_CARGO' in df_pres_2018.columns:
        df_pres_2018['DS_CARGO'] = df_pres_2018['DS_CARGO'].str.strip().str.upper()
    else:
        df_pres_2018['DS_CARGO'] = 'PRESIDENTE'
    data['2018_pres'] = df_pres_2018
    print(f" ✓")

    # 2022 Presidente (do arquivo BR)
    print(f"  2022 (Presidente de BR)...", end='')
    df_pres_2022 = pd.read_csv(
        TSE_FILES['2022_pres'],
        delimiter=';',
        encoding='latin-1',
        dtype={'SG_UF': str},
        low_memory=False
    )
    # Filtrar apenas AM
    df_pres_2022 = df_pres_2022[df_pres_2022['SG_UF'] == 'AM'].copy()
    if 'NM_MUNICIPIO' in df_pres_2022.columns:
        df_pres_2022['NM_MUNICIPIO'] = df_pres_2022['NM_MUNICIPIO'].str.strip()
    if 'NM_VOTAVEL' in df_pres_2022.columns:
        df_pres_2022['NM_VOTAVEL'] = df_pres_2022['NM_VOTAVEL'].str.strip()
    if 'DS_CARGO' in df_pres_2022.columns:
        df_pres_2022['DS_CARGO'] = df_pres_2022['DS_CARGO'].str.strip().str.upper()
    data['2022_pres'] = df_pres_2022
    print(f" ✓")

    return data

# ============================================================================
# 2. EXTRAÇÃO POR CARGO
# ============================================================================
def extract_by_cargo(data):
    """Extrai dados por cargo (Presidente, Senador, Governador)"""
    print("\n📊 Extraindo por cargo...")

    extracted = {}

    # 2010: Senado
    print("  2010 (Senado)...", end='')
    df_2010_senado = data[2010][data[2010]['DS_CARGO'] == 'SENADOR'].copy()
    extracted['2010_senado'] = df_2010_senado
    print(f" ✓")

    # 2010 Presidente (arquivo separado)
    if '2010_pres' in data and len(data['2010_pres']) > 0:
        print(f"  2010 (Presidente)...", end='')
        extracted['2010_pres'] = data['2010_pres'].copy()
        print(f" ✓")

    # 2014: Governador
    print("  2014 (Governador)...", end='')
    df_2014_gov = data[2014][data[2014]['DS_CARGO'] == 'GOVERNADOR'].copy()
    extracted['2014_gov'] = df_2014_gov
    print(f" ✓")

    # 2014 Presidente (buscar no arquivo 2014)
    pres_2014 = data[2014][data[2014]['DS_CARGO'] == 'PRESIDENTE']
    if len(pres_2014) > 0:
        print(f"  2014 (Presidente)...", end='')
        extracted['2014_pres'] = pres_2014.copy()
        print(f" ✓")

    # 2018: Senado
    print("  2018 (Senado)...", end='')
    df_2018_senado = data[2018][data[2018]['DS_CARGO'] == 'SENADOR'].copy()
    extracted['2018_senado'] = df_2018_senado
    print(f" ✓")

    # 2018 Presidente (arquivo separado)
    if '2018_pres' in data and len(data['2018_pres']) > 0:
        print(f"  2018 (Presidente)...", end='')
        extracted['2018_pres'] = data['2018_pres'].copy()
        print(f" ✓")

    # 2022: Governador
    print("  2022 (Governador)...", end='')
    df_2022_gov = data[2022][data[2022]['DS_CARGO'] == 'GOVERNADOR'].copy()
    extracted['2022_gov'] = df_2022_gov
    print(f" ✓")

    # 2022 Presidente (arquivo separado)
    if '2022_pres' in data and len(data['2022_pres']) > 0:
        print(f"  2022 (Presidente)...", end='')
        extracted['2022_pres'] = data['2022_pres'].copy()
        print(f" ✓")

    return extracted

# ============================================================================
# 3. AGREGAÇÃO POR MUNICÍPIO
# ============================================================================
def aggregate_by_municipio(extracted):
    """Agrega votos por município"""
    print("\n🏛️  Agregando por município...")

    municipios_data = {}

    # Inicializar dicionário de municípios
    all_municipios = set()
    for key, df in extracted.items():
        all_municipios.update(df['NM_MUNICIPIO'].unique())

    for mun in sorted(all_municipios):
        municipios_data[mun] = {
            'eleitorado_2022': 0,
            'presidente': {},
            'eb': {},
            'votos_validos': {}
        }

    # Processar Presidente
    print("  Presidente...", end='')
    for year_key, year in [('2010_pres', 2010), ('2014_pres', 2014), ('2018_pres', 2018), ('2022_pres', 2022)]:
        if year_key not in extracted:
            continue

        df = extracted[year_key]

        for mun in all_municipios:
            df_mun = df[df['NM_MUNICIPIO'] == mun]

            # Total válido
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                municipios_data[mun]['votos_validos'][year] = total_valido

                # PT
                pt_candidate = PT_CANDIDATES.get(year)
                if pt_candidate:
                    votos_pt = df_mun[df_mun['NM_VOTAVEL'] == pt_candidate]['QT_VOTOS'].sum()
                    pct_pt = (votos_pt / total_valido) * 100
                else:
                    pct_pt = 0

                # Direita
                right_candidate = RIGHT_CANDIDATES.get(year)
                if right_candidate:
                    votos_right = df_mun[df_mun['NM_VOTAVEL'] == right_candidate]['QT_VOTOS'].sum()
                    pct_right = (votos_right / total_valido) * 100
                else:
                    pct_right = 0

                municipios_data[mun]['presidente'][year] = {
                    'pt': round(pct_pt, 1),
                    'direita': round(pct_right, 1),
                    'margem': round(pct_pt - pct_right, 1)
                }
    print(" ✓")

    # Processar Eduardo Braga
    print("  Eduardo Braga...", end='')
    for year_key, (year, cargo) in [
        ('2010_senado', (2010, 'Senado')),
        ('2014_gov', (2014, 'Governador')),
        ('2018_senado', (2018, 'Senado')),
        ('2022_gov', (2022, 'Governador')),
    ]:
        if year_key not in extracted:
            continue

        df = extracted[year_key]

        # Calcular média estadual de EB
        votos_eb_estado = df[df['NM_VOTAVEL'] == EB_NAME]['QT_VOTOS'].sum()
        total_valido_estado = df[~df['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        pct_eb_estado = (votos_eb_estado / total_valido_estado * 100) if total_valido_estado > 0 else 0

        for mun in all_municipios:
            df_mun = df[df['NM_MUNICIPIO'] == mun]
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                votos_eb = df_mun[df_mun['NM_VOTAVEL'] == EB_NAME]['QT_VOTOS'].sum()
                pct_eb = (votos_eb / total_valido) * 100
                diff = pct_eb - pct_eb_estado

                municipios_data[mun]['eb'][year] = {
                    'cargo': cargo,
                    'votos_pct': round(pct_eb, 1),
                    'media_estado': round(pct_eb_estado, 1),
                    'diff': round(diff, 1)
                }
    print(" ✓")

    return municipios_data

# ============================================================================
# 4. CLASSIFICAÇÃO: ÍNDICE NACIONAL
# ============================================================================
def calculate_national_index(municipios_data):
    """Calcula Índice Nacional (Lulismo vs Bolsonarismo)"""
    print("\n🔴🔵 Calculando Índice Nacional...")

    for mun, data in municipios_data.items():
        margins = []
        weights = [0.10, 0.15, 0.30, 0.45]  # 2010, 2014, 2018, 2022

        for i, year in enumerate([2010, 2014, 2018, 2022]):
            if year in data['presidente']:
                margin = data['presidente'][year]['margem']
                margins.append(margin * weights[i])
            else:
                margins.append(0)

        in_index = sum(margins)

        # Classificação
        if in_index > 0.30:
            class_nat = 'Bastião Lulista'
        elif in_index > 0.10:
            class_nat = 'Tendência Lulista'
        elif in_index >= -0.10:
            class_nat = 'Swing'
        elif in_index >= -0.30:
            class_nat = 'Tendência Bolsonarista'
        else:
            class_nat = 'Bastião Bolsonarista'

        municipios_data[mun]['indice_nacional'] = round(in_index, 3)
        municipios_data[mun]['classificacao_nacional'] = class_nat

    print("  ✓")

# ============================================================================
# 5. CLASSIFICAÇÃO: ÍNDICE EB
# ============================================================================
def calculate_eb_index(municipios_data):
    """Calcula Índice Eduardo Braga"""
    print("📌 Calculando Índice Eduardo Braga...")

    for mun, data in municipios_data.items():
        diffs = []
        weights = [0.10, 0.15, 0.30, 0.45]  # 2010, 2014, 2018, 2022

        for i, year in enumerate([2010, 2014, 2018, 2022]):
            if year in data['eb']:
                diff = data['eb'][year]['diff']
                diffs.append(diff * weights[i])
            else:
                diffs.append(0)

        ieb_index = sum(diffs)

        # Classificação
        if ieb_index > 0.15:
            class_eb = 'Bastião Eduardista'
        elif ieb_index > 0.05:
            class_eb = 'Tendência Eduardista'
        elif ieb_index >= -0.05:
            class_eb = 'Swing'
        elif ieb_index >= -0.15:
            class_eb = 'Tendência Anti-EB'
        else:
            class_eb = 'Bastião Anti-EB'

        municipios_data[mun]['indice_eb'] = round(ieb_index, 3)
        municipios_data[mun]['classificacao_eb'] = class_eb

    print("  ✓")

# ============================================================================
# 6. CLASSIFICAÇÃO: E1-E6
# ============================================================================
def assign_e1e6(municipios_data):
    """Atribui eixo estratégico E1-E6"""
    print("📊 Atribuindo eixos E1-E6...")

    for mun, data in municipios_data.items():
        in_index = data['indice_nacional']

        # Interior vs Manaus (assumir todo não-Manaus como interior)
        is_manaus = mun == 'MANAUS'

        if in_index > 0:  # Lulista
            eixo = 'E2' if is_manaus else 'E1'
            label = 'Lulismo Manaus' if is_manaus else 'Lulismo Interior'
        elif in_index > -0.10:  # Swing/Amazonas
            eixo = 'E4' if is_manaus else 'E3'
            label = 'Amazonas Manaus' if is_manaus else 'Amazonas Interior'
        else:  # Bolsonarista
            eixo = 'E6' if is_manaus else 'E5'
            label = 'Bolsonarismo Manaus' if is_manaus else 'Bolsonarismo Interior'

        municipios_data[mun]['eixo_estrategico'] = eixo
        municipios_data[mun]['eixo_label'] = label

    print("  ✓")

# ============================================================================
# 7. MODELO PREDITIVO 2026
# ============================================================================
def calculate_predictive_model(municipios_data):
    """Calcula projeção 2026"""
    print("🎯 Calculando modelo preditivo 2026...")

    for mun, data in municipios_data.items():
        eb_data = data.get('eb', {})

        # Dados históricos de EB
        years = sorted([y for y in [2010, 2014, 2018, 2022] if y in eb_data])

        if len(years) >= 2:
            values = [eb_data[y]['diff'] for y in years]

            # Regressão linear (tendência)
            years_num = np.array([i for i in range(len(years))])
            values_num = np.array(values)

            if len(years_num) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(years_num, values_num)
                # Projetar para próxima eleição (índice 4)
                tendencia = slope * 3 + values[-1]  # 3 eleições depois, começando do último
            else:
                tendencia = values[-1]

            # Correlação Lula-EB
            correlacao = 0.0
            if 2022 in data['presidente'] and 2022 in eb_data:
                # Simplificado: se Lula foi bem, EB tem chance
                lula_margem = data['presidente'][2022]['margem']
                eb_diff = eb_data[2022]['diff']
                if abs(lula_margem) > 0 and abs(eb_diff) > 0:
                    correlacao = (lula_margem + eb_diff) / 2 / 100  # Normalizar

            # Score preditivo
            tendencia_norm = max(min(tendencia / 20, 1), -1)  # Normalizar para [-1, 1]
            correlacao_norm = max(min(correlacao, 1), -1)
            ultima_eleicao_norm = max(min(eb_data[2022]['diff'] / 20, 1), -1) if 2022 in eb_data else 0

            score = (tendencia_norm * 0.40) + (correlacao_norm * 0.25) + (ultima_eleicao_norm * 0.35)
            score = (score + 1) / 2  # Normalizar para [0, 1]
            score = max(min(score, 1), 0)

            # Classificação preditiva
            if score > 0.55:
                pred_class = 'SEGURO EB'
            elif score > 0.45:
                pred_class = 'COMPETITIVO PRÓ-EB'
            elif score > 0.40:
                pred_class = 'BATTLEGROUND'
            elif score > 0.35:
                pred_class = 'COMPETITIVO CONTRA'
            else:
                pred_class = 'DIFÍCIL'

            data['preditivo_2026'] = {
                'score': round(score, 3),
                'classificacao': pred_class,
                'tendencia': 'positiva' if tendencia > 0 else 'negativa' if tendencia < 0 else 'neutra',
                'volatilidade': round(np.std(values), 3) if len(values) > 1 else 0
            }
        else:
            data['preditivo_2026'] = {
                'score': 0.5,
                'classificacao': 'INDEFINIDO',
                'tendencia': 'neutra',
                'volatilidade': 0
            }

    print("  ✓")

# ============================================================================
# 8. EXECUTAR PIPELINE
# ============================================================================
def run_pipeline():
    """Executa pipeline completo"""
    print("\n" + "="*70)
    print("🚀 PIPELINE DE INTELIGÊNCIA ELEITORAL - AMAZONAS 2026")
    print("="*70)

    # 1. Carregar
    data = load_tse_data()

    # 2. Extrair por cargo
    extracted = extract_by_cargo(data)

    # 3. Agregar por município
    municipios_data = aggregate_by_municipio(extracted)

    # 4-7. Calcular índices
    calculate_national_index(municipios_data)
    calculate_eb_index(municipios_data)
    assign_e1e6(municipios_data)
    calculate_predictive_model(municipios_data)

    # Remover municípios sem dados relevantes
    municipios_data = {k: v for k, v in municipios_data.items() if len(v['presidente']) > 0}

    print(f"\n✅ Processados {len(municipios_data)} municípios")

    # Converter numpy int64/float64 para int/float para JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj) if isinstance(obj, np.floating) else int(obj)
        return obj

    municipios_data = convert_to_serializable(municipios_data)

    # 9. Salvar em JSON (data.js)
    print("\n💾 Salvando dados...")

    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'state': 'Amazonas',
            'total_municipalities': len(municipios_data),
            'elections': [2010, 2014, 2018, 2022]
        },
        'municipios': municipios_data
    }

    # Salvar como data.js
    output_file = OUTPUT_PATH / 'data.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('const DASHBOARD_DATA = ')
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write(';\n')

    print(f"  ✓ {output_file}")

    # Salvar como data.json também
    json_file = OUTPUT_PATH / 'data.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  ✓ {json_file}")

    # 10. Estatísticas
    print("\n📊 ESTATÍSTICAS:")

    classes_nat = {}
    classes_eb = {}
    eixos = {}
    pred_classes = {}

    for mun, data in municipios_data.items():
        classes_nat[data['classificacao_nacional']] = classes_nat.get(data['classificacao_nacional'], 0) + 1
        classes_eb[data['classificacao_eb']] = classes_eb.get(data['classificacao_eb'], 0) + 1
        eixos[data['eixo_estrategico']] = eixos.get(data['eixo_estrategico'], 0) + 1
        pred_classes[data['preditivo_2026']['classificacao']] = pred_classes.get(data['preditivo_2026']['classificacao'], 0) + 1

    print("\n  Classificação Nacional:")
    for cls, count in sorted(classes_nat.items()):
        print(f"    {cls}: {count}")

    print("\n  Classificação EB:")
    for cls, count in sorted(classes_eb.items()):
        print(f"    {cls}: {count}")

    print("\n  Eixos Estratégicos:")
    for eixo, count in sorted(eixos.items()):
        print(f"    {eixo}: {count}")

    print("\n  Prognóstico 2026:")
    for pred, count in sorted(pred_classes.items()):
        print(f"    {pred}: {count}")

    print("\n" + "="*70)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*70 + "\n")

if __name__ == '__main__':
    run_pipeline()
