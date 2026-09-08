---
name: gerar-word
description: >-
  Converts Markdown specs to A4 Word (.docx) with the Poly navy layout
  (header/footer bars, zebra tables, code blocks). Use when the user runs
  /gerar-word, asks to gerar Word, exportar markdown para Word/docx, or wants
  the same layout as the Pac integration spec PDFs in a .docx.
---

# gerar-word

Gera Word A4 no layout das specs Pac (faixa navy no topo e rodapé, tabelas com cabeçalho navy e linhas zebradas, blocos de código cinza).

## Quando usar

- Usuário pediu `/gerar-word` ou “gera o Word” / “versão em Word” de um `.md`
- Precisa do mesmo visual dos PDFs em `docs/project_docs/em_implementacao/integracao-pac-*.pdf`, em `.docx`

## Regras

1. **Execute o script desta skill.** Não recrie `_md_to_docx.py` no projeto.
2. **Não altere o Markdown** só para gerar o Word, salvo o usuário pedir.
3. Destino default: mesmo caminho do `.md`, extensão `.docx` (sobrescreve se já existir).
4. Parágrafos com “handoff” saem do Word por padrão (notas internas). Use `--keep-handoff` só se pedirem.
5. Não commite o `.docx` a menos que o usuário peça.

## Pré-requisitos

```bash
python3 -c "import markdown, docx"
```

Se falhar: `python3 -m pip install -r ~/CursorRulesSkills/skills/gerar-word/requirements.txt`

## Script

```bash
python3 ~/CursorRulesSkills/skills/gerar-word/scripts/md_to_docx.py INPUT.md [OUTPUT.docx] \
  [--title "..."] [--header "..."] [--subject "..."] [--author Poly] [--version 0.1] \
  [--keep-handoff]
```

O script imprime um JSON: `output`, `title`, `header`, `version`, `tables`, `paragraphs`.

`.docx` não expõe número de páginas sem abrir no Word — não invente páginas.

### Inferência (se o usuário não passar flags)

| Campo | Default |
|---|---|
| `title` | Primeiro H1 (`# ...`) |
| `header` | `{author} — {título com — virando ·}` |
| `version` | Campo `**Versão:**` do Markdown |
| `author` | `Poly` |
| `output` | `INPUT` com `.docx` |

`$ARGUMENTS` do comando: caminho do `.md`. Se vier também um `.docx`, use como destino. Se não houver argumento, use o `.md` da conversa / arquivo aberto.

`--header` só quando o H1 for longo demais para a faixa (ex.: Etapa 2 usou “documentos e serviços”).

## Depois de gerar

1. Confira o JSON (`output` no path certo, `tables`/`paragraphs` > 0).
2. Responda o caminho do `.docx`.
3. Não deixe gerador one-off no repo.

## Fora de escopo

Imagens, Markdown aninhado complexo, HTML rico. Se o `.md` depender disso, avise e gere o que o layout cobre (títulos, listas, tabelas, código, ênfase).
