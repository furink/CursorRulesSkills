# 🔍 Revisão de Pré-Commit: Verificação de Logs

Por favor, analise as alterações (diff) dos arquivos que estão adicionados na área de stage para o próximo commit.

Sua tarefa é garantir que nenhum log de debug tenha sido esquecido no código antes de enviá-lo.

**O que você deve procurar:**
- `console.log` (arquivos frontend, como React/TypeScript)
- `Log::info` (arquivos backend)
- Qualquer outra instrução de impressão de debug similar que não pareça fazer parte do fluxo oficial de logs da aplicação.

**Como você deve responder:**
1. **Se encontrar logs esquecidos:** Pare a geração da mensagem de commit. Liste os arquivos e as linhas exatas onde os logs foram encontrados e me pergunte se desejo removê-los.
2. **Se o código estiver limpo:** Confirme brevemente que nenhum log indesejado foi encontrado e siga normalmente com a sugestão da mensagem de commit ou próxima etapa.