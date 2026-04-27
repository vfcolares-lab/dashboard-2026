#!/bin/bash

# 🎯 RADAR ELEITORAL AM 2026
# Script para iniciar o dashboard

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🎯 RADAR ELEITORAL AMAZONAS 2026"
echo "=================================="
echo ""
echo "📁 Diretório: $DIR"
echo ""
echo "Opções:"
echo "  1) Abrir no navegador (Mac)"
echo "  2) Iniciar servidor HTTP (port 8000)"
echo ""
read -p "Escolha uma opção (1 ou 2): " choice

case $choice in
  1)
    echo "🌐 Abrindo dashboard no navegador..."
    open "$DIR/index.html"
    ;;
  2)
    echo "🚀 Iniciando servidor em http://localhost:8000"
    echo ""
    echo "Pressione Ctrl+C para parar"
    cd "$DIR"
    python3 -m http.server 8000
    ;;
  *)
    echo "❌ Opção inválida"
    exit 1
    ;;
esac
