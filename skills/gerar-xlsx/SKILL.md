---
name: gerar-xlsx
description: >-
  Converts CSV lists (or Markdown GFM tables) to Excel (.xlsx) with the Poly
  navy layout (header fill, zebra rows, frozen header, autofilter, optional
  Legenda sheet, P0–P3 coloring). Use when the user runs /gerar-xlsx, asks to
  gerar Excel/xlsx, exportar csv para xlsx, or wants the same spreadsheet
  layout as pedido-apis-erp-protheus-campos-restantes.xlsx.
---

# gerar-xlsx

Gera Excel (`.xlsx`) no layout navy das listas Poly: cabeçalho navy, linhas zebradas, filtro, primeira linha congelada, aba Legenda, prioridade P0–P3 colorida.

## Quando usar

- Usuário pediu `/gerar-xlsx`, “gera o Excel”, “versão em xlsx” de um `.csv` (ou de tabelas de um `.md`)
- Precisa do mesmo visual de `docs/project_docs/em_implementacao/pedido-apis-erp-protheus-campos-restantes.xlsx`

## Regras

1. **Execute o script desta skill.** Não recrie `_csv_to_xlsx.py` (ou equivalente) dentro do projeto.
2. **Não altere o CSV/Markdown** só para gerar o Excel, salvo o usuário pedir.
3. Destino default: mesmo caminho da origem, extensão `.xlsx` (sobrescreve se já existir).
4. CSV do portal usa `;` (UTF-8). O script detecta `;` vs `,`.
5. Não commite o `.xlsx` a menos que o usuário peça.

## Pré-requisitos

```bash
python3 -c "import openpyxl"
```

Se falhar: `python3 -m pip install -r ~/CursorRulesSkills/skills/gerar-xlsx/requirements.txt`

## Script

```bash
python3 ~/CursorRulesSkills/skills/gerar-xlsx/scripts/csv_to_xlsx.py INPUT.csv [OUTPUT.xlsx] \
  [--title "..."] [--header "..."] [--subject "..."] [--author Poly] [--version 0.1] \
  [--sheet "Dados"] [--delimiter ";"] [--no-legend]
```

Entrada também pode ser `.md` (todas as tabelas GFM viram abas).

O script imprime um JSON: `output`, `sheets`, `rows`, `title`, `header`, `version`.

### Inferência (se o usuário não passar flags)

| Campo | Default |
|---|---|
| `title` | H1 do `.md` irmão / do próprio `.md`; senão o stem do arquivo |
| `header` | `{author} — {título com — virando ·}` |
| `version` | Campo `**Versão:**` do Markdown irmão ou do `.md` |
| `author` | `Poly` |
| `output` | `INPUT` com `.xlsx` |
| `sheet` | `Dados` (CSV) ou o heading anterior à tabela (Markdown) |

`$ARGUMENTS` do comando: caminho do `.csv` ou `.md`. Se vier também um `.xlsx`, use como destino. Sem extensão, prefira o `.csv` com o mesmo stem; depois o `.md`. Sem argumentos: o `.csv`/`.md` da conversa, o arquivo aberto, ou pergunte o caminho.

`--header` só quando o título for longo demais para o cabeçalho de impressão.

## Depois de gerar

1. Confira o JSON (`output` no path certo, `rows` > 0).
2. Responda o caminho do `.xlsx` e quantas linhas/abas.
3. Não deixe gerador one-off no repo.

## Fora de escopo

Gráficos, macros, `.xls` antigo, várias planilhas de origem num único comando. Imagens no Markdown são ignoradas.
