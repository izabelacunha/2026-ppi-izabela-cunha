import os
from flask import Flask

def create_app(test_config=None):
    # Cria e configura o aplicativo Flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fornecedores.sqlite'),
    )

    if test_config is None:
        # Carrega a configuração da instância, se existir, quando não estiver testando
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuração de teste se passada
        app.config.from_mapping(test_config)

    # Garante que a pasta da instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Olá! Bem-vindo ao Gerenciador de Fornecedores de Eventos!'

    from . import db
    db.init_app(app)

    return app