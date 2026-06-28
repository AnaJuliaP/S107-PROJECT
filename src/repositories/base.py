from abc import ABC, abstractmethod

class RepositorioTarefas(ABC):
    @abstractmethod
    def criar_tarefa(self, titulo, disciplina, descricao, prioridade, prazo) -> int:
        pass

    @abstractmethod
    def buscar_tarefa(self, id_tarefa) -> dict:
        pass

    @abstractmethod
    def listar_tarefas(self) -> dict:
        pass

    @abstractmethod
    def editar_tarefa(self, id_tarefa, titulo=None, disciplina=None, descricao=None, prioridade=None, prazo=None) -> None:
        pass

    @abstractmethod
    def remover_tarefa(self, id_tarefa) -> None:
        pass

    @abstractmethod
    def concluir_tarefa(self, id_tarefa) -> None:
        pass

    @abstractmethod
    def filtrar_por_disciplina(self, disciplina) -> dict:
        pass

    @abstractmethod
    def filtrar_por_prioridade(self, prioridade) -> dict:
        pass

    @abstractmethod
    def filtrar_por_status(self, status) -> dict:
        pass
