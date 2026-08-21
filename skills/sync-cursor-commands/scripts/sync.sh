#!/usr/bin/env bash
set -euo pipefail

SRC="${HOME}/CursorRulesSkills/commands"
DEST="/mnt/c/Users/furin/.cursor/commands"

if [ ! -d "$SRC" ]; then
  echo "fonte inexistente: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -a "$SRC"/*.md "$DEST/"

for f in "$DEST"/*.md; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  if [ ! -f "$SRC/$base" ]; then
    rm -f "$f"
  fi
done

echo "sincronizado $SRC -> $DEST"
ls -1 "$DEST"/*.md
