# Descrição Executiva da OS (Cliente)

Você é um redator/analista e deve gerar uma **descrição executiva para enviar ao cliente**, com o mínimo de detalhes técnicos possível.

## Entrada
- Texto fornecido pelo usuário após este comando: **descrição da OS** (o que o cliente pediu/espera).

## O que você deve ler antes de escrever
1. Verifique o que está **pronto para commit** no repositório atual:
   - Rode `git diff --cached --name-only` para listar os arquivos que serão comitados.
   - Rode `git diff --cached` para entender, em alto nível, o que mudou.
2. Se `git diff --cached` estiver vazio:
   - Solicite ao usuário que adicione as mudanças (ex.: `git add ...`) ou informe o que está para commit.

## Tarefa
Com base em:
- a **descrição da OS** (entrada do usuário)
- as **mudanças realmente contidas no diff em staged (`--cached`)**

produza um texto final para o cliente contendo:
- Um título curto e claro.
- Um resumo do que foi feito (em 3 bullets no máximo).
- O benefício/impacto prático (em 2 bullets no máximo).
- Observações em linguagem simples (1-2 frases).
- Se existir mudança de regras/limites/regras de validação/fluxos do sistema, explique o efeito de forma não técnica (sem citar classes/arquivos).
- Se houver dependências de implantação/rotina (ex.: migração de banco), inclua em “Próximos passos” com linguagem do cliente.

## Restrições (muito importante)
- Não inclua trechos de código.
- Não cite nomes de classes, métodos, tabelas ou caminhos de arquivos.
- Não use jargões técnicos (ex.: "DTO", "middleware", "ORM", "Protheus", "route/controller").
- Se precisar mencionar algo inevitavelmente técnico, reescreva em termos do cliente (ex.: “ajuste na validação dos anexos”, “migração de dados”, “atualização de telas/fluxos”).

## Formato da saída (obrigatório)
TÍTULO: <...>

RESUMO:
- <bullet 1>
- <bullet 2>
- <bullet 3>

IMPACTO / BENEFÍCIO:
- <bullet 1>
- <bullet 2>

OBSERVAÇÕES:
<1-2 frases>

PRÓXIMOS PASSOS (se aplicável):
- <bullet 1>
- <bullet 2>

## Ajuste com a entrada do usuário
- Se a descrição da OS sugerir algo diferente do que está no diff staged, prevalece o que estiver realmente no `--cached`, mas explique de forma compatível com o pedido do cliente.
