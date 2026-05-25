# Imagem enxuta para execução local e CI (build reproduzível).
FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

# Dependências primeiro (melhor cache de camadas).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação e testes (integração roda no mesmo contexto).
COPY pyproject.toml .
COPY main.py .
COPY src ./src
COPY tests ./tests

# Usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Aplicação interativa (sobrescreva com `pytest` para a suíte).
CMD ["python", "main.py"]
