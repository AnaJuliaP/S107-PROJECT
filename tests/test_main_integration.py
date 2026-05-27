from __future__ import annotations

import builtins
import runpy
from pathlib import Path
from unittest.mock import patch

import pytest

import main as main_mod

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _feed_inputs(monkeypatch: pytest.MonkeyPatch, answers: list[str]) -> None:
    it = iter(answers)

    def fake_input(_prompt: str = "") -> str:
        try:
            return next(it)
        except StopIteration as exc:
            raise AssertionError(
                "main() solicitou mais entradas do que o teste forneceu"
            ) from exc

    monkeypatch.setattr(builtins, "input", fake_input)


def test_fluxo_basico_criar_listar_e_sair(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Revisão",
            "Cálculo I",
            "Lista 3",
            "alta",
            "2026-05-21",
            "2",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "GERENCIADOR DE TAREFAS" in out
    assert "Revisão" in out
    assert "Encerrando sistema" in out


def test_buscar_tarefa_por_id(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Estudo",
            "Física",
            "Cap 2",
            "media",
            "2026-06-01",
            "3",
            "1",
            "0",
        ],
    )
    main_mod.main()
    assert "Estudo" in capsys.readouterr().out


def test_editar_tarefa_campos_opcionais(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Antigo",
            "Química",
            "Lab",
            "baixa",
            "2026-04-10",
            "4",
            "1",
            "",
            "",
            "",
            "alta",
            "2026-04-12",
            "3",
            "1",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "Tarefa atualizada" in out
    assert "alta" in out


def test_remover_tarefa_confirmado(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Apagar",
            "Prog",
            "TP",
            "media",
            "2026-05-01",
            "5",
            "1",
            "s",
            "2",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "Tarefa removida" in out


def test_remover_tarefa_cancelado(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Manter",
            "BD",
            "SQL",
            "alta",
            "2026-05-02",
            "5",
            "1",
            "n",
            "2",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "Manter" in out
    assert "Tarefa removida" not in out


def test_concluir_tarefa(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "Entrega",
            "SO",
            "Relatório",
            "alta",
            "2026-05-30",
            "6",
            "1",
            "9",
            "concluida",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "Tarefa concluída" in out
    assert "concluida" in out


def test_filtros_disciplina_prioridade_status(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "A1",
            "Redes",
            "d1",
            "alta",
            "2026-01-01",
            "1",
            "A2",
            "Redes",
            "d2",
            "media",
            "2026-01-02",
            "1",
            "A3",
            "SO",
            "d3",
            "baixa",
            "2026-01-03",
            "7",
            "redes",
            "8",
            "media",
            "9",
            "pendente",
            "0",
        ],
    )
    main_mod.main()
    out = capsys.readouterr().out
    assert "A1" in out or "A2" in out
    assert "A2" in out or "media" in out


def test_opcao_invalida(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(monkeypatch, ["42", "0"])
    main_mod.main()
    assert "Opção inválida" in capsys.readouterr().out


def test_value_error_id_invalido(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(monkeypatch, ["3", "nao-eh-int", "0"])
    main_mod.main()
    assert "Erro:" in capsys.readouterr().out


def test_value_error_regra_de_negocio(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "",
            "X",
            "d",
            "alta",
            "2026-01-01",
            "0",
        ],
    )
    main_mod.main()
    assert "Título não pode ser vazio" in capsys.readouterr().out


def test_executar_main_como___main___via_runpy(
    monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    """Executa main.py com __name__ == '__main__' no mesmo processo (cobre o entrypoint)."""
    _feed_inputs(monkeypatch, ["0"])
    runpy.run_path(str(PROJECT_ROOT / "main.py"), run_name="__main__")
    assert "Encerrando sistema" in capsys.readouterr().out


def test_erro_inesperado(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _feed_inputs(
        monkeypatch,
        [
            "1",
            "X",
            "Y",
            "Z",
            "alta",
            "2026-01-01",
            "0",
        ],
    )
    with patch.object(main_mod.GerenciadorTarefas, "criar_tarefa", side_effect=RuntimeError("boom")):
        main_mod.main()
    assert "Erro inesperado" in capsys.readouterr().out
