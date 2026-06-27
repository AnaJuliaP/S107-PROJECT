import pytest
from src.gerenciador import GerenciadorTarefas


def test_editar_disciplina_valida_atualiza_campo():
    g = GerenciadorTarefas()
    id_ = g.criar_tarefa("Tarefa", "C14", "Desc", "baixa", "2026-06-01")

    g.editar_tarefa(id_, disciplina="C15")

    assert g.buscar_tarefa(id_)["disciplina"] == "C15"


def test_editar_descricao_atualiza_campo():
    g = GerenciadorTarefas()
    id_ = g.criar_tarefa("Tarefa", "C14", "Descrição original", "media", "2026-06-01")

    g.editar_tarefa(id_, descricao="Descrição atualizada")

    assert g.buscar_tarefa(id_)["descricao"] == "Descrição atualizada"


def test_editar_prazo_atualiza_campo():
    g = GerenciadorTarefas()
    id_ = g.criar_tarefa("Tarefa", "C14", "Desc", "alta", "2026-06-01")

    g.editar_tarefa(id_, prazo="2026-12-31")

    assert g.buscar_tarefa(id_)["prazo"] == "2026-12-31"


def test_editar_todos_os_campos_simultaneamente():
    g = GerenciadorTarefas()
    id_ = g.criar_tarefa("Original", "C14", "Desc original", "baixa", "2026-01-01")

    g.editar_tarefa(id_, titulo="Editado", disciplina="C99",
                    descricao="Nova desc", prioridade="alta", prazo="2026-12-31")

    t = g.buscar_tarefa(id_)
    assert t["titulo"]     == "Editado"
    assert t["disciplina"] == "C99"
    assert t["descricao"]  == "Nova desc"
    assert t["prioridade"] == "alta"
    assert t["prazo"]      == "2026-12-31"


def test_listar_tarefas_retorna_vazio_no_inicio():
    g = GerenciadorTarefas()

    assert g.listar_tarefas() == {}


def test_filtrar_por_disciplina_case_insensitive():
    g = GerenciadorTarefas()
    g.criar_tarefa("Tarefa", "Matemática", "Desc", "alta", "2026-06-01")

    assert len(g.filtrar_por_disciplina("matemática")) == 1


def test_filtrar_por_status_pendente_exclui_concluidas():
    g = GerenciadorTarefas()
    id1 = g.criar_tarefa("T1", "C14", "Desc", "alta", "2026-06-01")
    id2 = g.criar_tarefa("T2", "C14", "Desc", "media", "2026-06-02")
    g.concluir_tarefa(id1)

    resultado = g.filtrar_por_status("pendente")

    assert id2 in resultado
    assert id1 not in resultado


def test_ids_continuam_incrementando_apos_remocao():
    g = GerenciadorTarefas()
    id1 = g.criar_tarefa("T1", "C14", "Desc", "baixa", "2026-06-01")
    g.remover_tarefa(id1)
    id2 = g.criar_tarefa("T2", "C14", "Desc", "media", "2026-06-02")

    assert id2 == 2


def test_descricao_pode_ser_string_vazia():
    g = GerenciadorTarefas()
    id_ = g.criar_tarefa("Tarefa", "C14", "", "baixa", "2026-06-01")

    assert g.buscar_tarefa(id_)["descricao"] == ""