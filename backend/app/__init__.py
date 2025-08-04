# backend/app/__init__.py
"""
Este arquivo é o ponto de entrada para o nosso pacote 'app'.
Ele contém a função 'Application Factory', que é responsável por:
1. Criar a instância principal da aplicação Flask.
2. Carregar as configurações.
3. Inicializar extensões (como o banco de dados).
4. Registrar os 'Blueprints' (nossos conjuntos de rotas).
"""

import os
from flask import Flask
from flask_cors import CORS


def create_app():
    """Cria e configura uma instância da aplicação Flask."""

    # 1. Cria a instância da aplicação
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    # 'instance_relative_config=True' diz ao Flask para procurar arquivos de configuração
    # na pasta 'instance', que será criada no mesmo nível da pasta 'app'.
    # É um bom lugar para colocar segredos e o banco de dados.

    # 2. Define as configurações
    # Em um projeto real, esta chave seria mais complexa e guardada fora do código.
    # Usamos ela para assinar o token de segurança (JWT).
    app.config['SECRET_KEY'] = 'a-chave-secreta-de-bruce-wayne'

    # Define o local do nosso banco de dados SQLite.
    # O banco de dados se chamará 'wayne_industries.db' e será salvo na pasta 'instance'.
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'wayne_industries.db')}"

    # Desativa uma funcionalidade do SQLAlchemy que não usaremos e que emite avisos.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. Garante que a pasta 'instance' exista
    # O Flask não cria essa pasta automaticamente, então nós garantimos que ela esteja lá.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # A pasta já existe, não há nada a fazer.

    # 4. Importa e inicializa o banco de dados com a aplicação
    from .models import db
    db.init_app(app)

    # 5. Importa e registra os Blueprints (conjuntos de rotas)
    # Importamos nossas rotas aqui para evitar 'importações circulares'.
    from .routes import api
    from .auth import auth_bp
    app.register_blueprint(api)
    app.register_blueprint(auth_bp)

    # 6. Importa e registra os comandos de linha de comando
    from .commands import create_users_command
    app.cli.add_command(create_users_command)

    # A fábrica retorna a aplicação configurada, pronta para ser executada.
    return app
