---
description: Stage dos arquivos, gera descrição via /descricao_commit e faz o commit (com confirmação). Aborta se .alerta.txt estiver preenchido e staged.
---

Execute os passos abaixo, em ordem, sem pular etapas:

1. **Stage dos arquivos**
   - Rode `git status` para ver o que está modificado.
   - Rode `git add -A` (ou, se o usuário tiver indicado arquivos específicos na mensagem, use `git add <arquivos>`).

2. **Regra dura — `.alerta.txt` (obrigatória, não pular)**
   - Após o stage, verifique se `.alerta.txt` está no índice:
     - `git diff --staged --name-only -- .alerta.txt`
   - Se o arquivo **estiver no stage** e **preenchido** (conteúdo com texto além de espaços em branco / linhas vazias):
     - **Cancele imediatamente** o restante deste comando.
     - **Não** gere descrição, **não** peça confirmação e **não** execute `git commit`.
     - Notifique o usuário de forma explícita: o commit foi abortado porque `.alerta.txt` está preenchido e staged; esvazie o arquivo (ou retire-o do stage) e rode o comando de novo.
   - Se o arquivo não existir, estiver vazio/só whitespace, ou não estiver no stage: prossiga.

3. **Gerar a descrição do commit**
   - Siga exatamente as instruções do comando `/descricao_commit` (ver @descricao_commit.md) para gerar a descrição executiva com base no `git diff --staged` atual.
   - Não invente informação que não esteja no diff.

4. **Confirmação obrigatória**
   - Mostre ao usuário a mensagem de commit completa (título + corpo) gerada no passo anterior.
   - Pergunte explicitamente: "Posso commitar com essa mensagem?"
   - **NÃO execute `git commit` até receber uma confirmação clara do usuário** (ex: "sim", "pode", "confirmado").
   - Se o usuário pedir ajustes na mensagem, refaça o texto e pergunte novamente antes de prosseguir.

5. **Commit**
   - Somente após confirmação, rode:
```bash
     git commit -m "<título gerado>" -m "<corpo gerado>"
```

6. **Confirmação final**
   - Rode `git log -1 --stat` e mostre o resumo do commit criado.