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