---
description: Gera Word A4 no layout navy (faixa no cabeçalho/rodapé, tabelas zebradas) a partir de um Markdown de especificação.
---

# gerar-word

Converta o Markdown indicado em Word (`.docx`) com o layout Poly usado nas specs da Integração Pac (faixa navy, tabelas zebradas, blocos de código).

Argumentos: `$ARGUMENTS` — caminho do `.md`; opcionalmente o `.docx` de saída e/ou `--header` / `--title` / `--version`.

## Obrigatório

Leia e siga a skill `gerar-word`:

`~/CursorRulesSkills/skills/gerar-word/SKILL.md`

Execute **somente** o script dessa skill:

```bash
python3 ~/CursorRulesSkills/skills/gerar-word/scripts/md_to_docx.py
```

## Proibido

- Recriar `_md_to_docx.py` (ou equivalente) dentro do projeto
- Alterar o Markdown só para caber no Word, salvo o usuário pedir
- Commitar o `.docx` sem o usuário pedir

## Entrada

1. Se `$ARGUMENTS` tiver um `.md`, use esse arquivo.
2. Se também houver um caminho `.docx`, use como destino.
3. Sem argumentos: o `.md` da conversa, o arquivo aberto, ou pergunte o caminho.

## Saída

Informe o caminho do `.docx`. Não invente número de páginas.
