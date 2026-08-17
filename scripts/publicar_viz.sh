#!/usr/bin/env bash
# Builda o Kedro-Viz estático e copia o resultado pra docs/, na raiz do repo,
# de onde o GitHub Pages publica (Settings > Pages > Deploy from a branch >
# main / docs). Rode isso localmente, revise o conteúdo de docs/, e faça
# commit + push como parte do seu fluxo normal.
#
# Antes de publicar: confirme que o build não embute prévia de linhas dos
# datasets (licença CC BY-NC-SA do Olist — ver PLANO.md secao 3.0). No
# Kedro-Viz 12.4 o build padrão não embute, mas reconfira se a versão mudar.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJETO="$RAIZ/projeto/olist_analytics"
DOCS="$RAIZ/docs"

cd "$PROJETO"
kedro viz build

rm -rf "$DOCS"
mkdir -p "$DOCS"
cp -r "$PROJETO/build/." "$DOCS/"
touch "$DOCS/.nojekyll"

echo "Build copiado para $DOCS"
echo "Revise o conteúdo, depois: git add docs && git commit && git push"
