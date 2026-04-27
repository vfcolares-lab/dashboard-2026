#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIPELINE CORRIGIDO - Apenas 62 municípios do Amazonas (2022 como referência)
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

BASE_PATH = Path('/Users/vitorcolares/Desktop/relatorios tse')
OUTPUT_PATH = Path('/Users/vitorcolares/Desktop/relatorios tse/dashboard-2026')

# ============================================================================
# 1. DEFINIR 62 MUNICÍPIOS OFICIAIS
# ============================================================================

AMAZONAS_62 = [
    "ALVARÃES", "AMATURÁ", "ANAMÃ", "ANORI", "APUÍ", "ATALAIA DO NORTE", "AUTAZES",
    "BARCELOS", "BARREIRINHA", "BENJAMIN CONSTANT", "BERURI", "BOA VISTA DO RAMOS",
    "BOCA DO ACRE", "BORBA", "CAAPIRANGA", "CANUTAMA", "CARAUARI", "CAREIRO",
    "CAREIRO DA VÁRZEA", "COARI", "CODAJÁS", "EIRUNEPÉ", "ENVIRA", "FONTE BOA",
    "GUAJARÁ", "HUMAITÁ", "IPIXUNA", "IRANDUBA", "ITACOATIARA", "ITAMARATI",
    "ITAPIRANGA", "JAPURÁ", "JURUÁ", "JUTAÍ", "LÁBREA", "MANACAPURU", "MANAQUIRI",
    "MANAUS", "MANICORÉ", "MARAÃ", "MAUÉS", "NHAMUNDÁ", "NOVA OLINDA DO NORTE",
    "NOVO AIRÃO", "NOVO ARIPUANÃ", "PARINTINS", "PAUINI", "PRESIDENTE FIGUEIREDO",
    "RIO PRETO DA EVA", "SANTA ISABEL DO RIO NEGRO", "SANTO ANTÔNIO DO IÇÁ",
    "SILVES", "SÃO GABRIEL DA CACHOEIRA", "SÃO PAULO DE OLIVENÇA",
    "SÃO SEBASTIÃO DO UATUMÃ", "TABATINGA", "TAPAUÁ", "TEFÉ", "TONANTINS",
    "UARINI", "URUCARÁ", "URUCURITUBA"
]

# Nomes de candidatos (prefixos para busca flexível)
EB_NAME = 'CARLOS EDUARDO DE SOUZA BRAGA'
PT_CANDIDATES = {
    2010: ('DILMA', 'PT'),
    2014: ('DILMA', 'PT'),
    2018: ('HADDAD', 'PT'),
    2022: ('LULA', 'PT')
}
RIGHT_CANDIDATES = {
    2010: ('SERRA', 'Direita'),
    2014: ('AÉCIO', 'Direita'),
    2018: ('BOLSONARO', 'Direita'),
    2022: ('BOLSONARO', 'Direita')
}

# ============================================================================
# 2. CARREGAR DADOS
# ============================================================================

