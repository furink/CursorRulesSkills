---
description: Atualiza branches locais pendentes de push com o remoto e faz push de todas as tags locais.
---

# Atualiza repositório — push de branches e tags pendentes

Execute os passos abaixo em ordem. Responda em português.

---

## 1. Verificar estado do repositório

```bash
git remote -v
```

- Se não houver remote configurado, pare e avise o usuário.

---

## 2. Fetch do remoto

```bash
git fetch --all --prune
```

---

## 3. Identificar branches com commits pendentes de push

```bash
git for-each-ref --format='%(refname:short) %(upstream:short) %(upstream:trackshort)' refs/heads/
```

- Liste todas as branches locais que estejam **à frente** do remoto (indicador `>`  ou `<>` na coluna trackshort).
- Ignore branches sem upstream configurado (informe-as separadamente ao final, sem tentar push).
- Se nenhuma branch estiver pendente, informe e pule para o passo 5.

---

## 4. Push das branches pendentes

Para cada branch identificada no passo 3:

```bash
git push origin <branch>
```

- Se algum push falhar (ex.: rejected por divergência), **não force**. Registre o erro e continue com as demais.
- Ao final, mostre um resumo: branches atualizadas com sucesso e branches com erro (se houver).

---

## 5. Push de todas as tags locais

```bash
git push origin --tags
```

- Se não houver tags novas para enviar, informe que todas as tags já estão sincronizadas.

---

## 6. Resumo final

Apresente uma tabela com:

| Item | Resultado |
|---|---|
| Branches atualizadas | lista ou "nenhuma pendente" |
| Branches com erro | lista ou "nenhuma" |
| Branches sem upstream | lista ou "nenhuma" |
| Tags enviadas | quantidade ou "todas já sincronizadas" |
