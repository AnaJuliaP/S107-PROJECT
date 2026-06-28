import os
import psycopg2
from psycopg2.extras import RealDictCursor
from src.repositories.base import RepositorioTarefas

class PostgresTarefaRepository(RepositorioTarefas):
    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self._inicializar_tabela()

    def _get_connection(self):
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )

    def _inicializar_tabela(self):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tarefas (
                        id SERIAL PRIMARY KEY,
                        titulo VARCHAR(255) NOT NULL,
                        disciplina VARCHAR(255) NOT NULL,
                        descricao TEXT,
                        prioridade VARCHAR(50) NOT NULL,
                        status VARCHAR(50) NOT NULL DEFAULT 'pendente',
                        prazo VARCHAR(100)
                    );
                """)
                conn.commit()
        finally:
            conn.close()

    def criar_tarefa(self, titulo, disciplina, descricao, prioridade, prazo):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tarefas (titulo, disciplina, descricao, prioridade, status, prazo)
                    VALUES (%s, %s, %s, %s, 'pendente', %s)
                    RETURNING id;
                """, (titulo, disciplina, descricao, prioridade, prazo))
                id_tarefa = cur.fetchone()[0]
                conn.commit()
                return id_tarefa
        finally:
            conn.close()

    def buscar_tarefa(self, id_tarefa):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT titulo, disciplina, descricao, prioridade, status, prazo 
                    FROM tarefas WHERE id = %s;
                """, (id_tarefa,))
                res = cur.fetchone()
                if not res:
                    raise ValueError("Tarefa não encontrada")
                return dict(res)
        finally:
            conn.close()

    def listar_tarefas(self):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, titulo, disciplina, descricao, prioridade, status, prazo FROM tarefas;")
                res = cur.fetchall()
                ret = {}
                for row in res:
                    t_id = row['id']
                    t_data = dict(row)
                    del t_data['id']
                    ret[t_id] = t_data
                return ret
        finally:
            conn.close()

    def editar_tarefa(self, id_tarefa, titulo=None, disciplina=None, descricao=None, prioridade=None, prazo=None):
        self.buscar_tarefa(id_tarefa)  # Levanta erro se não existir
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                campos = []
                valores = []
                if titulo is not None:
                    campos.append("titulo = %s")
                    valores.append(titulo)
                if disciplina is not None:
                    campos.append("disciplina = %s")
                    valores.append(disciplina)
                if descricao is not None:
                    campos.append("descricao = %s")
                    valores.append(descricao)
                if prioridade is not None:
                    campos.append("prioridade = %s")
                    valores.append(prioridade)
                if prazo is not None:
                    campos.append("prazo = %s")
                    valores.append(prazo)

                if campos:
                    valores.append(id_tarefa)
                    query = f"UPDATE tarefas SET {', '.join(campos)} WHERE id = %s;"
                    cur.execute(query, tuple(valores))
                    conn.commit()
        finally:
            conn.close()

    def remover_tarefa(self, id_tarefa):
        self.buscar_tarefa(id_tarefa)  # Levanta erro se não existir
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tarefas WHERE id = %s;", (id_tarefa,))
                conn.commit()
        finally:
            conn.close()

    def concluir_tarefa(self, id_tarefa):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE tarefas SET status = 'concluida' WHERE id = %s;", (id_tarefa,))
                conn.commit()
        finally:
            conn.close()

    def filtrar_por_disciplina(self, disciplina):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, titulo, disciplina, descricao, prioridade, status, prazo 
                    FROM tarefas WHERE LOWER(disciplina) = LOWER(%s);
                """, (disciplina,))
                res = cur.fetchall()
                ret = {}
                for row in res:
                    t_id = row['id']
                    t_data = dict(row)
                    del t_data['id']
                    ret[t_id] = t_data
                return ret
        finally:
            conn.close()

    def filtrar_por_prioridade(self, prioridade):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, titulo, disciplina, descricao, prioridade, status, prazo 
                    FROM tarefas WHERE prioridade = %s;
                """, (prioridade,))
                res = cur.fetchall()
                ret = {}
                for row in res:
                    t_id = row['id']
                    t_data = dict(row)
                    del t_data['id']
                    ret[t_id] = t_data
                return ret
        finally:
            conn.close()

    def filtrar_por_status(self, status):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, titulo, disciplina, descricao, prioridade, status, prazo 
                    FROM tarefas WHERE status = %s;
                """, (status,))
                res = cur.fetchall()
                ret = {}
                for row in res:
                    t_id = row['id']
                    t_data = dict(row)
                    del t_data['id']
                    ret[t_id] = t_data
                return ret
        finally:
            conn.close()
