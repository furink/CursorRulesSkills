---
description: Gera Excel (.xlsx) no layout navy (cabeçalho, zebrado, filtro, Legenda, P0–P3) a partir de um CSV ou de tabelas Markdown.
---

# gerar-xlsx

Converta a lista CSV (ou as tabelas de um Markdown) em Excel com o layout Poly usado em `pedido-apis-erp-protheus-campos-restantes.xlsx` (cabeçalho navy, linhas zebradas, filtro, aba Legenda).

Argumentos: `$ARGUMENTS` — caminho do `.csv` ou `.md`; opcionalmente o `.xlsx` de saída e/ou `--header` / `--title` / `--version`.

## Obrigatório

Leia e siga a skill `gerar-xlsx`:

`~/CursorRulesSkills/skills/gerar-xlsx/SKILL.md`

Execute **somente** o script dessa skill:

```bash
python3 ~/CursorRulesSkills/skills/gerar-xlsx/scripts/csv_to_xlsx.py
```

## Proibido

- Recriar `_csv_to_xlsx.py` (ou equivalente) dentro do projeto
- Alterar o CSV/Markdown só para caber no Excel, salvo o usuário pedir
- Commitar o `.xlsx` sem o usuário pedir

## Entrada

1. Se `$ARGUMENTS` tiver um `.csv` ou `.md`, use esse arquivo.
2. Se também houver um caminho `.xlsx`, use como destino.
3. Sem extensão: prefira o `.csv` com o mesmo stem; depois o `.md`.
4. Sem argumentos: o `.csv`/`.md` da conversa, o arquivo aberto, ou pergunte o caminho.

## Saída

Informe o caminho do `.xlsx`, o número de linhas da aba de dados e os nomes das abas.
