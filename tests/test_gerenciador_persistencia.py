import os
import json
import tempfile
import pytest
from src.gerenciador import GerenciadorTarefas


def test_salvar_e_carregar_dados():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        caminho = f.name

    try:
        g = GerenciadorTarefas(arquivo_dados=caminho)
        g.criar_tarefa("Tarefa 1", "Matemática", "desc", "alta", "2025-12-01")

        g2 = GerenciadorTarefas(arquivo_dados=caminho)
        assert 1 in g2.tarefas
        assert g2.tarefas[1]["titulo"] == "Tarefa 1"
    finally:
        os.unlink(caminho)


def test_carregar_dados_arquivo_inexistente():
    g = GerenciadorTarefas(arquivo_dados="/tmp/nao_existe_xyz.json")
    assert g.tarefas == {}


def test_carregar_dados_json_invalido():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
        f.write("conteudo invalido")
        caminho = f.name

    try:
        g = GerenciadorTarefas(arquivo_dados=caminho)
        assert g.tarefas == {}
    finally:
        os.unlink(caminho)


def test_salvar_sem_arquivo_nao_falha():
    g = GerenciadorTarefas()
    g.criar_tarefa("Tarefa", "Física", "desc", "baixa", "2025-01-01")
    assert 1 in g.tarefas


def test_salvar_cria_diretorio_se_nao_existir():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "subdir", "dados.json")
        g = GerenciadorTarefas(arquivo_dados=caminho)
        g.criar_tarefa("Tarefa", "Química", "desc", "media", "2025-06-01")
        assert os.path.exists(caminho)


# ---------------------------------------------------------------------------
# Testes de persistência com PostgreSQL (executados quando há um banco
# acessível via DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME, como no
# docker-compose do projeto). Caso contrário, são pulados automaticamente.
# ---------------------------------------------------------------------------

def test_gerenciador_usa_postgres_quando_variaveis_definidas(postgres_env):
    g = GerenciadorTarefas()
    from src.repositories.postgres_repo import PostgresTarefaRepository
    assert isinstance(g.repo, PostgresTarefaRepository)


def test_postgres_criar_e_buscar_tarefa(postgres_repo):
    id_tarefa = postgres_repo.criar_tarefa(
        "Tarefa 1", "Matemática", "desc", "alta", "2025-12-01"
    )
    tarefa = postgres_repo.buscar_tarefa(id_tarefa)
    assert tarefa["titulo"] == "Tarefa 1"
    assert tarefa["disciplina"] == "Matemática"
    assert tarefa["status"] == "pendente"


def test_postgres_buscar_tarefa_inexistente_levanta_erro(postgres_repo):
    with pytest.raises(ValueError):
        postgres_repo.buscar_tarefa(999)


def test_postgres_listar_tarefas(postgres_repo):
    postgres_repo.criar_tarefa("Tarefa 1", "Física", "desc", "baixa", "2025-01-01")
    postgres_repo.criar_tarefa("Tarefa 2", "Química", "desc", "media", "2025-02-01")

    tarefas = postgres_repo.listar_tarefas()
    assert len(tarefas) == 2


def test_postgres_editar_tarefa(postgres_repo):
    id_tarefa = postgres_repo.criar_tarefa(
        "Tarefa", "Física", "desc", "baixa", "2025-01-01"
    )
    postgres_repo.editar_tarefa(id_tarefa, titulo="Tarefa Editada")

    tarefa = postgres_repo.buscar_tarefa(id_tarefa)
    assert tarefa["titulo"] == "Tarefa Editada"


def test_postgres_editar_tarefa_inexistente_levanta_erro(postgres_repo):
    with pytest.raises(ValueError):
        postgres_repo.editar_tarefa(999, titulo="Novo título")


def test_postgres_remover_tarefa(postgres_repo):
    id_tarefa = postgres_repo.criar_tarefa(
        "Tarefa", "Física", "desc", "baixa", "2025-01-01"
    )
    postgres_repo.remover_tarefa(id_tarefa)

    with pytest.raises(ValueError):
        postgres_repo.buscar_tarefa(id_tarefa)


def test_postgres_remover_tarefa_inexistente_levanta_erro(postgres_repo):
    with pytest.raises(ValueError):
        postgres_repo.remover_tarefa(999)


def test_postgres_concluir_tarefa(postgres_repo):
    id_tarefa = postgres_repo.criar_tarefa(
        "Tarefa", "Física", "desc", "baixa", "2025-01-01"
    )
    postgres_repo.concluir_tarefa(id_tarefa)

    tarefa = postgres_repo.buscar_tarefa(id_tarefa)
    assert tarefa["status"] == "concluida"


def test_postgres_filtrar_por_disciplina(postgres_repo):
    postgres_repo.criar_tarefa("Tarefa 1", "Física", "desc", "baixa", "2025-01-01")
    postgres_repo.criar_tarefa("Tarefa 2", "Química", "desc", "media", "2025-02-01")

    resultado = postgres_repo.filtrar_por_disciplina("física")
    assert len(resultado) == 1
    assert list(resultado.values())[0]["titulo"] == "Tarefa 1"


def test_postgres_filtrar_por_prioridade(postgres_repo):
    postgres_repo.criar_tarefa("Tarefa 1", "Física", "desc", "baixa", "2025-01-01")
    postgres_repo.criar_tarefa("Tarefa 2", "Química", "desc", "alta", "2025-02-01")

    resultado = postgres_repo.filtrar_por_prioridade("alta")
    assert len(resultado) == 1
    assert list(resultado.values())[0]["titulo"] == "Tarefa 2"


def test_postgres_filtrar_por_status(postgres_repo):
    id_tarefa = postgres_repo.criar_tarefa(
        "Tarefa 1", "Física", "desc", "baixa", "2025-01-01"
    )
    postgres_repo.criar_tarefa("Tarefa 2", "Química", "desc", "alta", "2025-02-01")
    postgres_repo.concluir_tarefa(id_tarefa)

    pendentes = postgres_repo.filtrar_por_status("pendente")
    concluidas = postgres_repo.filtrar_por_status("concluida")
    assert len(pendentes) == 1
    assert len(concluidas) == 1


def test_postgres_via_gerenciador_tarefas(postgres_env):
    g = GerenciadorTarefas()
    id_tarefa = g.criar_tarefa("Tarefa", "Biologia", "desc", "media", "2025-03-01")
    assert g.buscar_tarefa(id_tarefa)["titulo"] == "Tarefa"

    g.concluir_tarefa(id_tarefa)
    with pytest.raises(ValueError):
        g.concluir_tarefa(id_tarefa)