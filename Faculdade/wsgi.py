"""
Ponto de entrada WSGI para produção.

PythonAnywhere: aponte o campo "WSGI configuration file" para este arquivo
e defina a variável de ambiente SECRET_KEY no painel deles.

Render / Railway: defina a variável de ambiente FLASK_ENV=production
e o start command como: gunicorn wsgi:application
"""

import os

# Garante que roda em modo produção quando chamado pelo servidor WSGI
os.environ.setdefault("FLASK_ENV", "production")

from app import create_app

application = create_app()   # PythonAnywhere usa "application"
app = application             # Gunicorn aceita ambos
