# 🧩 Create Tasks in GitHub
Um script **100% em Python puro**, **sem dependências externas**, criado para **gerar issues automaticamente** em um repositório GitHub a partir de um arquivo de texto.  
Ideal para automatizar a criação de tarefas de trabalhos, projetos, planejamentos ou sprints.

---

## 🚀 Funcionalidades

✔️ Lê um arquivo `tarefas.txt` com a lista de issues  
✔️ Identifica sessões e tarefas automaticamente  
✔️ Cria issues no GitHub sem usar `requests`  
✔️ Usa apenas bibliotecas nativas (`urllib.request`, `os`, `json`)  
✔️ Envia cada issue com **título e corpo formatado**  
✔️ Delay interno para evitar **rate-limit 403**  
✔️ Aceita token via arquivo `.env`  
✔️ Configurável para qualquer repositório

---

## 📂 Estrutura do Repositório
```
create-tasks-in-github/
│
├── index.py # Script principal
├── tarefas.txt # Lista de tarefas/issues
├── .env # Token de acesso ao GitHub
└── README.md # Documentação 
```
---

## 📝 Estrutura do `tarefas.txt`

O arquivo deve seguir este formato:

```
13. Testes Finais
Issue 80 — Testar carga full
Issue 81 — Testar carga incremental
Issue 82 — Validar SCD Tipo 2
Issue 83 — Testar leitura Delta Lake
Issue 84 — Testar pipelines da orquestração
Issue 85 — Testar dashboard final
Issue 86 — Revisar documentação
Issue 87 — Revisar README final

14. Entrega Final
Issue 88 — Submeter URL do GitHub no AVA
Issue 89 — Submeter URL do MKDocs no AVA
Issue 90 — Verificar checklist final de entrega
```

---

O script automaticamente:

- Detecta sessões (ex: *1. Primeira Fase do Projeto*)
- Extrai número e título das issues
- Cria corpo padronizado
- Envia para o GitHub

---

## 🔑 Criando o `.env`

Crie um arquivo `.env` na raiz:

```
ACCESS_TOKEN=seu_token_aqui
```

O token deve ter permissão:

- `repo` → para criar issues

Crie o token em:  
https://github.com/settings/tokens?type=beta

---

## ⚙️ Configuração no Script

Modifique no topo do `index.py`:

```python
OWNER = "seu-usuario-ou-org"
REPO = "nome-do-repositorio"
```

---

# Como executar

```

py index.py

```

---
