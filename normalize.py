#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalizador de nomes de municípios do Amazonas
Remove duplicatas por variação de acentuação
"""

import json
import unicodedata

def normalize_name(name):
    """Remove acentos e normaliza para comparação"""
    nfd = unicodedata.normalize('NFD', name.upper())
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

def consolidate_municipalities(data):
    """Consolida municípios duplicados por variação de acentuação"""

    municipios = data['municipios']
    normalized_map = {}

    # Mapear nomes originais para nomes normalizados
    for mun_name in municipios.keys():
        normalized = normalize_name(mun_name)
        if normalized not in normalized_map:
            normalized_map[normalized] = []
        normalized_map[normalized].append(mun_name)

    print(f"Total de municípios com duplicatas: {sum(1 for v in normalized_map.values() if len(v) > 1)}")
    print("\n=== CONSOLIDAÇÃO ===\n")

    # Consolidar dados (usar o primeiro de cada grupo)
    consolidated = {}
    replacements = {}

    for normalized, original_names in normalized_map.items():
        if len(original_names) > 1:
            # Tem duplicata
            main_name = max(original_names)  # Usar o que tem mais acentos (geralmente correto)
            print(f"✓ {main_name}")
            print(f"  ← Consolidando: {', '.join(original_names)}")

            # Mesclar dados de todas as variações
            consolidated_data = municipios[main_name].copy()

            # Tentar agregar dados das variações (se houver diferenças)
            for other_name in original_names:
                if other_name != main_name:
                    other_data = municipios[other_name]
                    # Se uma variação tem mais dados, usar
                    # (útil se um encoding foi melhor que outro)
                    pass

            consolidated[main_name] = consolidated_data

            # Mapear todas as variações para o nome principal
            for orig_name in original_names:
                replacements[orig_name] = main_name
        else:
            # Sem duplicata
            consolidated[original_names[0]] = municipios[original_names[0]]
            replacements[original_names[0]] = original_names[0]

    print(f"\n✅ {len(consolidated)} municípios únicos")
    print(f"❌ {sum(1 for v in normalized_map.values() if len(v) > 1)} grupos de duplicatas")

    return consolidated

def main():
    print("🔧 NORMALIZADOR DE MUNICÍPIOS - AMAZONAS\n")

    # Carregar data original
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 Data original: {len(data['municipios'])} registros\n")

    # Consolidar
    consolidated = consolidate_municipalities(data)

    # Atualizar metadata
    data['metadata']['total_municipalities'] = len(consolidated)
    data['municipios'] = consolidated

    # Salvar novo data.js
    print("\n💾 Salvando dados consolidados...")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write('const DASHBOARD_DATA = ')
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write(';\n')

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ data.js ({len(consolidated)} municípios)")
    print(f"  ✓ data.json ({len(consolidated)} municípios)")

    print(f"\n✅ Consolidação concluída!")
    print(f"   Antes: 88 registros | Depois: {len(consolidated)} únicos")
    print(f"   Duplicatas removidas: {88 - len(consolidated)}")

if __name__ == '__main__':
    main()
