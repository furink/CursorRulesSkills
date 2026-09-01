---
description: Gera PDF A4 no layout navy (faixa no cabeçalho/rodapé, DejaVu, tabelas zebradas) a partir de um Markdown de especificação.
---

# gerar-pdf

Converta o Markdown indicado em PDF com o layout Poly usado nas specs da Integração Pac (faixa navy, DejaVu, tabelas zebradas, blocos de código).

Argumentos: `$ARGUMENTS` — caminho do `.md`; opcionalmente o `.pdf` de saída e/ou `--header` / `--title` / `--version`.

## Obrigatório

Leia e siga a skill `gerar-pdf`:

`~/CursorRulesSkills/skills/gerar-pdf/SKILL.md`

Execute **somente** o script dessa skill:

```bash
python3 ~/CursorRulesSkills/skills/gerar-pdf/scripts/md_to_pdf.py
```

## Proibido

- Recriar `_md_to_pdf.py` (ou equivalente) dentro do projeto
- Alterar o Markdown só para caber no PDF, salvo o usuário pedir
- Commitar o PDF sem o usuário pedir

## Entrada

1. Se `$ARGUMENTS` tiver um `.md`, use esse arquivo.
2. Se também houver um caminho `.pdf`, use como destino.
3. Sem argumentos: o `.md` da conversa, o arquivo aberto, ou pergunte o caminho.

## Saída

Informe o caminho do PDF e o número de páginas. Apague qualquer PNG de preview.
