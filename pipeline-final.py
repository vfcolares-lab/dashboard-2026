#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIPELINE FINAL - Dados completos com Presidencial + Regional
Carrega dados de Presidente de arquivos separados + dados regionais
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

# Nomes de candidatos (EXATOS conforme aparecem nos CSVs com encoding)
EB_NAME = 'CARLOS EDUARDO DE SOUZA BRAGA'
PT_CANDIDATES = {
    2010: 'DILMA VANA ROUSSEFF',
    2014: 'DILMA VANA ROUSSEFF',
    2018: 'FERNANDO HADDAD',
    2022: 'LUIZ INÁCIO LULA DA SILVA'
}
RIGHT_CANDIDATES = {
    2010: 'JOSÃ SERRA',  # Encoding CSVs - é JOSÉ SERRA mas aparece com til
    2014: 'AÉCIO NEVES',
    2018: 'JAIR MESSIAS BOLSONARO',
    2022: 'JAIR MESSIAS BOLSONARO'
}

# ============================================================================
# 2. CARREGAR DADOS
# ============================================================================

def load_data():
    print("📥 Carregando dados TSE...")

    data = {}

    # DADOS REGIONAIS (Gov/Senado para 2010-2018, 2022)
    regional_files = {
        2010: 'votacao_secao_2010_AM/votacao_secao_2010_AM.csv',
        2014: 'votacao_secao_2014_AM/votacao_secao_2014_AM.csv',
        2018: 'data/raw/votacao_secao_2018_AM.csv',
        2022: 'votacao_secao_2022_AM/votacao_secao_2022_AM.csv',
    }

    # DADOS PRESIDENCIAIS (separados)
    pres_files = {
        2010: 'presidente_2010_AM_por_secao.csv',
        2014: 'votacao_secao_2014_BR/votacao_secao_2014_BR.csv',  # Filtro por AM (Brasil)
        2018: 'presidente_2018_AM_por_secao.csv',
        2022: 'votacao_secao_2022_BR/votacao_secao_2022_BR.csv',  # Filtro por AM
    }

    for year in [2010, 2014, 2018, 2022]:
        print(f"  {year}...", end='')

        # Carregar dados regionais
        regional_path = BASE_PATH / regional_files[year]
        if regional_path.exists():
            df_regional = pd.read_csv(regional_path, delimiter=';', encoding='latin-1', low_memory=False)
            df_regional['NM_MUNICIPIO'] = df_regional['NM_MUNICIPIO'].str.strip().str.upper()
            df_regional['NM_VOTAVEL'] = df_regional['NM_VOTAVEL'].str.strip()
            df_regional['DS_CARGO'] = df_regional['DS_CARGO'].str.strip().str.upper()
            df_regional = df_regional[df_regional['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
            data[f'{year}_regional'] = df_regional
        else:
            data[f'{year}_regional'] = pd.DataFrame()

        # Carregar dados presidenciais
        pres_path = pres_files[year]
        if pres_path:
            pres_full_path = BASE_PATH / pres_path
            if pres_full_path.exists():
                if year in [2014, 2022]:
                    # 2014 e 2022 são nacionais, filtrar por AM
                    df_pres = pd.read_csv(pres_full_path, delimiter=';', encoding='latin-1', dtype={'SG_UF': str}, low_memory=False)
                    df_pres = df_pres[df_pres['SG_UF'] == 'AM'].copy()
                else:
                    df_pres = pd.read_csv(pres_full_path, delimiter=';', encoding='latin-1', low_memory=False)

                df_pres['NM_MUNICIPIO'] = df_pres['NM_MUNICIPIO'].str.strip().str.upper()
                df_pres['NM_VOTAVEL'] = df_pres['NM_VOTAVEL'].str.strip()
                df_pres = df_pres[df_pres['NM_MUNICIPIO'].isin(AMAZONAS_62)].copy()
                data[f'{year}_pres'] = df_pres
            else:
                data[f'{year}_pres'] = pd.DataFrame()
        else:
            data[f'{year}_pres'] = pd.DataFrame()

        count = len(data.get(f'{year}_regional', pd.DataFrame()))
        count_pres = len(data.get(f'{year}_pres', pd.DataFrame()))
        print(f" ✓ ({count} regional, {count_pres} presidencial)")

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

    # ===== PRESIDENTE (DADOS PRESIDENCIAIS) =====
    print("  Agregando Presidente...", end='')
    for year in [2010, 2014, 2018, 2022]:
        df = data.get(f'{year}_pres', pd.DataFrame())

        if df.empty:
            continue

        for mun in AMAZONAS_62:
            df_mun = df[df['NM_MUNICIPIO'] == mun]
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                # PT
                pt_cand = PT_CANDIDATES.get(year)
                votos_pt = 0
                if pt_cand:
                    # Procurar por parte do nome (mais robusto para encoding)
                    pt_first = pt_cand.split()[0]
                    votos_pt = df_mun[df_mun['NM_VOTAVEL'].str.contains(pt_first, case=False, na=False)]['QT_VOTOS'].sum()
                pct_pt = (votos_pt / total_valido) * 100

                # Direita
                right_cand = RIGHT_CANDIDATES.get(year)
                votos_right = 0
                if right_cand:
                    # Procurar por parte do nome (mais robusto para encoding)
                    right_first = right_cand.split()[0]
                    votos_right = df_mun[df_mun['NM_VOTAVEL'].str.contains(right_first, case=False, na=False)]['QT_VOTOS'].sum()
                pct_right = (votos_right / total_valido) * 100

                municipios_data[mun]['presidente'][year] = {
                    'pt': round(pct_pt, 1),
                    'direita': round(pct_right, 1),
                    'margem': round((pct_pt - pct_right) / 100, 3)
                }
    print(" ✓")

    # ===== EDUARDO BRAGA (DADOS REGIONAIS - Governador/Senador) =====
    print("  Agregando Eduardo Braga...", end='')
    for year in [2010, 2014, 2018, 2022]:
        df = data.get(f'{year}_regional', pd.DataFrame())

        if df.empty or df[df['NM_VOTAVEL'] == EB_NAME].empty:
            continue

        # Calcular média estadual
        votos_eb_estado = df[df['NM_VOTAVEL'] == EB_NAME]['QT_VOTOS'].sum()
        total_valido_estado = df[~df['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        pct_eb_estado = (votos_eb_estado / total_valido_estado * 100) if total_valido_estado > 0 else 0

        for mun in AMAZONAS_62:
            df_mun = df[df['NM_MUNICIPIO'] == mun]
            total_valido = df_mun[~df_mun['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if total_valido > 0:
                votos_eb = df_mun[df_mun['NM_VOTAVEL'] == EB_NAME]['QT_VOTOS'].sum()
                pct_eb = (votos_eb / total_valido) * 100
                diff = pct_eb - pct_eb_estado

                municipios_data[mun]['eb'][year] = {
                    'votos_pct': round(pct_eb, 1),
                    'media_estado': round(pct_eb_estado, 1),
                    'diff': round(diff / 100, 3)
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

        if in_index > 0.20:
            class_nat = 'Bastião Lulista'
        elif in_index > 0.05:
            class_nat = 'Tendência Lulista'
        elif in_index >= -0.05:
            class_nat = 'Swing'
        elif in_index >= -0.20:
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

        if ieb_index > 0.10:
            class_eb = 'Bastião Eduardista'
        elif ieb_index > 0.03:
            class_eb = 'Tendência Eduardista'
        elif ieb_index >= -0.05:
            class_eb = 'Swing'
        elif ieb_index >= -0.10:
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
    ieb_values = [(mun, data['indice_eb']) for mun, data in municipios_data.items()]
    ieb_values.sort(key=lambda x: x[1])

    for i, (mun, ieb) in enumerate(ieb_values):
        quintile = i // (len(ieb_values) // 5)
        if quintile >= 5:
            quintile = 4

        eb_data = municipios_data[mun].get('eb', {})
        recent_diff = eb_data.get(2022, {}).get('diff', 0)
        quintile_pos = (i % (len(ieb_values) // 5)) / (len(ieb_values) // 5 + 1)

        if quintile == 4:
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

    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '2.0',
            'state': 'Amazonas',
            'total_municipalities': len(municipios_data),
            'elections': [2010, 2014, 2018, 2022],
            'note': 'Dados completos com Presidencial + Regional'
        },
        'municipios': municipios_data
    }

    with open(OUTPUT_PATH / 'data.js', 'w', encoding='utf-8') as f:
        f.write('const DASHBOARD_DATA = ')
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write(';\n')

    with open(OUTPUT_PATH / 'data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  ✓ {OUTPUT_PATH / 'data.js'}")
    print(f"  ✓ {OUTPUT_PATH / 'data.json'}")

    # Estatísticas
    classes_nat = {}
    for mun, data in municipios_data.items():
        classes_nat[data['classificacao_nacional']] = classes_nat.get(data['classificacao_nacional'], 0) + 1

    print("\n📊 VERIFICAÇÃO FINAL:")
    for cls, count in sorted(classes_nat.items()):
        print(f"  {cls}: {count}")

# ============================================================================
# 6. MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 PIPELINE FINAL - DADOS COMPLETOS")
    print("="*70 + "\n")

    data = load_data()
    municipios_data = process_data(data)
    calculate_indices(municipios_data)
    save_data(municipios_data)

    print("\n" + "="*70)
    print("✅ PROCESSAMENTO CONCLUÍDO")
    print("="*70 + "\n")
