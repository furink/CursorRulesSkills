# CursorRulesSkills

Rules, commands e skills pessoais do Cursor, versionados neste repositório.

## Estrutura

- `rules/` — rules compartilhadas (symlink por arquivo em cada projeto: `.cursor/rules/`)
- `commands/` — commands globais (symlink em `~/.cursor/commands/`)
- `skills/` — skills globais (symlink em `~/.cursor/skills/`)
- `/gerar-pdf` — Markdown → PDF A4 no layout navy (skill `skills/gerar-pdf/`)
- `/gerar-word` — Markdown → Word A4 no layout navy (skill `skills/gerar-word/`)
- `/gerar-xlsx` — CSV (ou tabelas Markdown) → Excel navy, zebrado, Legenda (skill `skills/gerar-xlsx/`)

## Como editar

1. Edite os arquivos neste repositório (`~/CursorRulesSkills/`).
2. `git commit` + `git push` para backup.
3. Rules nos projetos e `~/.cursor` no WSL usam symlink — propagam sozinhas.
4. No Cursor Windows, commands do menu `/` vêm de `C:\Users\furin\.cursor\commands`. Depois de alterar um command, rode `/sync-cursor-commands` (ou o script `skills/sync-cursor-commands/scripts/sync.sh`) e faça Reload Window.

## Rules e commands específicos de projeto

Ficam como arquivos reais no `.cursor/` do projeto, não neste repo.
