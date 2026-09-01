---
name: gerar-pdf
description: >-
  Converts Markdown specs to A4 PDFs with the Poly navy layout (header/footer
  bars, DejaVu, zebra tables, code blocks). Use when the user runs /gerar-pdf,
  asks to gerar PDF, exportar markdown para PDF, or wants the same layout as the
  Pac integration spec PDFs.
---

# gerar-pdf

Gera PDF A4 no layout das specs Pac (faixa navy no topo e rodapé, DejaVu, tabelas com cabeçalho navy e linhas zebradas, blocos de código cinza).

## Quando usar

- Usuário pediu `/gerar-pdf` ou “gera o PDF” de um `.md`
- Precisa do mesmo visual dos PDFs em `docs/project_docs/em_implementacao/integracao-pac-*.pdf`

## Regras

1. **Execute o script desta skill.** Não recrie `_md_to_pdf.py` no projeto.
2. **Não altere o Markdown** só para gerar o PDF, salvo o usuário pedir.
3. Destino default: mesmo caminho do `.md`, extensão `.pdf` (sobrescreve se já existir).
4. Parágrafos com “handoff” saem do PDF por padrão (notas internas). Use `--keep-handoff` só se pedirem.
5. Não commite o PDF a menos que o usuário peça.

## Pré-requisitos

```bash
python3 -c "import markdown, reportlab"
```

Se falhar: `python3 -m pip install -r ~/CursorRulesSkills/skills/gerar-pdf/requirements.txt`

Fonte: DejaVu em `/usr/share/fonts/truetype/dejavu` (`fonts-dejavu-core`).

## Script

```bash
python3 ~/CursorRulesSkills/skills/gerar-pdf/scripts/md_to_pdf.py INPUT.md [OUTPUT.pdf] \
  [--title "..."] [--header "..."] [--subject "..."] [--author Poly] [--version 0.1] \
  [--keep-handoff]
```

O script imprime um JSON: `output`, `pages`, `title`, `header`, `version`.

### Inferência (se o usuário não passar flags)

| Campo | Default |
|---|---|
| `title` | Primeiro H1 (`# ...`) |
| `header` | `{author} — {título com — virando ·}` |
| `version` | Campo `**Versão:**` do Markdown |
| `author` | `Poly` |
| `output` | `INPUT` com `.pdf` |

`$ARGUMENTS` do comando: caminho do `.md`. Se vier também um `.pdf`, use como destino. Se não houver argumento, use o `.md` da conversa / arquivo aberto.

`--header` só quando o H1 for longo demais para a faixa (ex.: Etapa 2 usou “documentos e serviços”).

## Depois de gerar

1. Confira o JSON (páginas > 0, path certo).
2. Opcional — primeira página:

```bash
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r120 -sOutputFile=/tmp/pdf-preview.png OUTPUT.pdf
```

3. Apague PNG de preview. Não deixe gerador one-off no repo.
4. Responda o caminho do PDF e o número de páginas.

## Fora de escopo

Imagens, Markdown aninhado complexo, HTML rico. Se o `.md` depender disso, avise e gere o que o layout cobre (títulos, listas, tabelas, código, ênfase).
