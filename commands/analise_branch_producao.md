---
description: Analisa a branch atual (ou a informada) versus a branch principal/produção e diz se o conteúdo já está lá e se é seguro apagá-la. Somente leitura — não apaga nem altera branches.
---

# Analisa branch em relação à produção

Compare uma branch de feature com a branch principal do repositório (produção) e diga se o conteúdo já está nela e se é seguro apagar a feature. **Somente leitura.** Não altere o repositório.

Argumentos: `$ARGUMENTS`

## Restrições (obrigatórias)

Este comando é **estritamente informativo**. É proibido:

- `git branch -d` / `-D`, `git push --delete`, `git tag -d`
- `git checkout`, `git switch`, `git reset`, `git rebase`, `git merge`, `git cherry-pick`
- `git commit`, `git stash`, `git clean`, `git fetch`, `git pull`, `git push`
- criar, editar ou apagar arquivos do projeto
- sugerir executar o delete automaticamente no final

Use só comandos Git de leitura (`log`, `show`, `diff`, `merge-base`, `rev-list`, `rev-parse`, `cat-file`, `name-rev`, `tag --contains`, `grep`).

Responda em português.

---

## 1. Resolver branches

**Feature (alvo):**

1. Se `$ARGUMENTS` tiver um nome de branch, use esse nome (primeiro token).
2. Senão, use `git branch --show-current`.
3. Resolva o ref nesta ordem: nome local → `origin/<nome>` → o hash, se for um SHA.
4. Se não existir, pare e diga quais refs locais/remotos se aproximam.

**Produção (principal):**

1. `git symbolic-ref --quiet refs/remotes/origin/HEAD` (ex.: `origin/master`).
2. Senão, o primeiro que existir: `origin/master`, `master`, `origin/main`, `main`.
3. Neste repositório a produção é **`master`**, salvo `origin/HEAD` apontar para outra.

Se o alvo for a própria produção, pare: peça o nome da feature (`/analise_branch_producao feature/exemplo`).

Anote tips (hash, data, assunto, autor) do alvo local, `origin/<alvo>` (se houver), produção local e `origin/<produção>`.

---

## 2. Ancestralidade e ahead/behind

```bash
git merge-base <alvo> <producao>
git merge-base --is-ancestor <alvo> <producao>
git merge-base --is-ancestor <producao> <alvo>
git rev-list --left-right --count <producao>...<alvo>
git rev-list --count --no-merges <producao>..<alvo>
git rev-list --left-right --count origin/<alvo>...<alvo>   # se o remoto existir
```

Interprete:

| Situação | Significado |
|---|---|
| Alvo é ancestral da produção e 0 commits em `producao..alvo` | Feature **já incorporada** |
| Produção é ancestral do alvo e alvo tem commits à frente | Feature **ainda não mergeada** (ou só rebase pendente) |
| Divergiram (ambos à frente) | Históricos **divergentes** — não apagar sem analisar os commits exclusivos |

---

## 3. O que a feature fez

**Ainda não está na produção** (`producao..alvo` não vazio):

```bash
git log --oneline --no-merges <producao>..<alvo>
git diff --shortstat $(git merge-base <producao> <alvo>) <alvo>
git diff --diff-filter=A --name-only $(git merge-base <producao> <alvo>) <alvo>
```

**Já está na produção** (`producao..alvo` vazio):

Encontre o merge que entrou o tip do alvo:

```bash
git log --merges --reverse --ancestry-path --format='%H %ci %s%n%an%nparents: %P%n' <alvo>..<producao>
```

Use o **primeiro** merge cujo parent inclui o tip do alvo (ou o merge cujo assunto cita o nome da branch). Depois:

```bash
git log --oneline --no-merges <merge>^1..<alvo>
git diff --shortstat <merge>^1 <alvo>
git diff --diff-filter=A --name-only <merge>^1 <alvo>
```

Se não houver merge explícito (squash/cherry-pick), diga isso e liste o que `git log --oneline --no-merges` / `git log --grep` ainda revelar pelo nome da branch.

Agrupe o trabalho por domínio (backend, frontend, banco, jobs, rotas, docs), com base nas mensagens e nos paths — sem listar centenas de arquivos. Destaque arquivos/módulos-chave.

---

## 4. Ainda está na produção? Foi revertido?

Para os arquivos **adicionados** pela feature (amostra completa se for pouca; senão os paths centrais + contagem):

```bash
git cat-file -e <producao>:<arquivo>
```

Conte quantos adicionados **faltam** na produção.

```bash
git log --oneline <merge-ou-alvo>..<producao> --grep='revert' -i
git log --oneline <producao> --grep='<nome-da-branch>' -i
git tag --contains <merge-ou-alvo-tip>
```

Confirme no `web.php` / menus / equivalentes que rotas e entradas da feature ainda existem, quando fizer sentido.

---

## 5. Veredito: seguro apagar?

**Sim**, só se **todas** forem verdadeiras:

1. O tip do alvo é ancestral da produção **ou** não há commits exclusivos (`--no-merges producao..alvo` = 0).
2. Nenhum arquivo essencial adicionado pela feature está ausente na produção (não houve revert/remoção do recurso).
3. Local e `origin/<alvo>` não têm commits exclusivos um do outro **ou** o extra local também já está na produção.

**Não**, se houver commits exclusivos no alvo, conteúdo único não presente na produção, ou revert que tirou o recurso.

**Com ressalvas**, se o Git está mergeado mas: PRs/pipelines ainda abertos (só mencionar, não consultar remoto destrutivo); 22+ arquivos evoluíram depois na produção (apagar a branch ainda é seguro; o código na produção não é um clone); outras pessoas podem ter a branch local.

Nunca apague. Informe o hash do tip para recuperação (`git branch <nome> <hash>`).

---

## 6. Formato da resposta

1. **Conclusão** em uma frase (já está na produção? seguro apagar?).
2. Tips, merge-base, ahead/behind, ancestralidade.
3. Como entrou na produção (merge, release, tag), se aplicável.
4. O que a feature entregou (tabela ou bullets por domínio).
5. Integridade na produção (arquivos presentes/faltando, reverts, tags).
6. **Veredito de exclusão**: Sim / Não / Com ressalvas — e o que conferir operacionalmente (PR aberta, alguém usando a branch). Sem comandos de delete.
