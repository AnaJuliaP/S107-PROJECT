import os
from src.repositories.json_repo import JSONTarefaRepository

class GerenciadorTarefas:
    def __init__(self, arquivo_dados=None, repo=None):
        if repo is not None:
            self.repo = repo
        else:
            # Decisão dinâmica de infraestrutura
            db_host = os.getenv("DB_HOST")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_name = os.getenv("DB_NAME")

            usar_postgres = all([db_host, db_user, db_password, db_name])

            if usar_postgres:
                # Import dinâmico para não quebrar ambientes de teste sem psycopg2
                from src.repositories.postgres_repo import PostgresTarefaRepository
                self.repo = PostgresTarefaRepository()
            else:
                self.repo = JSONTarefaRepository(arquivo_dados)

    @property
    def tarefas(self):
        if hasattr(self.repo, 'tarefas'):
            return self.repo.tarefas
        return {}

    @property
    def proximo_id(self):
        if hasattr(self.repo, 'proximo_id'):
            return self.repo.proximo_id
        return 1

    def criar_tarefa(self, titulo, disciplina, descricao, prioridade, prazo):
        if not titulo or titulo.strip() == "":
            raise ValueError("Título não pode ser vazio")
        if not disciplina or disciplina.strip() == "":
            raise ValueError("Disciplina não pode ser vazia")

        prioridades_validas = ["baixa", "media", "alta"]
        if prioridade not in prioridades_validas:
            raise ValueError("Prioridade inválida")

        return self.repo.criar_tarefa(titulo, disciplina, descricao, prioridade, prazo)

    def buscar_tarefa(self, id_tarefa):
        return self.repo.buscar_tarefa(id_tarefa)

    def listar_tarefas(self):
        return self.repo.listar_tarefas()

    def editar_tarefa(self, id_tarefa, titulo=None, disciplina=None, descricao=None, prioridade=None, prazo=None):
        if titulo is not None and titulo.strip() == "":
            raise ValueError("Título não pode ser vazio")
        if disciplina is not None and disciplina.strip() == "":
            raise ValueError("Disciplina não pode ser vazia")
        if prioridade is not None:
            prioridades_validas = ["baixa", "media", "alta"]
            if prioridade not in prioridades_validas:
                raise ValueError("Prioridade inválida")

        self.repo.editar_tarefa(id_tarefa, titulo, disciplina, descricao, prioridade, prazo)

    def remover_tarefa(self, id_tarefa):
        self.repo.remover_tarefa(id_tarefa)

    def concluir_tarefa(self, id_tarefa):
        # Validação de regra de negócio acadêmica
        tarefa = self.buscar_tarefa(id_tarefa)
        if tarefa["status"] == "concluida":
            raise ValueError("Tarefa já está concluída")

        self.repo.concluir_tarefa(id_tarefa)

    def filtrar_por_disciplina(self, disciplina):
        return self.repo.filtrar_por_disciplina(disciplina)

    def filtrar_por_prioridade(self, prioridade):
        prioridades_validas = ["baixa", "media", "alta"]
        if prioridade not in prioridades_validas:
            raise ValueError("Prioridade inválida")
        return self.repo.filtrar_por_prioridade(prioridade)

    def filtrar_por_status(self, status):
        status_validos = ["pendente", "em andamento", "concluida"]
        if status not in status_validos:
            raise ValueError("Status inválido")
        return self.repo.filtrar_por_status(status)