import os
import json
import urllib.request
import time

# ------------------------------
# Carregar .env manualmente
# ------------------------------
def load_env(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            os.environ[key] = value

load_env()

# ------------------------------
# Variáveis
# ------------------------------
GITHUB_TOKEN = os.getenv("ACCESS_TOKEN")
OWNER = "luizantoniocardoso"
REPO = "trabalho-final-eng-dados"

API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"


# ------------------------------
# Enviar POST (sem requests)
# ------------------------------
def http_post(url, data, token):
    data_bytes = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        # Ler o body do erro
        error_body = e.read().decode("utf-8")

        return e.code, error_body
    except Exception as e:
        return None, str(e)


# ------------------------------
# Ler arquivo de tarefas
# ------------------------------
def ler_tarefas(caminho="tarefas.txt"):
    with open(caminho, "r", encoding="utf-8") as file:
        return file.readlines()


# ------------------------------
# Extrair issues
# ------------------------------
def extrair_issues(linhas):
    sessao_atual = None
    issues = []

    for linha in linhas:
        linha = linha.strip()

        if linha and "Issue" not in linha and linha[0].isdigit():
            sessao_atual = linha
            continue

        if linha.startswith("Issue"):
            partes = linha.split("—")
            numero = partes[0].replace("Issue", "").strip()
            titulo = partes[1].strip()

            issues.append({
                "numero": numero,
                "titulo": titulo,
                "sessao": sessao_atual
            })

    return issues


# ------------------------------
# Criar corpo da issue
# ------------------------------
def gerar_body(issue):
    return f"""
### 📌 Descrição
Esta issue refere-se à tarefa **{issue['numero']}** da etapa do projeto.

### 🧩 Objetivo
Executar: **{issue['titulo']}**

### 📄 Detalhes
- Esta tarefa faz parte da fase: **{issue['sessao']}**
- Criada automaticamente via script Python.

### ✅ Critérios de aceitação
- [ ] Atividade concluída
- [ ] Documentação atualizada (se aplicável)
- [ ] Revisão realizada
"""


# ------------------------------
# Criar issue no GitHub (com delay)
# ------------------------------
def criar_issue(titulo, body):
    payload = {
        "title": titulo,
        "body": body
    }

    status, resp = http_post(API_URL, payload, GITHUB_TOKEN)

    if status == 201:
        print(f"✔️ Issue criada: {titulo}")
    else:
        print(f"❌ Falha ao criar issue: {titulo}")
        print(f"Status: {status}")
        print(resp)

        # Caso seja rate-limit, mostrar aviso claro
        if status == 403 and "rate" in resp.lower():
            print("⚠️ Rate limit atingido! Aguardando 10 segundos...")
            time.sleep(10)

    # ------------------------------
    # DELAY PARA EVITAR RATE LIMIT
    # ------------------------------
    time.sleep(1.2)   # 1200ms evita 403 em lotes grandes


# ------------------------------
# Execução principal
# ------------------------------
def main():
    tarefas = ler_tarefas("tarefas.txt")
    issues = extrair_issues(tarefas)

    print(f"Encontradas {len(issues)} issues")

    for issue in issues:
        body = gerar_body(issue)
        criar_issue(issue["titulo"], body)


if __name__ == "__main__":
    main()
