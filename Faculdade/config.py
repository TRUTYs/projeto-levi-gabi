"""
Eight Sistemas — Configurações por ambiente.

Variáveis de ambiente reconhecidas:
  SECRET_KEY   — chave secreta para sessões (obrigatória em produção)
  DATABASE_URL — caminho do banco (opcional; padrão: sqlite local)
  FLASK_ENV    — "production" ou "development" (padrão: development)
"""

import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Detecta o ambiente pelo valor de FLASK_ENV
_ENV = os.environ.get("FLASK_ENV", "development").lower()
_EM_PRODUCAO = _ENV == "production"


class Config:
    # ── Segurança ────────────────────────────────────────────
    # Em produção DEVE ser definida via variável de ambiente.
    # Em desenvolvimento usa uma chave aleatória gerada na inicialização.
    SECRET_KEY = os.environ.get("SECRET_KEY") or (
        None if _EM_PRODUCAO else secrets.token_hex(32)
    )

    # ── Banco de dados ───────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(BASE_DIR, "projeto.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Debug ────────────────────────────────────────────────
    DEBUG = not _EM_PRODUCAO

    # ── Sessão ───────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY  = True   # JS não acessa o cookie de sessão
    SESSION_COOKIE_SAMESITE  = "Lax"  # Proteção contra CSRF básica
    SESSION_COOKIE_SECURE    = _EM_PRODUCAO  # HTTPS only em produção

    # Validação em produção
    @classmethod
    def validar(cls):
        if _EM_PRODUCAO and not os.environ.get("SECRET_KEY"):
            raise RuntimeError(
                "SECRET_KEY não definida. "
                "Defina a variável de ambiente SECRET_KEY antes de iniciar em produção."
            )
