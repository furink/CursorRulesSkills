# CursorRulesSkills

Rules, commands e skills pessoais do Cursor, versionados neste repositório.

## Estrutura

- `rules/` — rules compartilhadas (symlink por arquivo em cada projeto: `.cursor/rules/`)
- `commands/` — commands globais (symlink em `~/.cursor/commands/`)
- `skills/` — skills globais (symlink em `~/.cursor/skills/`)

## Como editar

1. Edite os arquivos neste repositório (`~/CursorRulesSkills/`).
2. `git commit` + `git push` para backup.
3. Os symlinks propagam a alteração automaticamente — sem copiar entre projetos.

## Rules e commands específicos de projeto

Ficam como arquivos reais no `.cursor/` do projeto, não neste repo.
