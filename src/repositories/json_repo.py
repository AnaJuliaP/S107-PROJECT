import json
import os
from src.repositories.base import RepositorioTarefas

class JSONTarefaRepository(RepositorioTarefas):
    def __init__(self, arquivo_dados=None):
        self.arquivo_dados = arquivo_dados or os.getenv("DATABASE_PATH")
        self.tarefas = {}
        self.proximo_id = 1
        if self.arquivo_dados:
            self._carregar_dados()

    def _carregar_dados(self):
        if not self.arquivo_dados or not os.path.exists(self.arquivo_dados):
            return
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.tarefas = {int(k): v for k, v in dados.get("tarefas", {}).items()}
                self.proximo_id = dados.get("proximo_id", 1)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Erro ao carregar dados de {self.arquivo_dados}: {e}")
            self.tarefas = {}
            self.proximo_id = 1

    def _salvar_dados(self):
        if not self.arquivo_dados:
            return
        diretorio = os.path.dirname(self.arquivo_dados)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump({
                    "tarefas": self.tarefas,
                    "proximo_id": self.proximo_id
                }, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados em {self.arquivo_dados}: {e}")

    def criar_tarefa(self, titulo, disciplina, descricao, prioridade, prazo):
        tarefa = {
            "titulo": titulo,
            "disciplina": disciplina,
            "descricao": descricao,
            "prioridade": prioridade,
            "status": "pendente",
            "prazo": prazo
        }
        id_tarefa = self.proximo_id
        self.tarefas[id_tarefa] = tarefa
        self.proximo_id += 1
        self._salvar_dados()
        return id_tarefa

    def buscar_tarefa(self, id_tarefa):
        if id_tarefa not in self.tarefas:
            raise ValueError("Tarefa não encontrada")
        return self.tarefas[id_tarefa]

    def listar_tarefas(self):
        return self.tarefas

    def editar_tarefa(self, id_tarefa, titulo=None, disciplina=None, descricao=None, prioridade=None, prazo=None):
        if id_tarefa not in self.tarefas:
            raise ValueError("Tarefa não encontrada")
        tarefa = self.tarefas[id_tarefa]
        if titulo is not None:
            tarefa["titulo"] = titulo
        if disciplina is not None:
            tarefa["disciplina"] = disciplina
        if descricao is not None:
            tarefa["descricao"] = descricao
        if prioridade is not None:
            tarefa["prioridade"] = prioridade
        if prazo is not None:
            tarefa["prazo"] = prazo
        self._salvar_dados()

    def remover_tarefa(self, id_tarefa):
        if id_tarefa not in self.tarefas:
            raise ValueError("Tarefa não encontrada")
        del self.tarefas[id_tarefa]
        self._salvar_dados()

    def concluir_tarefa(self, id_tarefa):
        if id_tarefa not in self.tarefas:
            raise ValueError("Tarefa não encontrada")
        self.tarefas[id_tarefa]["status"] = "concluida"
        self._salvar_dados()

    def filtrar_por_disciplina(self, disciplina):
        return {
            id_tarefa: tarefa
            for id_tarefa, tarefa in self.tarefas.items()
            if tarefa["disciplina"].lower() == disciplina.lower()
        }

    def filtrar_por_prioridade(self, prioridade):
        return {
            id_tarefa: tarefa
            for id_tarefa, tarefa in self.tarefas.items()
            if tarefa["prioridade"] == prioridade
        }

    def filtrar_por_status(self, status):
        return {
            id_tarefa: tarefa
            for id_tarefa, tarefa in self.tarefas.items()
            if tarefa["status"] == status
        }