def load_data():
    print("📥 Carregando dados TSE...")

    data = {}

    # ===== DADOS REGIONAIS (Gov/Senador) =====
    for year in [2010, 2014, 2018, 2022]:
        files = {
            2010: 'votacao_secao_2010_AM/votacao_secao_2010_AM.csv',
            2014: 'votacao_secao_2014_AM/votacao_secao_2014_AM.csv',
            2018: 'data/raw/votacao_secao_2018_AM.csv',  # Corrigido: estava em data/raw
            2022: 'votacao_secao_2022_AM/votacao_secao_2022_AM.csv',
        }

        filepath = BASE_PATH / files[year]
        if not filepath.exists():
            # Tentar variante com zip extraído
            alt_filepath = BASE_PATH / files[year].replace('.csv', '')
            if alt_filepath.is_dir():
                alt_filepath = alt_filepath / f"votacao_secao_{year}_AM.csv"
                if alt_filepath.exists():
                    filepath = alt_filepath

        print(f"  {year} (Regional)...", end='')

        if filepath.exists():
            df = pd.read_csv(filepath, delimiter=';', encoding='latin-1', low_memory=False)
            df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
            df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
            df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()

            # Filtrar apenas os 62 municipios
            df = df[df['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()

            data[year] = df
            print(f" ✓ ({len(df):,} registros)")
        else:
            data[year] = pd.DataFrame()
            print(f" ⚠ Arquivo não encontrado")

    # ===== DADOS PRESIDENCIAIS =====
    # 2010 - Arquivo estadual específico
    print(f"  2010 (Presidente AM)...", end='')
    try:
        df_pres = pd.read_csv(
            BASE_PATH / 'presidente_2010_AM_por_secao.csv',
            delimiter=';',
            encoding='latin-1',
            low_memory=False
        )
        df_pres['NM_MUNICIPIO'] = df_pres['NM_MUNICIPIO'].str.strip().str.upper()
        df_pres = df_pres[df_pres['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
        df_pres['NM_VOTAVEL'] = df_pres['NM_VOTAVEL'].str.strip()
        data['2010_pres'] = df_pres
        print(f" ✓ ({len(df_pres):,} registros)")
    except Exception as e:
        data['2010_pres'] = pd.DataFrame()
        print(f" ❌ Erro: {str(e)[:30]}")

    # 2014 - Arquivo nacional filtrado por AM
    print(f"  2014 (Presidente BR)...", end='')
    try:
        df_pres = pd.read_csv(
            BASE_PATH / 'votacao_secao_2014_BR/votacao_secao_2014_BR.csv',
            delimiter=';',
            encoding='latin-1',
            dtype={'SG_UF': str},
            low_memory=False
        )
        df_pres = df_pres[(df_pres['SG_UF'] == 'AM')].copy()
        df_pres['NM_MUNICIPIO'] = df_pres['NM_MUNICIPIO'].str.strip().str.upper()
        df_pres = df_pres[df_pres['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
        df_pres['NM_VOTAVEL'] = df_pres['NM_VOTAVEL'].str.strip()
        data['2014_pres'] = df_pres
        print(f" ✓ ({len(df_pres):,} registros)")
    except Exception as e:
        data['2014_pres'] = pd.DataFrame()
        print(f" ❌ Erro: {str(e)[:30]}")

    # 2018 - Arquivo estadual específico
    print(f"  2018 (Presidente AM)...", end='')
    try:
        df_pres = pd.read_csv(
            BASE_PATH / 'presidente_2018_AM_por_secao.csv',
            delimiter=';',
            encoding='latin-1',
            low_memory=False
        )
        df_pres['NM_MUNICIPIO'] = df_pres['NM_MUNICIPIO'].str.strip().str.upper()
        df_pres = df_pres[df_pres['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
        df_pres['NM_VOTAVEL'] = df_pres['NM_VOTAVEL'].str.strip()
        data['2018_pres'] = df_pres
        print(f" ✓ ({len(df_pres):,} registros)")
    except Exception as e:
        data['2018_pres'] = pd.DataFrame()
        print(f" ❌ Erro: {str(e)[:30]}")

    # 2022 - Arquivo nacional filtrado por AM
    print(f"  2022 (Presidente BR)...", end='')
    try:
        df_pres = pd.read_csv(
            BASE_PATH / 'votacao_secao_2022_BR/votacao_secao_2022_BR.csv',
            delimiter=';',
            encoding='latin-1',
            dtype={'SG_UF': str},
            low_memory=False
        )
        df_pres = df_pres[(df_pres['SG_UF'] == 'AM')].copy()
        df_pres['NM_MUNICIPIO'] = df_pres['NM_MUNICIPIO'].str.strip().str.upper()
        df_pres = df_pres[df_pres['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
        df_pres['NM_VOTAVEL'] = df_pres['NM_VOTAVEL'].str.strip()
        data['2022_pres'] = df_pres
        print(f" ✓ ({len(df_pres):,} registros)")
    except Exception as e:
        data['2022_pres'] = pd.DataFrame()
        print(f" ❌ Erro: {str(e)[:30]}")

    return data

# ============================================================================
# 3. PROCESSAR
# ============================================================================

def process_data(data):
    print("\n🔧 Processando dados...")

    municipios_data = {mun: {
        'presidente': {},
        'eb': {},
        'indice_nacional': 0,
        'classificacao_nacional': '',
        'indice_eb': 0,
        'classificacao_eb': '',
        'eixo_estrategico': '',
        'eixo_label': '',
        'preditivo_2026': {}
    } for mun in AMAZONAS_62}

    # ===== PRESIDENTE =====
    print("  Agregando Presidente...", end='')
    for year in [2010, 2014, 2018, 2022]:
        df_key = f'{year}_pres'  # Agora todos os anos têm dados presidenciais em _pres
        df = data.get(df_key, pd.DataFrame())

        if df.empty:
            continue

        for mun in AMAZONAS_62:
            df_mun = df[df['NM_MUNICIPIO'] == mun]
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                # PT - Busca flexível pelo primeiro nome
                pt_cand_info = PT_CANDIDATES.get(year)
                if pt_cand_info:
                    pt_search_name = pt_cand_info[0]
                    votos_pt = df_mun[df_mun['NM_VOTAVEL'].str.contains(pt_search_name, case=False, na=False)]['QT_VOTOS'].sum()
                else:
                    votos_pt = 0
                pct_pt = (votos_pt / total_valido) * 100

                # Direita - Busca flexível pelo primeiro nome
                right_cand_info = RIGHT_CANDIDATES.get(year)
                if right_cand_info:
                    right_search_name = right_cand_info[0]
                    votos_right = df_mun[df_mun['NM_VOTAVEL'].str.contains(right_search_name, case=False, na=False)]['QT_VOTOS'].sum()
                else:
                    votos_right = 0
                pct_right = (votos_right / total_valido) * 100

                municipios_data[mun]['presidente'][int(year)] = {
                    'pt': round(pct_pt, 1),
                    'direita': round(pct_right, 1),
                    'margem': round((pct_pt - pct_right) / 100, 3)  # Normalizar para -1 a +1
                }
    print(" ✓")

    # ===== EDUARDO BRAGA =====
    print("  Agregando Eduardo Braga...", end='')

    # Carregar dados de EB (regional elections: Senador ou Governador)
    eb_data = {}

    # 2010 - Senador
    try:
        df_2010_regional = data.get(2010, pd.DataFrame())
        if not df_2010_regional.empty:
            df_2010_eb = df_2010_regional[df_2010_regional['DS_CARGO'].str.upper().str.contains('SENADOR', na=False)].copy()
            eb_data[2010] = df_2010_eb
    except:
        eb_data[2010] = pd.DataFrame()

    # 2014 - Governador
    try:
        df_2014_regional = data.get(2014, pd.DataFrame())
        if not df_2014_regional.empty:
            df_2014_eb = df_2014_regional[df_2014_regional['DS_CARGO'].str.upper().str.contains('GOVERNADOR', na=False)].copy()
            eb_data[2014] = df_2014_eb
    except:
        eb_data[2014] = pd.DataFrame()

    # 2018 - Senador (usar arquivo regional 2018)
    try:
        # Usar dados regionais de 2018 que já foram carregados
        df_2018_regional = data.get(2018, pd.DataFrame())
        if not df_2018_regional.empty:
            df_2018_eb = df_2018_regional[df_2018_regional['DS_CARGO'].str.upper().str.contains('SENADOR', na=False)].copy()
            eb_data[2018] = df_2018_eb
        else:
            eb_data[2018] = pd.DataFrame()
    except:
        eb_data[2018] = pd.DataFrame()

    # 2022 - Governador
    try:
        df_2022_regional = data.get(2022, pd.DataFrame())
        if not df_2022_regional.empty:
            df_2022_eb = df_2022_regional[df_2022_regional['DS_CARGO'].str.upper().str.contains('GOVERNADOR', na=False)].copy()
            eb_data[2022] = df_2022_eb
    except:
        eb_data[2022] = pd.DataFrame()

    # Processar EB
    for year in [2010, 2014, 2018, 2022]:
        df = eb_data.get(year, pd.DataFrame())

        if df.empty:
            continue

        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()

        # Buscar EB flexivelmente
        if df[df['NM_VOTAVEL'].str.contains('EDUARDO', case=False, na=False)].empty:
            continue

        # Buscar EB flexivelmente (CARLOS EDUARDO ou similar)
        votos_eb_estado = df[df['NM_VOTAVEL'].str.contains('EDUARDO', case=False, na=False)]['QT_VOTOS'].sum()
        total_valido_estado = df[~df['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        pct_eb_estado = (votos_eb_estado / total_valido_estado * 100) if total_valido_estado > 0 else 0

        for mun in AMAZONAS_62:
            df_mun = df[df['NM_MUNICIPIO'] == mun]
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                votos_eb = df_mun[df_mun['NM_VOTAVEL'].str.contains('EDUARDO', case=False, na=False)]['QT_VOTOS'].sum()
                pct_eb = (votos_eb / total_valido) * 100
                diff = pct_eb - pct_eb_estado

                municipios_data[mun]['eb'][int(year)] = {
                    'votos_pct': round(pct_eb, 1),
                    'media_estado': round(pct_eb_estado, 1),
                    'diff': round(diff / 100, 3)  # Normalizar para -1 a +1
                }
    print(" ✓")

    return municipios_data

# ============================================================================
# 4. CALCULAR ÍNDICES
# ============================================================================

def calculate_indices(municipios_data):
    print("  Calculando índices...", end='')

    for mun, data in municipios_data.items():
        # Índice Nacional
        margins = [
            (data['presidente'].get(y, {}).get('margem', 0) * w)
            for y, w in [(2010, 0.10), (2014, 0.15), (2018, 0.30), (2022, 0.45)]
        ]
        in_index = sum(margins)

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

        data['indice_nacional'] = round(in_index, 3)
        data['classificacao_nacional'] = class_nat

        # Índice EB
        diffs = [
            (data['eb'].get(y, {}).get('diff', 0) * w)
            for y, w in [(2010, 0.10), (2014, 0.15), (2018, 0.30), (2022, 0.45)]
        ]
        ieb_index = sum(diffs)

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

        data['indice_eb'] = round(ieb_index, 3)
        data['classificacao_eb'] = class_eb

        # Eixo E1-E6
        is_manaus = mun == 'MANAUS'
        if in_index > 0:
            eixo = 'E2' if is_manaus else 'E1'
            label = 'Lulismo Manaus' if is_manaus else 'Lulismo Interior'
        elif in_index > -0.10:
            eixo = 'E4' if is_manaus else 'E3'
            label = 'Amazonas Manaus' if is_manaus else 'Amazonas Interior'
        else:
            eixo = 'E6' if is_manaus else 'E5'
            label = 'Bolsonarismo Manaus' if is_manaus else 'Bolsonarismo Interior'

        data['eixo_estrategico'] = eixo
        data['eixo_label'] = label

    print(" ✓")

    # ===== CALCULAR PREDITIVO COM PERCENTIS =====
    # Usar índice_eb para classificar municípios em 5 categorias
    ieb_values = [(mun, data['indice_eb']) for mun, data in municipios_data.items()]
    ieb_values.sort(key=lambda x: x[1])

    for i, (mun, ieb) in enumerate(ieb_values):
        quintile = i // (len(ieb_values) // 5)
        if quintile >= 5:
            quintile = 4

        eb_data = municipios_data[mun].get('eb', {})
        recent_diff = eb_data.get(2022, {}).get('diff', 0)

        # Calcular score dentro do quintil (0-1)
        quintile_pos = (i % (len(ieb_values) // 5)) / (len(ieb_values) // 5 + 1)

        if quintile == 4:  # Top 20%
            pred_class = 'SEGURO EB'
            score = 0.75 + quintile_pos * 0.25
        elif quintile == 3:
            pred_class = 'COMPETITIVO PRÓ-EB'
            score = 0.55 + quintile_pos * 0.20
        elif quintile == 2:
            pred_class = 'BATTLEGROUND'
            score = 0.40 + quintile_pos * 0.15
        elif quintile == 1:
            pred_class = 'COMPETITIVO CONTRA'
            score = 0.25 + quintile_pos * 0.15
        else:
            pred_class = 'DIFÍCIL'
            score = 0.0 + quintile_pos * 0.25

        municipios_data[mun]['preditivo_2026'] = {
            'score': round(min(score, 1), 3),
            'classificacao': pred_class,
            'tendencia': 'positiva' if recent_diff > 0 else 'negativa',
            'volatilidade': round(np.std([eb_data.get(y, {}).get('diff', 0) for y in [2010, 2014, 2018, 2022]]), 3)
        }

# ============================================================================
# 5. SALVAR
# ============================================================================

def save_data(municipios_data):
    print("\n💾 Salvando dados...")

    # ===== CALCULAR DADOS ESTADUAIS (agregados dos 62 municípios) =====
    estado_data = {
        'presidente': {},
        'eb': {},
        'indice_nacional': 0,
        'classificacao_nacional': '',
        'indice_eb': 0,
        'classificacao_eb': '',
        'eixo_estrategico': 'ESTADO',
        'eixo_label': 'Agregado Estadual',
        'preditivo_2026': {}
    }

    # Calcular presidente estadual
    for year in [2010, 2014, 2018, 2022]:
        pt_pct_sum = 0
        right_pct_sum = 0
        count = 0

        for mun, data in municipios_data.items():
            year_key = str(year)  # As chaves são strings
            if year_key in data['presidente']:
                pt_pct_sum += data['presidente'][year_key]['pt']
                right_pct_sum += data['presidente'][year_key]['direita']
                count += 1

        if count > 0:
            estado_data['presidente'][str(year)] = {
                'pt': round(pt_pct_sum / count, 1),
                'direita': round(right_pct_sum / count, 1),
                'margem': round((pt_pct_sum - right_pct_sum) / count / 100, 3)
            }

    # Calcular EB estadual
    for year in [2010, 2014, 2018, 2022]:
        eb_pct_sum = 0
        count = 0

        for mun, data in municipios_data.items():
            if year in data['eb']:
                eb_pct_sum += data['eb'][year]['votos_pct']
                count += 1

        if count > 0:
            media_estado = eb_pct_sum / count
            estado_data['eb'][str(year)] = {
                'votos_pct': round(media_estado, 1),
                'media_estado': round(media_estado, 1),
                'diff': 0  # Diff é zero pois é a média
            }

    # Calcular índices estaduais (igual aos municípios)
    margins = [
        (estado_data['presidente'].get(str(y), {}).get('margem', 0) * w)
        for y, w in [(2010, 0.10), (2014, 0.15), (2018, 0.30), (2022, 0.45)]
    ]
    in_index = sum(margins)

    if in_index > 0.20:
        estado_data['classificacao_nacional'] = 'Bastião Lulista'
    elif in_index > 0.05:
        estado_data['classificacao_nacional'] = 'Tendência Lulista'
    elif in_index >= -0.05:
        estado_data['classificacao_nacional'] = 'Swing'
    elif in_index >= -0.20:
        estado_data['classificacao_nacional'] = 'Tendência Bolsonarista'
    else:
        estado_data['classificacao_nacional'] = 'Bastião Bolsonarista'

    estado_data['indice_nacional'] = round(in_index, 3)

    # Calcular índice EB estadual
    diffs = [
        (estado_data['eb'].get(str(y), {}).get('diff', 0) * w)
        for y, w in [(2010, 0.10), (2014, 0.15), (2018, 0.30), (2022, 0.45)]
    ]
    ieb_index = sum(diffs)

    if ieb_index > 0.10:
        estado_data['classificacao_eb'] = 'Bastião Eduardista'
    elif ieb_index > 0.03:
        estado_data['classificacao_eb'] = 'Tendência Eduardista'
    elif ieb_index >= -0.05:
        estado_data['classificacao_eb'] = 'Swing'
    elif ieb_index >= -0.15:
        estado_data['classificacao_eb'] = 'Tendência Anti-EB'
    else:
        estado_data['classificacao_eb'] = 'Bastião Anti-EB'

    estado_data['indice_eb'] = round(ieb_index, 3)

    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'state': 'Amazonas',
            'total_municipalities': len(municipios_data),
            'elections': [2010, 2014, 2018, 2022],
            'note': 'Apenas 62 municípios oficiais do Amazonas'
        },
        'estado': estado_data,
        'municipios': municipios_data
    }

    # data.js
    with open(OUTPUT_PATH / 'data.js', 'w', encoding='utf-8') as f:
        f.write('const DASHBOARD_DATA = ')
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write(';\n')

    # data.json
    with open(OUTPUT_PATH / 'data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  ✓ {OUTPUT_PATH / 'data.js'}")
    print(f"  ✓ {OUTPUT_PATH / 'data.json'}")

    # Estatísticas
    classes_nat = {}
    classes_eb = {}
    eixos = {}
    pred_classes = {}

    for mun, data in municipios_data.items():
        classes_nat[data['classificacao_nacional']] = classes_nat.get(data['classificacao_nacional'], 0) + 1
        classes_eb[data['classificacao_eb']] = classes_eb.get(data['classificacao_eb'], 0) + 1
        eixos[data['eixo_estrategico']] = eixos.get(data['eixo_estrategico'], 0) + 1
        pred_classes[data['preditivo_2026']['classificacao']] = pred_classes.get(data['preditivo_2026']['classificacao'], 0) + 1

    print("\n📊 ESTATÍSTICAS:")
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

# ============================================================================
# 6. MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 PIPELINE CORRIGIDO - 62 MUNICÍPIOS AMAZONAS")
    print("="*70 + "\n")

    data = load_data()
    municipios_data = process_data(data)
    calculate_indices(municipios_data)
    save_data(municipios_data)

    print("\n" + "="*70)
    print("✅ PROCESSAMENTO CONCLUÍDO")
    print("="*70 + "\n")
