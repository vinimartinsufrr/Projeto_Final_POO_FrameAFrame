from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# 🔹 Inicializa SQLAlchemy e LoginManager
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # 🔹 Configuração do banco de dados SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(BASE_DIR, '../locadora.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "chave_secreta"

    # 🔹 Inicializa banco de dados e LoginManager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()  # 🔹 Garante que as tabelas são criadas antes do uso

    # 🔹 Importação de rotas
    from app.routes.auth import auth_bp
    from app.routes.home import home_bp
    from app.routes.filmes import filmes_bp
    from app.routes.locacoes import locacoes_bp
    from app.routes.relatorios import relatorios_bp
    from app.routes.explorar import explorar_bp
    from app.routes.relatorios_estoque import relatorios_estoque_bp
    from app.routes.meus_dados import meus_dados_bp
    from app.routes.minhas_locacoes import minhas_locacoes_bp
    from app.routes.avaliacoes import avaliacoes_bp

    # 🔹 Registro de Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(filmes_bp)
    app.register_blueprint(locacoes_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(explorar_bp)
    app.register_blueprint(relatorios_estoque_bp)
    app.register_blueprint(meus_dados_bp)
    app.register_blueprint(minhas_locacoes_bp)
    app.register_blueprint(avaliacoes_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario
    return Usuario.query.get(int(user_id))
