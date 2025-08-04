# backend/app/models.py
"""
Este arquivo define os modelos de dados da nossa aplicação.
Modelos são representações em Python das tabelas do nosso banco de dados.
Usamos o Flask-SQLAlchemy para gerenciar essa interação.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Criamos a instância do SQLAlchemy. Ela não está ligada a nenhuma aplicação ainda.
# Ela será conectada à nossa aplicação Flask no arquivo __init__.py.
db = SQLAlchemy()


class Usuario(db.Model):
    """
    Representa a tabela 'usuario' no banco de dados.
    Armazena as informações de cada usuário do sistema.
    """
    __tablename__ = 'usuario'  # Nome explícito da tabela

    # Define as colunas da tabela:
    # Chave primária, autoincremento por padrão.
    id = db.Column(db.Integer, primary_key=True)
    # Nome de usuário, deve ser único.
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Armazena a senha de forma segura (hash).
    password_hash = db.Column(db.String(256), nullable=False)

    # Coluna para o papel do usuário (nível de acesso).
    # Valores possíveis: 'funcionario', 'gerente', 'admin_seguranca'.
    role = db.Column(db.String(50), nullable=False, default='funcionario')

    def set_password(self, password):
        """
        Recebe uma senha em texto puro e a armazena na propriedade 'password_hash'
        de forma segura, usando um algoritmo de hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Recebe uma senha em texto puro e a compara com o hash armazenado no banco de dados.
        Retorna True se a senha for correta, False caso contrário.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # Representação em texto do objeto, útil para depuração.
        return f'<Usuario {self.username}>'


class Recurso(db.Model):
    """
    Representa a tabela 'recurso' no banco de dados.
    Armazena o inventário de equipamentos, veículos e dispositivos de segurança.
    """
    __tablename__ = 'recurso'

    # Define as colunas da tabela:
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # O tipo do recurso, ex: 'equipamento', 'veiculo', etc.
    tipo = db.Column(db.String(50), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False, default=1)

    # O estado atual do recurso, ex: 'disponivel', 'em uso', 'manutencao'.
    status = db.Column(db.String(50), nullable=False, default='disponivel')

    def __repr__(self):
        return f'<Recurso {self.nome}>'
