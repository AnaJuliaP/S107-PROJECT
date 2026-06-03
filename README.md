# 📚 Gerenciador de Tarefas Acadêmicas
 
Sistema desenvolvido em Python para gerenciamento de tarefas acadêmicas via terminal, com suporte a CRUD completo, filtros e validações, integrado a uma esteira completa de CI/CD com Jenkins e Docker.

---

## 🎯 Objetivo

Facilitar a organização de atividades acadêmicas, permitindo criar, acompanhar e gerenciar tarefas de forma simples e eficiente diretamente pelo terminal, demonstrando na prática os conceitos de DevOps: containerização, pipeline automatizado e entrega contínua.

---

## ⚙️ Funcionalidades

- Criar tarefas;
- Listar tarefas;
- Buscar tarefa por ID;
- Editar tarefas;
- Remover tarefas (com confirmação);
- Marcar tarefas como concluídas;
- Filtrar tarefas por:
  - Disciplina;
  - Prioridade (baixa, média, alta);
  - Status (pendente, em andamento, concluída).

---

## 🧱 Estrutura do Projeto

```text
S107-PROJECT/
├── src/
│   └── gerenciador.py           # Lógica principal do sistema
├── tests/
│   ├── test_gerenciador.py      # Testes unitários (domínio)
│   ├── test_gerenciador_cobertura.py  # Testes de cobertura adicional
│   └── test_main_integration.py # Testes de integração (CLI / main)
├── scripts/
│   └── notificar.py             # Script de notificação do pipeline
├── Dockerfile                   # Imagem da aplicação (Python 3.12 slim)
├── Dockerfile.jenkins           # Imagem do Jenkins com Python e Docker CLI
├── Jenkinsfile                  # Pipeline CI/CD (testes, build, Docker Hub, notificação)
├── docker-compose.yml           # Orquestração dos 4 containers
├── main.py                      # Interface via terminal
├── pyproject.toml               # Configuração de build e testes
└── requirements.txt             # Dependências do projeto
```

---

## 🚀 Como executar o projeto

