import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fornecedores.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Criando a rota inicial aqui para nunca mais dar o erro de 'index'!
    @app.route('/')
    def index():
        return '<h1>Página Inicial da Agenda de Fornecedores</h1><p>Vá para <a href="/auth/register">/auth/register</a> para testar o cadastro!</p>'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app