import os
import psycopg2
import pytest


def pytest_html_report_title(report):
    report.title = "Relatório de testes — Gerenciador de Tarefas Acadêmicas"


def pytest_html_results_summary(prefix, summary, postfix, session):
    prefix.append(
        '<div class="report-brand">'
        '<div class="report-brand__row">'
        '<span class="report-badge">pytest · relatório HTML</span>'
        '<a class="report-brand__back" href="index.html">← Página do projeto</a>'
        "</div>"
        '<h2 class="report-summary-title">Resumo</h2>'
        "</div>"
    )


POSTGRES_TEST_ENV = {
    "DB_HOST": os.getenv("DB_HOST", "localhost"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_USER": os.getenv("DB_USER", "admin"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD", "admin"),
    "DB_NAME": os.getenv("DB_NAME", "tarefas"),
}


def _conectar_postgres():
    return psycopg2.connect(
        host=POSTGRES_TEST_ENV["DB_HOST"],
        port=POSTGRES_TEST_ENV["DB_PORT"],
        user=POSTGRES_TEST_ENV["DB_USER"],
        password=POSTGRES_TEST_ENV["DB_PASSWORD"],
        database=POSTGRES_TEST_ENV["DB_NAME"],
    )


def _postgres_disponivel():
    try:
        conn = _conectar_postgres()
        conn.close()
        return True
    except Exception:
        return False


def _limpar_tabela_tarefas():
    conn = _conectar_postgres()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS tarefas ("
                "id SERIAL PRIMARY KEY, "
                "titulo VARCHAR(255) NOT NULL, "
                "disciplina VARCHAR(255) NOT NULL, "
                "descricao TEXT, "
                "prioridade VARCHAR(50) NOT NULL, "
                "status VARCHAR(50) NOT NULL DEFAULT 'pendente', "
                "prazo VARCHAR(100));"
            )
            cur.execute("TRUNCATE TABLE tarefas RESTART IDENTITY;")
            conn.commit()
    finally:
        conn.close()


@pytest.fixture(scope="session")
def postgres_disponivel():
    return _postgres_disponivel()


@pytest.fixture
def postgres_env(monkeypatch, postgres_disponivel):
    """Configura as variáveis de ambiente do PostgreSQL e pula o teste
    se não houver um banco acessível (ex: execução local sem docker-compose)."""
    if not postgres_disponivel:
        pytest.skip("PostgreSQL não disponível para testes de integração")

    for chave, valor in POSTGRES_TEST_ENV.items():
        monkeypatch.setenv(chave, valor)

    _limpar_tabela_tarefas()
    yield POSTGRES_TEST_ENV
    _limpar_tabela_tarefas()


@pytest.fixture
def postgres_repo(postgres_env):
    from src.repositories.postgres_repo import PostgresTarefaRepository

    return PostgresTarefaRepository()