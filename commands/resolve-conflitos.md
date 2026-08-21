# Resolução de Conflitos de Merge

Você vai me ajudar a resolver conflitos de merge seguindo um processo em duas fases. Não pule etapas nem tente resolver tudo de uma vez.

## Fase 1 — Levantamento

1. Rode `git status` e `git diff --name-only --diff-filter=U` para identificar todos os arquivos em conflito.
2. Para cada arquivo, abra e liste:
   - O trecho em conflito (marcadores `<<<<<<<`, `=======`, `>>>>>>>`)
   - Uma explicação do que cada lado (branch atual vs. branch de origem do merge) está tentando fazer
   - Por que o conflito ocorreu (ex: mesma linha alterada, lógica divergente, refatoração x feature nova)
3. Apresente essa lista completa e **pare**. Não inicie a resolução ainda — aguarde minha confirmação para prosseguir.

## Fase 2 — Resolução arquivo a arquivo

Depois que eu confirmar, processe os arquivos em conflito **um de cada vez**, nesta ordem:

Para cada arquivo:
1. **Por que o conflito aconteceu** — explicação objetiva do motivo técnico.
2. **Ação de resolução proposta** — o que você pretende manter, remover ou mesclar, e por quê. Se houver mais de uma abordagem razoável, apresente as opções antes de aplicar.
3. Aplique a resolução no arquivo (remova os marcadores de conflito).
4. Rode um `git diff` do arquivo resolvido para eu revisar.
5. Aguarde minha confirmação explícita de que a resolução deste arquivo está correta.
6. Após minha confirmação, execute `git add <arquivo>` para stagear apenas este arquivo.
7. Confirme o stage com `git status` (o arquivo deve aparecer em "Changes to be committed") e só então avance para o próximo arquivo.

## Regras gerais
- Nunca resolva mais de um arquivo por vez sem confirmação.
- Só execute `git add` de um arquivo **depois** que eu confirmar que a resolução dele está correta. Nunca faça o stage antes da minha confirmação, e nunca faça o stage de mais de um arquivo por vez.
- Se um conflito envolver lógica de negócio ambígua (não só formatação/import), sinalize isso claramente e peça minha decisão em vez de escolher sozinho.
- **NUNCA execute `git commit` por conta própria, em nenhuma etapa.** O commit só acontece se eu autorizar explicitamente ao final do processo.

## Fase 3 — Encerramento

Após todos os arquivos em conflito terem sido resolvidos e stageados:

1. Rode `git diff --check` para confirmar que não sobrou nenhum marcador de conflito (`<<<<<<<`, `=======`, `>>>>>>>`) em nenhum arquivo.
2. Rode `git status` e me mostre o resumo de todos os arquivos já stageados.
3. Apresente um resumo geral do merge: quais arquivos foram alterados e a lógica de resolução aplicada em cada um.
4. **Pergunte explicitamente se eu quero que você faça o commit agora.** Não assuma uma resposta positiva nem prossiga automaticamente.
5. Se eu confirmar, pergunte também se devo sugerir uma mensagem de commit ou se você mesmo vai escrever uma — só então execute `git commit`.
6. Se eu não quiser commitar agora, encerre o fluxo e deixe as mudanças apenas stageadas, aguardando minha ação manual.