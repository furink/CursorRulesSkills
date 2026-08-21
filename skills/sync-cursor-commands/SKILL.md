---
name: sync-cursor-commands
description: Copies global Cursor slash commands from ~/CursorRulesSkills/commands to C:\Users\furin\.cursor\commands (Windows). Use after editing command files in CursorRulesSkills, when the user asks to sync commands, copiar commands, or when slash commands in chat would otherwise stay stale on Windows/WSL.
---

# Sync Cursor commands (WSL → Windows)

O Cursor no Windows lê `C:\Users\furin\.cursor\commands`, não o `~/.cursor/commands` do WSL. Depois de criar, editar ou apagar um `.md` em `~/CursorRulesSkills/commands`, sincronize.

## Instruções

1. Execute o script (não reescreva o `cp` na mão):

```bash
bash ~/CursorRulesSkills/skills/sync-cursor-commands/scripts/sync.sh
```

2. Confirme a listagem de `.md` no destino.
3. Avise para fazer **Reload Window** (`Ctrl+Shift+P` → `Developer: Reload Window`) se o menu `/` ainda mostrar a versão antiga.

Não copie outros diretórios (`rules/`, `skills/`). Não altere o conteúdo dos commands — só espelhe os arquivos.
