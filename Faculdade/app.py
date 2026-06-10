import os
from flask import Flask
from extensions import db
from config import Config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )
    app.config.from_object(config_class)
    db.init_app(app)

    from routes.auth         import auth_bp
    from routes.dashboard    import dashboard_bp
    from routes.estoque      import estoque_bp
    from routes.fornecedores import fornecedores_bp
    from routes.movimento    import movimento_bp
    from routes.curva_abc    import curva_abc_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(fornecedores_bp)
    app.register_blueprint(movimento_bp)
    app.register_blueprint(curva_abc_bp)

    with app.app_context():
        db.create_all()
        _seed_admin()

        # Dados iniciais do sistema (fornecedores + produtos)
        from seed import run_seed
        run_seed()

    return app


def _seed_admin():
    from werkzeug.security import generate_password_hash
    from models.usuario import Usuario
    if not Usuario.query.filter_by(nome="admin").first():
        db.session.add(Usuario(
            nome="admin",
            email="admin@eight.com",
            senha=generate_password_hash("admin123"),
            tipo="admin",
        ))
        db.session.commit()
        print("[seed] Admin criado — login: admin | senha: admin123")


if __name__ == "__main__":
    create_app().run(debug=True)
