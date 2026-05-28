# 📚 Gerenciador de Tarefas Acadêmicas

Sistema desenvolvido em Python para gerenciamento de tarefas acadêmicas via terminal, com suporte a CRUD completo, filtros e validações, além de integração com CI/CD utilizando GitHub Actions.

---

## 🎯 Objetivo

Facilitar a organização de atividades acadêmicas, permitindo ao usuário criar, acompanhar e gerenciar suas tarefas de forma simples e eficiente diretamente pelo terminal.

---

## ⚙️ Funcionalidades

- ✅ Criar tarefas
- 📋 Listar tarefas
- 🔍 Buscar tarefa por ID
- ✏️ Editar tarefas
- 🗑️ Remover tarefas (com confirmação)
- ✔️ Marcar tarefas como concluídas
- 🎯 Filtrar tarefas por:
  - Disciplina
  - Prioridade (baixa, média, alta)
  - Status (pendente, em andamento, concluída)

---

## 🧱 Estrutura do Projeto

```text
gerenciador-tarefas-academicas/
├── src/
│   └── gerenciador.py          # Lógica principal do sistema
├── tests/
│   ├── test_gerenciador.py     # Testes unitários (domínio)
│   └── test_main_integration.py # Testes de integração (CLI / main)
├── Dockerfile                  # Imagem local (Python 3.12 slim)
├── Jenkinsfile                 # Pipeline Jenkins (testes, build, Docker Hub)
├── Dockerfile.jenkins          # Imagem opcional do Jenkins com Python, pip e cliente Docker
├── main.py                     # Interface via terminal
├── notificar.py                # Script de notificação do pipeline
├── requirements.txt            # Dependências do projeto
└── .github/
    └── workflows/
        └── ci-cd.yml           # Pipeline CI/CD
```


---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/gerenciador-tarefas-academicas.git
cd gerenciador-tarefas-academicas
```

### 2. Crie um ambiente virtual (opcional)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema

```bash
python main.py
```

## 🧪 Testes

O projeto utiliza pytest com cobertura mínima de **90%** (`pytest-cov`, configurado em `pyproject.toml`).

Para executar:

```bash
pytest -v
```

## 🐳 Docker (build local e testes no container)

Construir a imagem (na raiz do repositório):

```bash
docker build -t gerenciador-tarefas:local .
```

Rodar a aplicação interativa:

```bash
docker run --rm -it gerenciador-tarefas:local
```

Rodar a suíte de testes (unitários + integração) com cobertura:

```bash
docker run --rm gerenciador-tarefas:local pytest -q
```

Imagem publicada pelo Jenkins (Docker Hub), após o pipeline:

```bash
docker pull leticialm/s107-project:latest
docker run --rm -it leticialm/s107-project:latest
```

## 🔁 Jenkins + publicação no Docker Hub

O `Jenkinsfile` segue a ordem: **Checkout → Instalar Deps → Testes → Build → Docker Build e Push → Notificação**. O estágio **Docker Build e Push** envia a imagem para o repositório **`leticialm/s107-project`** no Docker Hub com as tags **`${BUILD_NUMBER}`** e **`latest`**.

### Pré-requisitos

1. **Docker Hub**: crie o repositório público (ou privado) `s107-project` na conta `leticialm`, se ainda não existir.
2. **Access Token** no Hub: *Account Settings → Security → New Access Token* (não use a senha da conta).
3. **Jenkins**
   - O job roda como usuário **sem root**: **não** use `apt-get` dentro do `Jenkinsfile`. Dependências de sistema (Python, pip, cliente Docker) devem estar na **imagem do Jenkins** (ex.: `Dockerfile.jenkins` na raiz: `docker build -f Dockerfile.jenkins -t jenkins-custom .`).
   - Agente com **`docker`** no `PATH` e acesso ao daemon (ex.: montar `/var/run/docker.sock` do host no container do Jenkins, e usuário `jenkins` com permissão nesse socket).
   - **Credencial** (*Manage Jenkins → Credentials*):
     - Tipo: **Username with password**
     - Usuário: seu usuário Docker Hub (`leticialm`)
     - Senha: o **token** de acesso
     - ID da credencial: **`docker-hub-leticialm`** (tem que ser exatamente esse ID, ou altere o valor de `DOCKER_HUB_CREDENTIAL_ID` no `Jenkinsfile`)

Cada execução bem-sucedida do job (após **Testes** e **Build** do pacote Python) faz `docker login`, `docker build`, `docker push` das duas tags e `docker logout`.

## 🔁 CI/CD com GitHub Actions

O pipeline automatiza:

🔧 Instalação de dependências  
🧪 Execução dos testes  
📦 Geração de pacote do projeto  
📊 Geração de relatório de testes  
📣 Notificação do resultado do pipeline  
🌐 Deploy automático no GitHub Pages (quando na branch main)  
📧 Notificação do Pipeline

O sistema suporta envio de e-mails com o resultado do CI/CD.

Para ativar, configure os seguintes secrets no GitHub:

SMTP_HOST  
SMTP_PORT  
EMAIL_REMETENTE  
EMAIL_SENHA  
EMAIL_DESTINO

## 🛠️ Tecnologias Utilizadas

Python 3.11  
Pytest  
GitHub Actions  
SMTP (envio de e-mails)

## 📌 Regras de Negócio

O título e a disciplina não podem ser vazios  
Prioridade deve ser: baixa, media ou alta  
Status válidos: pendente, em andamento, concluida  
IDs são gerados automaticamente e são únicos  
Não é possível concluir uma tarefa já concluída

## 🤖 Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta de apoio durante o desenvolvimento do projeto, auxiliando na estruturação e refatoração do código, sugestão de tipos de testes, definição do pipeline de CI/CD e identificação/correção de erros. Seu uso teve caráter complementar, com todas as decisões finais de implementação, validação e organização sendo realizadas manualmente.

## 👨‍💻 Autor

Desenvolvido por Vitória Dutra e Letícia Moraes

## 📄 Licença

Este projeto é apenas para fins acadêmicos.