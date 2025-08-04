# backend/app/commands.py
"""
Este arquivo define comandos de linha de comando (CLI) personalizados para o Flask.
Comandos CLI são úteis para automatizar tarefas de gerenciamento.
"""

import click
from flask.cli import with_appcontext
from .models import db, Usuario

@click.command(name='create-users')
@with_appcontext
def create_users_command():
    """Cria os usuários iniciais com diferentes papéis para teste."""
    db.create_all()

    # Dicionário com os usuários a serem criados
    users_to_create = {
        'bruce': {'role': 'admin_seguranca', 'password': 'gotham'},
        'lucius': {'role': 'gerente', 'password': 'fox'},
        'barbara': {'role': 'gerente', 'password': 'gordon'},
        'alfred': {'role': 'funcionario', 'password': 'pennyworth'},
        'tim': {'role': 'funcionario', 'password': 'drake'},
        'selina': {'role': 'funcionario', 'password': 'kyle'}
    }

    for username, data in users_to_create.items():
        if Usuario.query.filter_by(username=username).first() is None:
            user = Usuario(username=username, role=data['role'])
            user.set_password(data['password'])
            db.session.add(user)
            click.echo(f"Usuário '{username}' ({data['role']}) criado.")

    db.session.commit()
    click.echo('Comando para criar usuários finalizado.')
    