### Pré-requisitos
 
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução
- [Git](https://git-scm.com/) instalado

### 1. Clone o repositório

```bash
git clone https://github.com/AnaJuliaP/S107-PROJECT.git
cd S107-PROJECT
```

### 2. Execute o sistema localmente (sem Docker)
 
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```
 
---
 
## 🐳 Como executar com Docker Compose
 
### 1. Suba todos os containers
 
```bash
docker compose up --build
```
 
Isso irá subir os 4 containers:
- **jenkins** — servidor CI/CD na porta `http://localhost:8080`
- **app** — a aplicação Python (imagem do Docker Hub)
- **mailhog** — servidor de e-mail fake na porta `http://localhost:8025`
- **db** — banco de dados PostgreSQL

### 2. Acesse o Jenkins
 
Abra `http://localhost:8080` no navegador.
 
Na primeira execução, a senha inicial aparece no terminal. Exemplo:
```
jenkins | > 3cb8876f217e4d5aa79cdc95a1722acd
```
 
Instale os plugins sugeridos e crie seu usuário.
 
### 3. Configure a credencial do Docker Hub
 
Vá em **Gerenciar Jenkins → Credentials → Global → Add Credentials**:
 
| Campo | Valor |
|---|---|
| Kind | Username with password |
| Username | leticialm |
| Password | (token de acesso Docker Hub) |
| ID | docker-hub-leticialm |
 
### 4. Configure as credenciais de e-mail
 
Adicione mais duas credenciais do tipo **Secret text**:
 
| ID | Valor |
|---|---|
| EMAIL_REMETENTE | endereço de e-mail remetente |
| EMAIL_DESTINO | endereço de e-mail destinatário |
 
### 5. Crie o pipeline
 
Clique em **Novo tarefa → Pipeline**, configure:
- **Definition:** Pipeline script from SCM
- **SCM:** Git
- **Repository URL:** `https://github.com/AnaJuliaP/S107-PROJECT`
- **Branch:** `*/main`
- **Script Path:** `Jenkinsfile`
Clique em **Construir agora** para rodar o pipeline.
 
### 6. Para parar os containers
 
```bash
docker compose down
```
 
> ⚠️ Use `docker compose down -v` apenas se quiser apagar todos os dados e começar do zero.
 
---
 
## 🧪 Testes
 
O projeto utiliza pytest com cobertura mínima de **90%** (configurado em `pyproject.toml`). A cobertura atual é de **100%**.
 
```bash
pytest -v
```
 
Para gerar relatório de cobertura:
 
```bash
pytest --cov=src --cov-report=term-missing
```
 
---
 
## 🔁 Pipeline Jenkins
 
O `Jenkinsfile` executa automaticamente as seguintes etapas:
 
| Stage | O que faz |
|---|---|
| Checkout | Clona o repositório do GitHub |
| Instalar Dependências | Instala pytest, pytest-cov, pytest-html e build |
| Testes | Roda 44 testes com cobertura, gera `report.html` e `coverage.xml` |
| Build | Empacota o projeto com `python -m build`, gera `.whl` e `.tar.gz` |
| Docker Build e Push | Builda e publica a imagem no Docker Hub com tags `latest` e `{BUILD_NUMBER}` |
| Notificação | Envia e-mail com o status do pipeline via Mailhog |
 
Os artefatos gerados (relatório de testes, cobertura e pacote) ficam disponíveis no Jenkins para download.
 
---
 
## 🐳 Docker Hub
 
Imagem publicada pelo pipeline: [`leticialm/s107-project`](https://hub.docker.com/r/leticialm/s107-project)
 
```bash
docker pull leticialm/s107-project:latest
docker run --rm -it leticialm/s107-project:latest
```
 
---
 
## 📌 Regras de Negócio
 
- O título e a disciplina não podem ser vazios
- Prioridade deve ser: `baixa`, `media` ou `alta`
- Status válidos: `pendente`, `em andamento`, `concluida`
- IDs são gerados automaticamente e são únicos
- Não é possível concluir uma tarefa já concluída
---
 
## 🛠️ Tecnologias Utilizadas
 
- Python 3.12 / 3.13
- Pytest + pytest-cov + pytest-html
- Docker + Docker Compose
- Jenkins (modo container)
- Docker Hub
- Mailhog (servidor SMTP para testes)
- PostgreSQL 15
---
 
## 🤖 Uso de Inteligência Artificial
 
### Modelos utilizados
 
- **Claude Sonnet (Anthropic)** — Lilyan
- **Claude (Anthropic) — via claude.ai** — Ana Julia
- **Claude (Anthropic) — via claude.ai** — Letícia
- **[PREENCHER]** — Vitória
- **[PREENCHER]** — Lucas
- **ChatGPT** — Gustavo

---

### Para quê foi usada - Lilyan:
 
- Entendimento do projeto e da divisão de tarefas
- Criação do `docker-compose.yml` com 4 containers e configuração de redes
- Debug de erros no `Dockerfile.jenkins` (tag inválida, conflito de wheel com apt)
- Validação e testes do pipeline Jenkins
- Entendimento dos conceitos de CI/CD, containerização e pipeline

### Exemplos reais de prompts
 
**Prompt 1:**
> "Com base nesses slides e nessa matéria, poderia gerar perguntas pra mim pra eu saber se estou entendendo o conteúdo?"
 
Resposta aceita: quiz completo sobre CI/CD, pipeline e containerização com feedback detalhado por questão.
 
**Prompt 2:**
> "Poderia me ajudar a entender o projeto e o meu papel como Integrante 3?"
 
Resposta aceita com ajustes: a IA explicou os papéis de cada integrante e identificou que as tarefas do meu papel já estavam prontas, sugerindo que eu assumisse o `docker-compose.yml`.
 
**Prompt 3:**
> "Agora cria o arquivo docker-compose.yml. Vou te mostrar o Dockerfile.jenkins e o Dockerfile da aplicação primeiro."
 
Resposta aceita com ajuste: a IA gerou o compose com 4 containers. O placeholder da imagem do Docker Hub foi ajustado manualmente quando a Letícia publicou a imagem real.
 
**Prompt 4:**
> "Deu esse erro no docker compose up --build [erro do pip wheel]. O que está errado?"
 
Resposta aceita: a IA identificou o conflito entre o wheel instalado pelo apt (Debian) e o pip tentando fazer upgrade, e explicou como corrigir no Dockerfile.jenkins.
 
### Dinâmica de uso
 
Usada em sessão contínua de pair programming ao longo de vários dias, cobrindo desde o entendimento dos conceitos até o debug de problemas reais no Docker.

> **[ATENÇÃO PARA O GRUPO]:** Cada integrante deve preencher sua linha na lista de modelos utilizados e pode adicionar seus próprios prompts nesta seção.
---
### Para quê foi usada - Ana Julia:

### Exemplos reais de prompts
 
**Prompt 1**
>Como configurar um Dockerfile para rodar Jenkins com Python 3 instalado?

Resposta aceita: a IA explicou como estender a imagem oficial do Jenkins instalando Python via apt-get e as ferramentas de teste via pip, mantendo boas práticas como voltar para USER jenkins ao final.

**Prompt 2**
>Como estruturar as stages de teste e build no Jenkinsfile para salvar artefatos no Jenkins?

Resposta aceita: a IA explicou o uso de archiveArtifacts dentro do bloco post e como separar o relatório de testes do pacote gerado pelo build.

**Prompt 3**
>Variáveis como currentBuild.currentResult podem ser usadas diretamente dentro de sh no Jenkinsfile?

Resposta aceita: a IA explicou que não funcionam com aspas simples e sugeriu capturar o valor em variável local dentro de um bloco script{} antes de passar ao shell.

**Prompt 4**
>Como identificar quais ramos do código não estão sendo cobertos pelos testes usando pytest-cov?

Resposta aceita: a IA explicou o uso da flag --cov-report=term-missing que mostra exatamente as linhas não cobertas, o que ajudou a identificar os casos faltantes no editar_tarefa().

**Prompt 5**
>O Dockerfile está apontando vulnerabilidades críticas na imagem base do Jenkins, como resolver?

Resposta aceita: a IA sugeriu trocar para a variante -slim e adicionar apt-get upgrade -y para reduzir CVEs herdados da imagem base.

### Dinâmica de uso

Utilizada em sessões pontuais durante o desenvolvimento, consultando dúvidas específicas de configuração do Jenkins e cobertura de testes. A IA funcionou como apoio para entender comportamentos inesperados e revisar decisões técnicas, sempre com o código sendo escrito e validado pelo integrante.

### Para quê foi usada - Leticia:

- Diagnóstico e correção de erros no `Dockerfile.jenkins` (binário Docker não encontrado, tag de imagem inválida, conflito de pip com ambiente externo)
- Configuração do `docker-compose.yml` para permitir acesso ao socket do Docker dentro do container Jenkins (`/var/run/docker.sock` e `group_add`)
- Debug de permissão no socket do Docker (identificação do GID 0 no Docker Desktop/Windows)
- Reconfiguração do Jenkins após perda de volume
- Entendimento de como o Docker Desktop no Windows gerencia o socket diferente do Linux

### Exemplos reais de prompts
 
**Prompt 1:**
> "to com esse erro no jenkins: docker: not found / ERROR: script returned exit code 127"

Resposta aceita com ajustes: a IA sugeriu inicialmente instalar o `docker.io` via apt, o que não resolveu o problema. Após mais investigação, a solução correta foi instalar o `docker-ce-cli` via repositório oficial do Docker, adicionando a chave GPG e o repositório antes da instalação

**Prompt 2:**
> "docker exec -it jenkins docker version
> permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock"

Resposta aceita: a IA identificou que o usuário `jenkins` não tinha permissão no socket do Docker e orientou a usar `group_add` no `docker-compose.yml` com o GID do socket, que no Docker Desktop no Windows é `0` (root).

**Prompt 3:**
> "docker compose build --no-cache jenkins
> error: externally-managed-environment — pip não consegue instalar pacotes sistema"

Resposta aceita: a IA identificou que o comando `pip install --upgrade pip` estava sem a flag `--break-system-packages`, causando falha no build. A correção foi adicionar a flag em todos os comandos pip do Dockerfile.

**Prompt 4:**
> "pq quando eu coloquei o group_add "0" (root) funcionou?"

Resposta aceita: a IA explicou que no Docker Desktop no Windows o socket pertence ao grupo root (GID 0), diferente do Linux onde o GID costuma ser 999.

### Dinâmica de uso
Usada em sessão contínua de debug do pipeline, cobrindo desde o erro inicial de `docker: not found` até a resolução de permissão no socket e reconfiguração do Jenkins após perda de volume.
---


### Para quê foi usada - Vitoria:

### Exemplos reais de prompts
 
**Prompts:**

### Dinâmica de uso
---


### Para quê foi usada - Lucas:

### Exemplos reais de prompts
 
**Prompts:**

### Dinâmica de uso
---


### Para quê foi usada - Gustavo:

- Entendimento da estrutura do Jenkins Pipeline e funcionamento do CI/CD
- Integração do Jenkins com repositório GitHub e execução por branch específica
- Configuração de variáveis de ambiente e credentials no Jenkins
- Debug de erros relacionados a Docker, Jenkins, SMTP e variáveis de ambiente
- Ajustes no `docker-compose.yml` para comunicação entre containers

### Exemplos reais de prompts
 
**Prompts:**

**Prompt 1:**
> "Agora tem esse erro: RUN python3 -m pip install --break-system-packages --upgrade pip setuptools wheel..."

Resposta aceita: a IA identificou conflito entre pacotes instalados pelo Debian (`wheel`) e o `pip`, explicando como remover o upgrade problemático no Dockerfile.


**Prompt 2:**
> "Tem como eu testar se o email tá funcionando?"

Resposta aceita: a IA orientou a utilizar MailHog para validar o envio SMTP localmente dentro do Docker Compose, explicando o acesso via navegador (`localhost:8025`).


**Prompt 3:**
> "Chat, está sendo gerado duas imagens, como arrumo?"

Resposta aceita: a IA explicou a diferença entre múltiplas tags (`latest` e `${BUILD_NUMBER}`) e múltiplas imagens Docker, além de orientar sobre versionamento de imagens.

### Dinâmica de uso
Utilizada como suporte contínuo durante o desenvolvimento do pipeline CI/CD, atuando como auxílio técnico para configuração do Jenkins, Docker Compose, integração com Docker Hub, variáveis de ambiente, notificações SMTP e resolução de erros de infraestrutura e automação.


### O que não foi feito por IA
 
- A decisão de qual sistema reutilizar (Gerenciador de Tarefas) foi tomada pelo grupo
- Os commits e PRs foram feitos manualmente por cada integrante
- A configuração do Jenkins (criação do job, adição de credenciais) foi feita manualmente
- O teste final do pipeline rodando com SUCCESS foi validado manualmente
---
 
 
## 👥 Autores
 
Desenvolvido por:
- Ana Julia P.
- Letícia M.
- Lilyan Oliveira
- Vitória Dutra
- Lucas David
- Gustavo Marques

INATEL — S107 Gerência de Configuração e Evolução de Software
 
## 📄 Licença
 
Este projeto é apenas para fins acadêmicos.
 